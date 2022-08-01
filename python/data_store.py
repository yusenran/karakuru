

from collections import deque
from threading import Event
import time
from typing import Deque, Optional

from humanoid import VrmHumanoid, Bone, HalfBody, Finger


BoneDict = dict[str, Bone]

def set_bone_to_finger( finger: Finger, name: str, bone: Bone )->Finger:
    if name == "Proximal":
        finger.proximal = bone
    elif name == "Intermediate":
        finger.intermediate = bone
    elif name == "Distal":
        finger.distal = bone
    return finger

def set_bone_to_half_body( half_body: HalfBody, name: str, bone: Bone )->HalfBody:
    if name.startswith("Thumb"):
        name = name.removeprefix("Thumb")
        half_body.hand_fingers.thumb = set_bone_to_finger( half_body.hand_fingers.thumb, name, bone )
    elif name.startswith("Index"):
        name = name.removeprefix("Index")
        half_body.hand_fingers.index = set_bone_to_finger( half_body.hand_fingers.index, name, bone )
    elif name.startswith("Middle"):
        name = name.removeprefix("Middle")
        half_body.hand_fingers.middle = set_bone_to_finger( half_body.hand_fingers.middle, name, bone )
    elif name.startswith("Ring"):
        name = name.removeprefix("Ring")
        half_body.hand_fingers.ring = set_bone_to_finger( half_body.hand_fingers.ring, name, bone )
    elif name.startswith("Little"):
        name = name.removeprefix("Little")
        half_body.hand_fingers.little = set_bone_to_finger( half_body.hand_fingers.little, name, bone )
    elif name == "Eye":
        half_body.eye = bone
    elif name == "Shoulder":
        half_body.shoulder = bone
    elif name == "UpperArm":
        half_body.upper_arm = bone
    elif name == "LowerArm":
        half_body.lower_arm = bone
    elif name == "Hand":
        half_body.hand = bone
    elif name == "UpperLeg":
        half_body.upper_leg = bone
    elif name == "LowerLeg":
        half_body.lower_leg = bone
    elif name == "Foot":
        half_body.foot = bone
    elif name == "Toe":
        half_body.toe = bone
    else:
        print( "unknown bone name:{}".format(name) )
    return half_body

def set_bone_to_humanoid( humanoid: VrmHumanoid, name: str, bone: Bone)->VrmHumanoid:
    if name.startswith("Left"):
        name = name.removeprefix("Left")
        humanoid.left_body = set_bone_to_half_body( humanoid.left_body, name, bone )
    elif name.startswith("Right"):
        name = name.removeprefix("Right")
        humanoid.right_body = set_bone_to_half_body( humanoid.right_body, name, bone )
    elif name == "Head":
        humanoid.head = bone
    elif name == "Neck":
        humanoid.neck = bone
    elif name == "Spine":
        humanoid.spine = bone
    elif name == "UpperChest":
        humanoid.upper_chest = bone
    elif name == "Chest":
        humanoid.chest = bone
    elif name == "Hips":
        humanoid.hips = bone
    else:
        print( "unknown bone name:{}".format(name) )
    return humanoid

def gen_humanoid( humanoid: VrmHumanoid, bone_dict: BoneDict)->VrmHumanoid:
    for name, bone in bone_dict.items():
        humanoid = set_bone_to_humanoid( humanoid, name, bone )
    return humanoid

class DataStore:
    bone_dict: BoneDict = {}
    bone_dict_queue: Deque[BoneDict] = deque([])
    humanoid_queue: Deque[VrmHumanoid] = deque([])

    def __init__(self):
        pass

    @classmethod
    def push( cls, bone_name: str, bone: Bone, new: bool):
        if new:
            cls.bone_dict_queue.append(cls.bone_dict)
            cls.bone_dict = {}
            cls.bone_dict[bone_name] = bone
        else:
            cls.bone_dict[bone_name] = bone

    @classmethod
    def extract(cls, exiting: Event):
        try:
            humanoid = VrmHumanoid()
            fps = 60.0
            interval = 1.0 / fps
            count = 0
            while not exiting.is_set():
                if cls.bone_dict_queue:
                    # print("extract")
                    bone_dict = cls.bone_dict_queue.popleft()
                    humanoid = gen_humanoid( humanoid, bone_dict)
                    cls.humanoid_queue.append(humanoid)
                    count += 1
                    if count > 60:
                        count = 0
                        # print(f"[head]: {humanoid.head}")
                        # print(f"[leftlittledistal]: {humanoid.left_body.hand_fingers.little.distal}")
                time.sleep(interval)
        except Exception as e:
            print(e)
            raise e
        print("extract end")

    @classmethod
    def pop(cls)->Optional[VrmHumanoid]:
        if cls.humanoid_queue:
            return cls.humanoid_queue.popleft()
        return None

