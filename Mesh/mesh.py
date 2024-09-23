import open3d as o3d
import numpy as np

# upload the clean .ply and view
pcd = o3d.io.read_point_cloud("clean_point_cloud.ply")
o3d.visualization.draw_geometries([pcd], window_name="Clean point cloud")

# filter to delete noise
pcd = pcd.voxel_down_sample(voxel_size=0.005)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
pcd.orient_normals_consistent_tangent_plane(k=10)

# mesh reconstruction with Ball Pivoting Algorithm
radii = [0.005, 0.01, 0.015, 0.02]  
mesh_bpa = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector(radii))

# clean up
mesh_bpa.remove_degenerate_triangles()
mesh_bpa.remove_duplicated_triangles()
mesh_bpa.remove_duplicated_vertices()
mesh_bpa.remove_non_manifold_edges()
mesh_bpa = mesh_bpa.simplify_quadric_decimation(target_number_of_triangles=50000)


o3d.visualization.draw_geometries([mesh_bpa], window_name="BPA mesh")
o3d.io.write_triangle_mesh("mesh_bpa_generado.ply", mesh_bpa)
print("Save as 'mesh_bpa_generado.ply'.")

# Poisson Surface Reconstruction 
mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=12, scale=1.1)

# low density vertex
vertices_to_remove = densities < np.quantile(densities, 0.02) 
mesh_poisson.remove_vertices_by_mask(vertices_to_remove)

# clean up
mesh_poisson.remove_degenerate_triangles()
mesh_poisson.remove_duplicated_triangles()
mesh_poisson.remove_duplicated_vertices()
mesh_poisson.remove_non_manifold_edges()

# save and view
o3d.visualization.draw_geometries([mesh_poisson], window_name="Poisson mesh")
o3d.io.write_triangle_mesh("mesh_poisson_generado.ply", mesh_poisson)
print("save as 'mesh_poisson_generado.ply'.")
