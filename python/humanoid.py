
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from quaternion import Quaternion, vec3d, vec4d, Vec3d

# head	必須
# left/right Eye	オプション
# jaw	オプション
# hips	必須
# spine	必須
# chest	必須
# upperChest	オプション
# left/right Shoulder	オプション
# left/right UpperArm	必須
# left/right LowerArm	必須
# left/right Hand	必須
# left/right UpperLeg	必須
# left/right LowerLeg	必須
# left/right Foot	必須
# left/right Toe	オプション
# left/right Thumb Proximal, Intermediate, Distal	オプション
# left/right Index Proximal, Intermediate, Distal	オプション
# left/right Middle Proximal, Intermediate, Distal	オプション
# left/right Ring Proximal, Intermediate, Distal	オプション
# left/right Little Proximal, Intermediate, Distal

@dataclass
class Bone:
    name: str = "unknown"
    position: Vec3d = vec3d(0.0, 0.0, 0.0)
    rotation: Quaternion = Quaternion( vec4d(0.0, 0.0, 0.0, 1.0) )

@dataclass
class Finger:
    proximal: Bone = Bone()
    intermediate: Bone = Bone()
    distal: Bone = Bone()

@dataclass
class Fingers:
    thumb: Finger = Finger()
    index: Finger = Finger()
    middle: Finger = Finger()
    ring: Finger = Finger()
    little: Finger = Finger()

@dataclass
class HalfBody:
    eye: Optional[Bone] = None
    shoulder: Optional[Bone] = None
    upper_arm: Bone = Bone()
    lower_arm: Bone = Bone()
    hand: Bone = Bone()
    upper_leg: Bone = Bone()
    lower_leg: Bone = Bone()
    foot: Bone = Bone()
    toe: Optional[Bone] = None
    hand_fingers: Optional[Fingers] = Fingers()

@dataclass
class VrmHumanoid:
    head: Bone = Bone()
    jaw: Optional[Bone] = None
    neck: Bone = Bone()
    spine: Bone = Bone()
    upper_chest: Optional[Bone] = None
    chest: Bone = Bone()
    hips: Bone = Bone()
    left_body: HalfBody = HalfBody()
    right_body: HalfBody = HalfBody()

class LinkedBone:
    def __init__(self, bone: Bone):
        self.bone = bone
        self.children: list[LinkedBone] = []

    def chain(self, bone: Bone)->LinkedBone:
        child = LinkedBone(bone)
        self.children.append( child )
        return child

    def connect(self, linked_bone: LinkedBone):
        self.children.append( linked_bone )

    def connect_list(self, linked_bones: list[LinkedBone]):
        for linked_bone in linked_bones:
            self.connect(linked_bone)

    def __str__(self):
        dict = {}
        dict["name"] = self.bone.name
        dict["children"] = [ str(child) for child in self.children ]
        return str(dict)


def finger_to_linked_bone(finger: Finger)->LinkedBone:
    root = LinkedBone(finger.proximal)
    root.chain(finger.intermediate) \
        .chain(finger.distal)
    return root

def fingers_to_linked_bones(fingers: Fingers)->list[LinkedBone]:
    thumb = finger_to_linked_bone(fingers.thumb)
    index = finger_to_linked_bone(fingers.index)
    middle = finger_to_linked_bone(fingers.middle)
    ring = finger_to_linked_bone(fingers.ring)
    little = finger_to_linked_bone(fingers.little)
    return [thumb, index, middle, ring, little]

def humanoid_to_linked_bone(humanoid: VrmHumanoid) -> LinkedBone:
    root = LinkedBone(humanoid.hips)
    if humanoid.upper_chest is None:
        chest = root \
            .chain(humanoid.spine) \
            .chain(humanoid.chest)
    else:
        chest = root \
            .chain(humanoid.spine) \
            .chain(humanoid.chest) \
            .chain(humanoid.upper_chest)

    if humanoid.left_body.shoulder is None:
        left_arm = LinkedBone(humanoid.left_body.upper_arm)
    else:
        left_arm = LinkedBone(humanoid.left_body.shoulder)
        left_arm.chain(humanoid.left_body.upper_arm)

    left_fingers = fingers_to_linked_bones(humanoid.left_body.hand_fingers)

    left_arm.chain(humanoid.left_body.lower_arm) \
        .chain(humanoid.left_body.hand) \
        .connect_list(left_fingers)

    if humanoid.right_body.shoulder is None:
        right_arm = LinkedBone(humanoid.right_body.upper_arm)
    else:
        right_arm = LinkedBone(humanoid.right_body.shoulder)
        right_arm.chain(humanoid.right_body.upper_arm)

    right_fingers = fingers_to_linked_bones(humanoid.right_body.hand_fingers)

    right_arm.chain(humanoid.right_body.lower_arm) \
        .chain(humanoid.right_body.hand) \
        .connect_list(right_fingers)

    chest.connect(left_arm)
    chest.connect(right_arm)

    return root

if __name__ == "__main__":
    a = Bone()
    a.name = "a"
    root = LinkedBone(a)
    b = root.chain(a).chain(a).chain(a)
    b.chain(a)
    b.chain(a)
    print(root)

