import typing
from dataclasses import dataclass



def _unpack_convert(v, t=typing.Any):
    if v == "_":
        return None
    elif v in ["T", "F"]:
        return True if v == "T" else False
    else:
        try:
            n = int(v)
            return n
        except ValueError:
            pass
        
        try:
            n = float(v)
            return n
        except ValueError:
            pass
        
        return str(v)


def _pack_convert(v):
    if isinstance(v, bool):
        return "T" if v else "F"
    elif v is None:
        return "_"
    else:
        return str(v)


@dataclass(
        slots=True,
)
class CallBackData:
    """
    example:
    citychoice/msk/F#DFSFSDHBSEDFSDSDFSD/4
    citychoice/spb/F#DFSFSDHBSEDFSDSDFSD/4
    citychoice/complete/F#DFSFSDHBSEDFSDSDFSD/4
    """
    
    msg_type: str | None = None
    btn_id: str | None = None
    value: typing.Any | None = None
    version: int | None = 1
    
    
    @staticmethod
    def from_str(cbd: str):
        return CallBackData().unpack(cbd)
    
    
    def unpack(self, cbd: str):
        l = cbd.split("/")
        l = list(map(_unpack_convert, l))
        self.msg_type, self.btn_id, self.value, self.version = l
        return self
    
    
    def pack(self):
        target = [self.msg_type, self.btn_id, self.value, self.version]
        target = [_pack_convert(v) for v in target]
        res = "/".join(target)
        
        assert len(res) <= 64
        return res
