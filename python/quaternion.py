
from __future__ import annotations
from dataclasses import dataclass

import numpy as np
from nptyping import NDArray, Shape, Float

Vec3d = NDArray[Shape["1,3"], Float]
Vec4d = NDArray[Shape["1,4"], Float]
Matrix4d = NDArray[Shape["4,4"], Float]

def vec3d(x: float, y: float, z: float) -> Vec3d:
    return np.array([x, y, z])

def vec4d(x: float, y: float, z: float, w: float) -> Vec4d:
    return np.array([x, y, z, w])

@dataclass
class Quaternion:
    q_vec: Vec4d

    def __add__(self, other: Quaternion)->Quaternion:
        return Quaternion(self.q_vec + other.q_vec)

    def __mul__(self, other: Quaternion)->Quaternion:
        rot_array: Matrix4d = self.rotate_matrix()
        q: Vec4d = np.dot( rot_array, other.q_vec)
        return Quaternion(q)

    def __str__(self):
        return f"Quaternion({self.q_vec})"

    def image(self)->Vec3d:
        return self.q_vec[:3]

    def real(self)->float:
        return self.q_vec[3]

    def rotate_matrix(self)->Matrix4d:
        return np.array([
            [self.q_vec[3], -self.q_vec[2], self.q_vec[1], self.q_vec[0]]
            ,[self.q_vec[2], self.q_vec[3], -self.q_vec[0], self.q_vec[1]]
            ,[-self.q_vec[1], self.q_vec[0], self.q_vec[3], self.q_vec[2]]
            ,[-self.q_vec[0], -self.q_vec[1], -self.q_vec[2], self.q_vec[3]]
            ])

    def rotate(self, vec: Vec3d)->Vec3d:
        q = self * Quaternion(vec4d(vec[0], vec[1], vec[2], 0.0))
        return q.q_vec[:3]
