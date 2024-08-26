import urx
import math3d as m3d
from scipy.spatial.transform import Rotation as R
import numpy as np


r = urx.URRobot("192.168.2.2", use_rt=True, urFirm=5.9)

csys_point = r.getl()
local_point = [0.1,0.1,0,0,0,0]
print(csys_point)

def euler_to_quaternion(xr, yr, zr):
    # Erstelle eine Rotation aus den Euler-Winkeln (in Radian)
    rotation = R.from_euler('xyz', [xr, yr, zr], degrees=False)
    # Konvertiere die Rotation in ein Quaternion
    quaternion = rotation.as_quat()
    return quaternion

def local_to_global(local_point, local_rotation, origin, origin_rotation):
    # Erstelle Rotationen aus den Quaternions
    local_rot = R.from_quat(local_rotation)
    origin_rot = R.from_quat(origin_rotation)
    
    # Kombiniere die Rotationen
    combined_rotation = origin_rot * local_rot
    
    # Wende die kombinierte Rotation auf den lokalen Punkt an
    rotated_point = combined_rotation.apply(local_point[:3])
    
    # Verschiebe den Punkt in das globale Koordinatensystem
    global_point = rotated_point + origin[:3]
    
    # Kombiniere die Rotationen für die Ausgabe
    global_rotation = combined_rotation.as_euler('xyz', degrees=False)
    
    return np.concatenate((global_point, global_rotation))

# Beispielwerte
local_point = local_point  # Lokale Koordinaten des Punktes (x, y, z, xr, yr, zr)
origin = csys_point       # Ursprung des lokalen Koordinatensystems (x, y, z, xr, yr, zr)

# Berechne die Quaternions aus den Euler-Winkeln
local_rotation = euler_to_quaternion(local_point[3], local_point[4], local_point[5])
origin_rotation = euler_to_quaternion(origin[3], origin[4], origin[5])

# Berechne die globalen Koordinaten des Punktes
global_point = local_to_global(local_point[:3], local_rotation, origin[:3], origin_rotation)
global_point_back = local_to_global([x * -1 for x in local_point[:3]], local_rotation, origin[:3], origin_rotation)
global_point_origin = local_to_global([x * 0 for x in local_point[:3]], local_rotation, origin[:3], origin_rotation)

print(global_point)

r.movel(global_point,0.1,0.1)
r.movel(global_point_back,0.1,0.1)
r.movel(global_point_origin,0.1,0.1)


r.close()