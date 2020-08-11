import matplotlib.pyplot as plt
import numpy as np




def extractPoints():
    # from xcode data to preprocessed data
    with open('tmp.txt', 'r') as f:
        lines=f.readlines()

    data=[] 
    feature=[]
    world=[]
    for i in lines:   
        li=i.split(' ')
        if li[0] == 'thissss':
            new=i.strip('thissss SIMD3<Float>').strip('\n').strip('(').strip(')').split(',')
            data_=[]
            try:
                for i in new:
                    data_.append(float(i))
            except ValueError:
                pass
            data.append(data_)

        if li[0] == 'point':
            new=i.strip('point SIMD3<Float>').strip('\n').strip('(').strip(')').split(',')
            print(new)
            data_f=[]
            try:
                for i in new:
                    data_f.append(float(i))
            except ValueError:
                pass
            feature.append(data_f)


        if li[0] == 'world':
            new=i.strip('world SIMD3<Float>').strip('\n').strip('(').strip(')').split(',')
            print('hshs',new)
            data_=[]
            try:
                for i in new:
                    data_.append(float(i))
            except ValueError:
                pass
            world.append(data_)

        
        if li[0] == 'flo':
            new=i.strip('aaaaaaa simd_float4x4').strip('\n').strip('(').strip(')').split(',')
            data_=[]
            try:
                for i in new:
                    data_.append(float(i))
            except ValueError:
                pass
            data.append(data_)

    print(len(feature), len(data))      


    x=[]
    y=[]
    z=[]

    for i in data:
    #    print(i)
        try:
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])
        except IndexError:
            pass

    x_f=[]
    y_f=[]
    z_f=[]
    for i in feature:
    #    print(i)
        try:
            x_f.append(i[0])
            y_f.append(i[1])
            z_f.append(i[2])
        except IndexError:
            pass


    x_w=[]
    y_w=[]
    z_w=[]
    for i in world:
    #    print(i)
        try:
            x_w.append(i[0])
            y_w.append(i[1])
            z_w.append(i[2])
        except IndexError:
            pass

    print('tssssssssssssssssssssssssssssss')
    array=[]
    aggregate_points=[]
    center = []

    """
    for i,d,e in zip(x_f,y_f,z_f):
        array.append([i,d,e])

        tmp_array= np.array(array)
        element = [float(np.mean(tmp_array[:][:,0])), float(np.mean(tmp_array[:][:,1])), float(np.mean(tmp_array[:][:,2]))]
        if len(element) !=0:
            center.append(element)
        else:
            pass
    """
        
    print('ssssssssssssssssssssssssssssssssssss')
    array = np.array(feature, dtype=np.float64)#array, dtype=np.float64)
    
    center = np.array(feature, dtype=np.float64)#center, dtype=np.float64)

    array_cam=[]
    """    
    for i,d,e in zip(x,y,z):
        array_cam.append([i,d,e])
    """
    array_cam = np.array(data, dtype=np.float64)#array_cam, dtype=np.float64)



    array_w=[]
    """    
    for i,d,e in zip(x_w,y_w,z_w):
        array_w.append([i,d,e])
    """
    array_w = np.array(world, dtype=np.float64)#array_w, dtype=np.float64)


    print(np.shape(center),np.shape(array))
#    print(np.linalg.norm(array_cam.tolist()[0][-1], center.tolist()[0][-1]))
#
    return array,array_cam, array_w, center




if __name__=='__main__':
    extractPoints()
