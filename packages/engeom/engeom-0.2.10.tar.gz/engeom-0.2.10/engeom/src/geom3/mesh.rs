//! This module contains an abstraction for a mesh of triangles, represented by vertices and their
//! indices into the vertex list.  This abstraction is built around the `TriMesh` type from the
//! `parry3d` crate.

mod conformal;
mod edges;
mod faces;
pub mod filtering;
mod measurement;
mod outline;
mod patches;
mod queries;
mod sampling;
mod uv_mapping;
mod collisions;

pub use self::uv_mapping::UvMapping;
pub use self::collisions::MeshCollisionSet;
use crate::geom3::Aabb3;
use crate::{Iso3, Point2, Point3, Result, SurfacePoint3, UnitVec3, Vector3};
pub use edges::MeshEdges;
use parry3d_f64::shape::{TriMesh, TriMeshFlags};
use parry3d_f64::transformation;

#[derive(Clone)]
pub struct Mesh {
    shape: TriMesh,
    is_solid: bool,
    uv: Option<UvMapping>,
}

// Core access
impl Mesh {
    /// Get a reference to the AABB of the underlying mesh in the local coordinate system.
    pub fn aabb(&self) -> &Aabb3 {
        self.shape.local_aabb()
    }

    /// Gets a reference to the underlying `TriMesh` object to provide direct access to
    /// the `parry3d` API.
    pub fn tri_mesh(&self) -> &TriMesh {
        &self.shape
    }

    /// Return a flag indicating whether the mesh is considered "solid" or not for the purposes of
    /// distance queries. If a mesh is "solid", then distance queries for points on the inside of
    /// the mesh will return a zero distance.
    pub fn is_solid(&self) -> bool {
        self.is_solid
    }

    /// Get a reference to the vertices of the mesh.
    pub fn vertices(&self) -> &[Point3] {
        self.shape.vertices()
    }

    /// Get a reference to the face indices of the mesh.
    pub fn faces(&self) -> &[[u32; 3]] {
        self.shape.indices()
    }
}

impl Mesh {
    pub fn calc_edges(&self) -> Result<MeshEdges> {
        MeshEdges::new(self)
    }

    /// Create a new mesh from a list of vertices and a list of triangles.  Additional options can
    /// be set to merge duplicate vertices and delete degenerate triangles.
    ///
    /// # Arguments
    ///
    /// * `vertices`:
    /// * `triangles`:
    /// * `is_solid`:
    /// * `merge_duplicates`:
    /// * `delete_degenerate`:
    /// * `uv`:
    ///
    /// returns: Result<Mesh, Box<dyn Error, Global>>
    ///
    /// # Examples
    ///
    /// ```
    ///
    /// ```
    pub fn new_with_options(
        vertices: Vec<Point3>,
        triangles: Vec<[u32; 3]>,
        is_solid: bool,
        merge_duplicates: bool,
        delete_degenerate: bool,
        uv: Option<UvMapping>,
    ) -> Result<Self> {
        let mut flags = TriMeshFlags::empty();
        if merge_duplicates {
            flags |= TriMeshFlags::MERGE_DUPLICATE_VERTICES;
            flags |= TriMeshFlags::DELETE_DUPLICATE_TRIANGLES;
        }
        if delete_degenerate {
            flags |= TriMeshFlags::DELETE_BAD_TOPOLOGY_TRIANGLES;
            flags |= TriMeshFlags::DELETE_DEGENERATE_TRIANGLES;
        }

        let shape = TriMesh::with_flags(vertices, triangles, flags)?;
        Ok(Self {
            shape,
            is_solid,
            uv,
        })
    }

    pub fn new(vertices: Vec<Point3>, triangles: Vec<[u32; 3]>, is_solid: bool) -> Self {
        let shape = TriMesh::new(vertices, triangles).expect("Failed to create TriMesh");
        Self {
            shape,
            is_solid,
            uv: None,
        }
    }
    pub fn new_take_trimesh(shape: TriMesh, is_solid: bool) -> Self {
        Self {
            shape,
            is_solid,
            uv: None,
        }
    }

    /// Return a convex hull of the points in the mesh.
    pub fn convex_hull(&self) -> Self {
        let (vertices, faces) = transformation::convex_hull(self.shape.vertices());
        Self::new(vertices, faces, true)
    }

    pub fn append(&mut self, other: &Mesh) -> Result<()> {
        // For now, both meshes must have an empty UV mapping
        if self.uv.is_some() || other.uv.is_some() {
            return Err("Cannot append meshes with UV mappings".into());
        }

        self.shape.append(&other.shape);
        Ok(())
    }

    pub fn new_with_uv(
        vertices: Vec<Point3>,
        triangles: Vec<[u32; 3]>,
        is_solid: bool,
        uv: Option<UvMapping>,
    ) -> Self {
        let shape =
            TriMesh::new(vertices, triangles).expect("Failed to create TriMesh with UV mapping");
        Self {
            shape,
            is_solid,
            uv,
        }
    }

    pub fn uv(&self) -> Option<&UvMapping> {
        self.uv.as_ref()
    }
    pub fn transform(&mut self, transform: &Iso3) {
        self.shape.transform_vertices(transform);
    }

