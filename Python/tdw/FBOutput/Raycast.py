# automatically generated by the FlatBuffers compiler, do not modify

# namespace: FBOutput

import tdw.flatbuffers

class Raycast(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsRaycast(cls, buf, offset):
        n = tdw.flatbuffers.encode.Get(tdw.flatbuffers.packer.uoffset, buf, offset)
        x = Raycast()
        x.Init(buf, n + offset)
        return x

    # Raycast
    def Init(self, buf, pos):
        self._tab = tdw.flatbuffers.table.Table(buf, pos)

    # Raycast
    def Hit(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return bool(self._tab.Get(tdw.flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # Raycast
    def RaycastId(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Raycast
    def ObjectId(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(tdw.flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Raycast
    def Normal(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from .Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Raycast
    def Point(self):
        o = tdw.flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = o + self._tab.Pos
            from .Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def RaycastStart(builder): builder.StartObject(5)
def RaycastAddHit(builder, hit): builder.PrependBoolSlot(0, hit, 0)
def RaycastAddRaycastId(builder, raycastId): builder.PrependInt32Slot(1, raycastId, 0)
def RaycastAddObjectId(builder, objectId): builder.PrependInt32Slot(2, objectId, 0)
def RaycastAddNormal(builder, normal): builder.PrependStructSlot(3, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(normal), 0)
def RaycastAddPoint(builder, point): builder.PrependStructSlot(4, tdw.flatbuffers.number_types.UOffsetTFlags.py_type(point), 0)
def RaycastEnd(builder): return builder.EndObject()
