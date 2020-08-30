

from alfred.vis.pointcloud.pointcloud_vis import draw_pcs_open3d
from alfred.fusion.common import draw_3d_box, compute_3d_box_lidar_coords
from alfred.fusion.kitti_fusion import load_pc_from_file

import open3d as o3d
import numpy as np
from extractPointCloud import  Extractor
import time


data, data_cam,data_w, center, new_list, new_list_camera, final_frustum, camera_angle = Extractor('generator').extractPoints()

print(len(data),len(data_cam), len(data_w),len(center), len(final_frustum))
print(final_frustum)


#geo=[]
#for i in range(len(new_list)):
#    pointcloud = o3d.PointCloud()
#    pointcloud.points = o3d.Vector3dVector(new_list[i])
#    pointcloud.paint_uniform_color([0, 0.651, 0.929])
#    geo.append(pointcloud)


geometry = o3d.geometry.PointCloud()
#geometry.points = o3d.utility.Vector3dVector(new_list[0])
geometry_camera = o3d.geometry.PointCloud()
geometry_center = o3d.geometry.PointCloud()
#geometry_line = o3d.geometry.PointCloud()
geometry_camera_angle = o3d.geometry.PointCloud()


# Animation
vis = o3d.visualization.Visualizer()
vis.create_window()
opt = vis.get_render_option()
opt.point_size = 6.0

line_set_ = o3d.geometry.LineSet() # for drawing object center
line_set = o3d.geometry.LineSet() # for drawing camera angle

while True:
    for i in range(len(new_list)):

        # point cloud 
        if i == 0:
            new_ = np.array(new_list[i], dtype=np.float64)
            new_l = np.array(new_list_camera, dtype=np.float64)[i]
            cameraAngle = np.array(camera_angle, dtype=np.float64)[i]
        else:
            new_ = np.concatenate([new_,np.array(new_list[i], dtype=np.float64)],axis=0)
            new_l = np.concatenate([new_l, np.array(new_list_camera, dtype=np.float64)[i]],axis=0)
            cameraAngle = np.concatenate([cameraAngle, np.array(cameraAngle, dtype=np.float64)[i], axis=0)
        
#        new_l = np.array(new_list_camera, dtype=np.float64)[i]

        camera_position = np.array([float(np.mean(new_l[:,0])),float(np.mean(new_l[:,1])),float(np.mean(new_l[:,2]))], dtype=np.float64)
        center = np.array([float(np.mean(new_[:,0])), float(np.mean(new_[:,1])), float(np.mean(new_[:,2]))], dtype=np.float64) # object center
        cameraAngle_ = np.array([float(np.mean(cameraAngle[:,0])), float(np.mean(cameraAngle[:,1])), float(np.mean(cameraAngle[:,2]))],dtype=np.float64)

        print('distance', np.linalg.norm(camera_position-center))


        # create geometries
        geometry.points = o3d.utility.Vector3dVector(new_)
        geometry_camera.points = o3d.utility.Vector3dVector(new_l)
        geometry_center.points = o3d.utility.Vector3dVector([center])
        geometry_camera_angle.points = o3d.utility.Vector3dVector(cameraAngle_)

        # paint color
        geometry.paint_uniform_color([0, 0.651, 0.929])
        geometry_camera.paint_uniform_color([1,0,0])
        geometry_center.paint_uniform_color([1,0,0])
        geometry_camera_angle.paint_uniform_color([0,1,0])

        
        # draw lines 
        lines=[[0,1]]
        lines_angle = [[1,2],[2,3],[3,4],[4,1],[0,0],
                        [0,1],[0,2],[0,3],[0,4]]

        box = np.array([-0.05,-0.05,0],dtype=np.float64)#left-down
        box2 = np.array([0.05,-0.05,0],dtype=np.float64)#right-down
        box3 = np.array([0.05,0.05,0],dtype=np.float64)#right-top
        box4 = np.array([-0.05,0.05,0],dtype=np.float64)#left-top
        angle_position = [center+box,center+box2,center+box3, center+box4
            ,camera_position]
     
        # draw object center line 
        colors = [[1,0, 0] for i in range(len(lines))]
        line_set_.points = o3d.utility.Vector3dVector([camera_position, center])
        line_set_.lines = o3d.utility.Vector2iVector(lines)
        line_set_.colors = o3d.utility.Vector3dVector(colors)

        # draw camera angle line 
        colors = [[1,0, 0] for i in range(len(lines_angle))]
        line_set.points = o3d.utility.Vector3dVector(angle_position)
        line_set.lines = o3d.utility.Vector2iVector(lines_angle)
        line_set.colors = o3d.utility.Vector3dVector(colors)
        
        
        #geometry_line.points = line_set_
        if i == 0:
            vis.add_geometry(geometry)
            vis.add_geometry(geometry_camera)
            vis.add_geometry(geometry_center)
            vis.add_geometry(geometry_camera_angle)
            vis.add_geometry(line_set_)
            vis.add_geometry(line_set)
        else:
            vis.update_geometry(geometry)
            vis.update_geometry(geometry_camera)
            vis.update_geometry(geometry_center)
            vis.update_geometry(geometry_camera_angle)
            vis.update_geometry(line_set_)
            vis.update_geometry(line_set)

        vis.poll_events()
        vis.update_renderer()
        #ytime.sleep(1)
vis.destroy_window()


    
#from open3d.open3d.geometry import voxel_down_sample
#source_raw = o3d.io.read_point_cloud("./output.pcd")
#source = voxel_down_sample(source_raw,voxel_size=0.02)
#print(type(source))







    
