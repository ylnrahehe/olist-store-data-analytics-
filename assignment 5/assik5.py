import open3d as o3d
import numpy as np
import copy
import tempfile
import os


MODEL_PATH = "Wolf_obj.obj"  
SAMPLE_POINTS = 500000    
VOXEL_SIZE = 0.02        
POISSON_DEPTH = 10        


def print_mesh_info(name, mesh):
    v = np.asarray(mesh.vertices).shape[0]
    t = np.asarray(mesh.triangles).shape[0] if np.asarray(mesh.triangles).size else 0
    has_colors = mesh.has_vertex_colors()
    has_normals = mesh.has_vertex_normals()
    print(f"=== {name} ===")
    print(f"Vertices: {v}")
    print(f"Triangles: {t}")
    print(f"Has vertex colors: {has_colors}")
    print(f"Has vertex normals: {has_normals}")
    print()

def print_pcd_info(name, pcd):
    v = np.asarray(pcd.points).shape[0]
    has_colors = pcd.has_colors()
    has_normals = pcd.has_normals()
    print(f"=== {name} ===")
    print(f"Points: {v}")
    print(f"Has colors: {has_colors}")
    print(f"Has normals: {has_normals}")
    print()

def print_voxel_info(name, vox):
    # vox is VoxelGrid
    vox_count = len(vox.get_voxels())
    print(f"=== {name} ===")
    print(f"Voxels: {vox_count}")
    print()

#original model
mesh = o3d.io.read_triangle_mesh(MODEL_PATH)
if mesh is None or len(mesh.vertices) == 0:
    raise ValueError("Не удалось загрузить mesh. Проверьте MODEL_PATH и формат файла.")

# Compute normals if отсутствуют 
if not mesh.has_vertex_normals():
    mesh.compute_vertex_normals()

# show original mesh
print_mesh_info("Original mesh (step 1)", mesh)
o3d.visualization.draw_geometries([mesh], window_name="Step 1: Original mesh")

#point cloud 
tmp_ply = None
try:
    #читаем как point cloud напрямую 
    pcd_try = o3d.io.read_point_cloud(MODEL_PATH)
    if np.asarray(pcd_try.points).size == 0:
        
        pcd_sampled = mesh.sample_points_uniformly(number_of_points=SAMPLE_POINTS)
        #прочитаем через read_point_cloud 
        tmp_ply = tempfile.NamedTemporaryFile(suffix=".ply", delete=False)
        o3d.io.write_point_cloud(tmp_ply.name, pcd_sampled)
        pcd = o3d.io.read_point_cloud(tmp_ply.name)
        tmp_ply.close()
    else:
        pcd = pcd_try
except Exception as e:
    # fallback: sample from mesh
    pcd_sampled = mesh.sample_points_uniformly(number_of_points=SAMPLE_POINTS)
    tmp_ply = tempfile.NamedTemporaryFile(suffix=".ply", delete=False)
    o3d.io.write_point_cloud(tmp_ply.name, pcd_sampled)
    pcd = o3d.io.read_point_cloud(tmp_ply.name)
    tmp_ply.close()

print_pcd_info("Point cloud (step 2)", pcd)
o3d.visualization.draw_geometries([pcd], window_name="Step 2: Point Cloud")

#Surface reconstruction (Poisson)
if not pcd.has_normals():
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
# Poisson reconstruction
print("Запускаю Poisson reconstruction (может занять время)...")
mesh_poisson, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=POISSON_DEPTH)

dens = np.asarray(densities)
# установим порог как 0.01 
thr = np.quantile(dens, 0.01)
vertices_to_keep = dens > thr
# Удаляем вершины и находим бибокс

bbox = pcd.get_axis_aligned_bounding_box()
mesh_poisson_crop = mesh_poisson.crop(bbox)


mesh_poisson_crop.compute_vertex_normals()

print_mesh_info("Poisson mesh (step 3) BEFORE crop", mesh_poisson)
print_mesh_info("Poisson mesh (step 3) AFTER crop", mesh_poisson_crop)
print("Poisson восстановил поверхность; crop удалил артефакты вне bbox облака.")
o3d.visualization.draw_geometries([mesh_poisson_crop], window_name="Step 3: Poisson reconstructed mesh (cropped)")

#Voxelization
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=VOXEL_SIZE)
print_voxel_info("Voxel grid (step 4)", voxel_grid)
print("выбран размер вокселя и видно, как меняется разрешение формы.")

o3d.visualization.draw_geometries([voxel_grid], window_name="Step 4: Voxel grid")

# Adding a plane
# Создаём плоскость как box
plane = o3d.geometry.TriangleMesh.create_box(width=2.0, height=2.0, depth=0.01)
plane.compute_vertex_normals()
# разместим plane рядом с объектом: возьмём центр объекта и сместим по X
center = pcd.get_center()
plane.translate(center + np.array([max(bbox.get_extent()) * 0.6, 0, -0.5]))
plane.paint_uniform_color([0.8, 0.2, 0.2])  
o3d.visualization.draw_geometries([mesh, plane], window_name="Step 5: Mesh + Plane")

