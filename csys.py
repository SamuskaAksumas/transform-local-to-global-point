from scipy.spatial.transform import Rotation as R
import numpy as np

def euler_to_quaternion(xr, yr, zr, degree=False):
    '''
    Input:
    Rotation-Angles: xr,yr,zr
    degree: Bool-Type, is in degree

    Converts Euler-Angles into Quaternion-Angles
    '''

    # create the rotation from euler angles
    rotation = R.from_euler('xyz', [xr, yr, zr], degrees=degree)

    # convert rotations into quaternions
    quaternion = rotation.as_quat()

    return quaternion

def local_to_global(local_point, origin_point, degree=False):
    '''
    Input:
    Local-Point: Point in Local-Coordinatesystem (in Shape X,Y,Z,XR,YR,ZR).
    Simply type in 0 for Rs if there is no rotation
    Origin-Point: Origin-Point of Local-Coordinatesystem, same Shape as Local-Point
    degree: Bool-Type, is in degree

    Converts Local_Point in Local-Coordinatesystem into Global-Point
    '''

    # create rotations from quaternions
    local_rot = R.from_quat(euler_to_quaternion(local_point[3],local_point[4],local_point[5]))
    origin_rot = R.from_quat(euler_to_quaternion(origin_point[3],origin_point[4], origin_point[5]))
    
    # combine rotations
    combined_rotation = origin_rot * local_rot
    
    # apply combined rotations of local-point
    rotated_point = combined_rotation.apply(local_point[:3])
    
    # tranlate point to global-coordinatesysten
    global_point = rotated_point + origin_point[:3]
    
    # combine rotations for global-point
    global_rotation = combined_rotation.as_euler('xyz', degrees=degree)
    
    return np.concatenate((global_point, global_rotation))


if __name__ == '__main__':
    
    # example

    local_point = [10,0,0,0,0,0]
    # local coordinates of local point (x, y, z, xr, yr, zr)
    print('Local-Point:')
    print(local_point, '\n')

    origin_point = [50,100,0,np.radians(180),0,0]
    # origin of local-coordinatesystem (x, y, z, xr, yr, zr)
    print('Origin of Local-Coordinatesystem:')
    print(origin_point, '\n')

    # calculate global_point with global coordinates
    global_point = local_to_global(local_point, origin_point)
    print('Global-Point:')
    print(global_point)

