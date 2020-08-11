
# date: 2020/07/11
# extractPointCloud.extractionPoints()より点群情報を受け取り
# point cloudを書き出す・可視化するコード

from alfred.vis.pointcloud.pointcloud_vis import draw_pcs_open3d
from alfred.fusion.common import draw_3d_box, compute_3d_box_lidar_coords
from alfred.fusion.kitti_fusion import load_pc_from_file

import open3d as o3d
import numpy as np
import extractPointCloud


#data = np.random.rand(10,3)
# 点群データ(np.array())を取得する
data, data_cam,data_w, center = extractPointCloud.extractPoints()

"""
array_bed = []
with open('/Users/matsunagamasaaki/bed_0219.txt', 'r') as f:
    line=f.readlines()

for i in line:
    result = []
    elem = i.strip('\n').split(' ')
    for e in elem:
        result.append(float(e))
    array_bed.append(result)
array_bed = np.array(array_bed)
print(data_w)
print(array_bed)
"""
print(data)
geometries = []

pointcloud = o3d.PointCloud()
pointcloud.points = o3d.Vector3dVector(data)

pointcloud_ = o3d.PointCloud()
pointcloud_.points = o3d.Vector3dVector(data_cam)


pointcloud_center = o3d.PointCloud()
pointcloud_center.points = o3d.Vector3dVector(center)

#print(np.shape(array_bed), np.shape(data_w), type(array_bed), type(data_w)) 
pointcloud_w = o3d.PointCloud()
pointcloud_w.points = o3d.Vector3dVector(data_w)



# 点群にそれぞれ色をつける
pointcloud_.paint_uniform_color([255,0,0])
pointcloud.paint_uniform_color([0, 0.651, 0.929])
pointcloud_w.paint_uniform_color([0, 0, 0])
pointcloud_center.paint_uniform_color([0,255,0])



#　点群をまとめる
geometries.append(pointcloud)
geometries.append(pointcloud_)
geometries.append(pointcloud_w)
geometries.append(pointcloud_center)




# 3dBoundingBoxの定義
box = [4.481686, 5.147319, -1.0229858, 0.3728549, 0.46751, 0.5121397, 1.5486346]
box_bottle = [-0.2, 0, -0.1229858, 0.3728549, 0.146751, 0.1121397, 1.5486346]
box_camera = [-0.2, 0, -0.1229858, 0.0128549,  0.016751, 0.0121397, 30]

xyz = np.array(center[-1])#np.array([box[: 3]])
xyz_b = np.array([box_bottle[:3]])


print('center',np.shape(center), np.shape(np.array([box[:3]])))
print(center)

# PC用
hwl = np.array([box[3: 6]])
r_y = [box[6]]
pts3d = compute_3d_box_lidar_coords(xyz, hwl, angles=r_y, origin=(0.5,0.5,0.5), axis=2)

# ペットボトル用
hwl = np.array([box_bottle[3: 6]])
r_y = [box[6]]
pts3d_bottle =  compute_3d_box_lidar_coords(xyz+xyz_b, hwl, angles=r_y, origin=(0.5,0.5,0.5), axis=2)


# for pc and bottle
lines = [[0,1],[1,2],[2,3],[3,0],
             [4,5],[5,6],[6,7],[7,4],
             [0,4],[1,5],[2,6],[3,7]]

# for camera
lines_camera =  [[0,1], [1,2], [2,3],[3,0]]

#pc
colors = [[1, 0, 1] for i in range(len(lines))]
line_set = o3d.geometry.LineSet()
line_set.points = o3d.utility.Vector3dVector(pts3d[0])
line_set.lines = o3d.utility.Vector2iVector(lines)
line_set.colors = o3d.utility.Vector3dVector(colors)


#bottle
colors = [[10, 10, 1] for i in range(len(lines))]
line_set_ = o3d.geometry.LineSet()
line_set_.points = o3d.utility.Vector3dVector(pts3d_bottle[0])
line_set_.lines = o3d.utility.Vector2iVector(lines)
line_set_.colors = o3d.utility.Vector3dVector(colors)


for i in data_cam:
    xyz_cam = np.array(i)
    
    # ペットボトル用
    hwl = np.array([box_camera[3: 6]])
    r_y = [box_camera[6]]
    pts3d_ =  compute_3d_box_lidar_coords(xyz_cam, hwl, angles=r_y, origin=(0.5,0.5,0.5), axis=2)

    # camera
    colors = [[255,0,0] for i in range(len(lines_camera))]
    line_set_c = o3d.geometry.LineSet()
    line_set_c.points = o3d.utility.Vector3dVector(pts3d_[0])
    line_set_c.lines = o3d.utility.Vector2iVector(lines_camera)
    line_set_c.colors = o3d.utility.Vector3dVector(colors)
    geometries.append(line_set_c)



#geometries.append(line_set)
#geometries.append(line_set_)


# 純正open3d用
#o3d.draw_geometries([pointcloud, pointcloud_, pointcloud_w, pointcloud_center])

# alfredopen3d用
draw_pcs_open3d(geometries)

# 点群書き出し用
#o3d.write_point_cloud("output.pcd", geometries)