# Surface clipping 
# берем три вершины плоскости чтобы получить нормаль
plane_vertices = np.asarray(plane.vertices)
# возьмём три точки и вычислим нормаль
p0 = plane_vertices[0]
p1 = plane_vertices[1]
p2 = plane_vertices[2]
n = np.cross(p1 - p0, p2 - p0)
n = n / (np.linalg.norm(n) + 1e-8)

# Для "правой стороны" будем считать точки с dot((pt - p0), n) > 0 -- их удалим
pts = np.asarray(pcd.points)
dists = (pts - p0).dot(n)
mask_keep = dists <= 0  # сохраняем те, что не по правую сторону
clipped_pts = pts[mask_keep]

if pcd.has_colors():
    colors = np.asarray(pcd.colors)[mask_keep]
else:
    colors = None
if pcd.has_normals():
    normals = np.asarray(pcd.normals)[mask_keep]
else:
    normals = None

pcd_clipped = o3d.geometry.PointCloud()
pcd_clipped.points = o3d.utility.Vector3dVector(clipped_pts)
if colors is not None:
    pcd_clipped.colors = o3d.utility.Vector3dVector(colors)
if normals is not None:
    pcd_clipped.normals = o3d.utility.Vector3dVector(normals)


if len(clipped_pts) < 10:
    print("Внимание: после обрезки очень мало точек — Poisson может не сработать корректно.")
    mesh_clipped = None
else:
    # понижаем depth для скорости
    mesh_clipped, densities_clipped = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd_clipped, depth=max(6, POISSON_DEPTH-2))
    # crop по bbox обрезанного облака
    bbox2 = pcd_clipped.get_axis_aligned_bounding_box()
    mesh_clipped = mesh_clipped.crop(bbox2)
    mesh_clipped.compute_vertex_normals()

print_pcd_info("Clipped point cloud (step 6)", pcd_clipped)
if mesh_clipped is not None:
    print_mesh_info("Mesh after clipping (step 6)", mesh_clipped)
else:
    print("Mesh after clipping не построен из-за малого числа точек.")
print("обрезка по плоскости убирает часть модели; проверяем оставшиеся вершины/треугольники/цвета/нормали.")
o3d.visualization.draw_geometries([pcd_clipped], window_name="Step 6: Clipped (point cloud)")

#Color gradient and extrema
# Начнём с облака
pcd_for_color = pcd_clipped if len(pcd_clipped.points) > 0 else pcd
pts_for_color = np.asarray(pcd_for_color.points)
# убираем исходные цвета
pcd_for_color.colors = o3d.utility.Vector3dVector(np.zeros_like(pts_for_color))  

# axis
axis = 2
coords = pts_for_color[:, axis]
# нормализуем от 0 до 1
minv = coords.min()
maxv = coords.max()
if maxv - minv < 1e-9:
    normalized = np.zeros_like(coords)
else:
    normalized = (coords - minv) / (maxv - minv)
# Создадим градиент — от синего к красному: color = [r, 0, b] где r = normalized, b = 1 - normalized
colors_new = np.vstack([normalized, np.zeros_like(normalized), 1 - normalized]).T
pcd_for_color.colors = o3d.utility.Vector3dVector(colors_new)

# найти экстремумы по выбранной оси
idx_min = np.argmin(coords)
idx_max = np.argmax(coords)
pt_min = pts_for_color[idx_min]
pt_max = pts_for_color[idx_max]

print("=== Step 7: Extremes ===")
print(f"Axis chosen: {axis} (0:X,1:Y,2:Z)")
print(f"Min coord ({['X','Y','Z'][axis]}): {pt_min}")
print(f"Max coord ({['X','Y','Z'][axis]}): {pt_max}")
print()


sphere_min = o3d.geometry.TriangleMesh.create_sphere(radius=0.02 * max(bbox.get_extent()))
sphere_min.translate(pt_min)
sphere_min.paint_uniform_color([1.0, 0.8, 0.0])  # желтая
sphere_min.compute_vertex_normals()

sphere_max = o3d.geometry.TriangleMesh.create_sphere(radius=0.02 * max(bbox.get_extent()))
sphere_max.translate(pt_max)
sphere_max.paint_uniform_color([0.0, 1.0, 0.0])  # зеленая
sphere_max.compute_vertex_normals()

print("применён градиент по выбранной оси, найдены экстремумы и отмечены сферами.")
o3d.visualization.draw_geometries([pcd_for_color, sphere_min, sphere_max], window_name="Step 7: Gradient + Extremes")


if tmp_ply is not None:
    try:
        os.remove(tmp_ply.name)
    except:
        pass

print("Готово. Проверьте выводы в консоли и окна визуализации для каждого шага.")