    pub fn uv_to_3d(&self, uv: &Point2) -> Option<SurfacePoint3> {
        let (i, bc) = self.uv()?.triangle(uv)?;
        let t = self.shape.triangle(i as u32);
        let coords = t.a.coords * bc[0] + t.b.coords * bc[1] + t.c.coords * bc[2];

        t.normal().map(|n| SurfacePoint3::new(coords.into(), n))
    }

    pub fn uv_with_tol(
        &self,
        point: &Point3,
        max_dist: f64,
        max_angle: f64,
        transform: Option<&Iso3>,
    ) -> Option<(Point2, f64)> {
        if let Some(uv_map) = self.uv() {
            let point = if let Some(transform) = transform {
                transform * point
            } else {
                *point
            };

            if let Some((prj, id, loc)) = self.project_with_tol(&point, max_dist, max_angle, None) {
                let triangle = self.shape.triangle(id);
                if let Some(normal) = triangle.normal() {
                    let uv = uv_map.point(id as usize, loc.barycentric_coordinates().unwrap());
                    // Now find the depth
                    let sp = SurfacePoint3::new(prj.point, normal);
                    Some((uv, sp.scalar_projection(&point)))
                } else {
                    None
                }
            } else {
                None
            }
        } else {
            None
        }
    }

    pub fn create_box(width: f64, height: f64, depth: f64, is_solid: bool) -> Self {
        let (vertices, triangles) = box_geom(width, height, depth);
        Self::new(vertices, triangles, is_solid)
    }

    pub fn create_cylinder(radius: f64, height: f64, steps: usize) -> Self {
        let mut vertices = Vec::new();
        let mut faces: Vec<[u32; 3]> = Vec::new();

        for i in 0..steps {
            let angle = i as f64 * 2.0 * std::f64::consts::PI / (steps as f64);
            let x = radius * angle.cos();
            let y = radius * angle.sin();

            // First vertex is i * 2
            vertices.push(Point3::new(x, y, 0.0));
            // Second vertex is i * 2 + 1
            vertices.push(Point3::new(x, y, height));

            let k = (i + 1) % steps;

            faces.push([(i * 2) as u32, (i * 2 + 1) as u32, (k * 2 + 1) as u32]);
            faces.push([(i * 2) as u32, (k * 2) as u32, (k * 2 + 1) as u32]);
        }

        Mesh::new(vertices, faces, false)
    }

    pub fn get_patches(&self) -> Vec<Vec<usize>> {
        patches::compute_patch_indices(self)
    }

    /// Gets the boundary points of each patch in the mesh.  This function will return a list of
    /// lists of points, where each list of points is the boundary of a patch.  Note that this
    /// function will not work on non-manifold meshes.
    ///
    /// returns: Result<Vec<Vec<usize, Global>, Global>>
    pub fn get_patch_boundary_points(&self) -> Result<Vec<Vec<Point3>>> {
        let patches = self.get_patches();
        let mut result = Vec::new();
        for patch in patches.iter() {
            result.extend(patches::compute_boundary_points(self, patch)?);
        }

        Ok(result)
    }

    pub fn get_face_normals(&self) -> Result<Vec<UnitVec3>> {
        let mut result = Vec::new();
        for t in self.shape.triangles() {
            if let Some(n) = t.normal() {
                result.push(n.clone());
            } else {
                return Err("Failed to get normal".into());
            }
        }

        Ok(result)
    }

    pub fn get_vertex_normals(&self) -> Vec<Vector3> {
        let mut sums: Vec<Vector3> = vec![Vector3::new(0.0, 0.0, 0.0); self.shape.vertices().len()];
        let mut counts = vec![0; self.shape.vertices().len()];

        for (indices, tri) in self.shape.indices().iter().zip(self.shape.triangles()) {
            if let Some(n) = tri.normal() {
                for i in indices {
                    sums[*i as usize] += n.into_inner();
                    counts[*i as usize] += 1;
                }
            }
        }

        // Normalize the normals
        for i in 0..sums.len() {
            if counts[i] > 0 {
                let v = sums[i] / counts[i] as f64;
                sums[i] = v.normalize();
            }
        }

        sums
    }
}

fn box_geom(width: f64, height: f64, depth: f64) -> (Vec<Point3>, Vec<[u32; 3]>) {
    let vertices = vec![
        Point3::new(0.0, 0.0, 0.0),
        Point3::new(width, 0.0, 0.0),
        Point3::new(0.0, 0.0, depth),
        Point3::new(width, 0.0, depth),
        Point3::new(0.0, height, 0.0),
        Point3::new(width, height, 0.0),
        Point3::new(0.0, height, depth),
        Point3::new(width, height, depth),
    ];

    let triangles = vec![
        [4, 7, 5],
        [4, 6, 7],
        [0, 2, 4],
        [2, 6, 4],
        [0, 1, 2],
        [1, 3, 2],
        [1, 5, 7],
        [1, 7, 3],
        [2, 3, 7],
        [2, 7, 6],
        [0, 4, 1],
        [1, 4, 5],
    ];

    (vertices, triangles)
}
