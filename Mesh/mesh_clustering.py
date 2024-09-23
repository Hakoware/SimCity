import open3d as o3d
import numpy as np

# upload ply
pcd = o3d.io.read_point_cloud("point_cloud.ply")

# view the point cloud
o3d.visualization.draw_geometries([pcd], window_name="Point cloud")
# Filter by clustering to delete the noise
# Identify clusters in the point cloud using DBSCAN
# dbscan_eps determines the proximity between points to consider them in the same cluster
# min_points is the minimum number of points to consider a valid cluster
labels = np.array(pcd.cluster_dbscan(eps=0.05, min_points=10, print_progress=True))

# Bigger cluster. Object of interest
max_label = labels.max()
largest_cluster_index = np.argmax(np.bincount(labels[labels >= 0]))

# Filter the points belonging to the largest cluster
pcd = pcd.select_by_index(np.where(labels == largest_cluster_index)[0])

# Filter to delete noise
pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

# View the clean point cloud
o3d.visualization.draw_geometries([pcd], window_name="Clean point cloud")
# Save the clean point cloud
o3d.io.write_point_cloud("clean_point_cloud.ply", pcd)

# Estimate normal to mesh reconstruction
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# meshreconstruction with Poisson Surface Reconstruction
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

# Filter mesh faces to remove those with low density values
vertices_to_remove = densities < np.quantile(densities, 0.01) 
mesh.remove_vertices_by_mask(vertices_to_remove)

# Clean up the generated mesh
mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=50000)
mesh.remove_degenerate_triangles()
mesh.remove_duplicated_triangles()
mesh.remove_duplicated_vertices()
mesh.remove_non_manifold_edges()

# View the mesh
o3d.visualization.draw_geometries([mesh], window_name="Mesh")

# save in .obj format
o3d.io.write_triangle_mesh("mesh_generado.obj", mesh)
