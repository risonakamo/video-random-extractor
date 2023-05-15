from cv2 import Mat

from pydantic import BaseModel
from typing import Any, TypeAlias,TypeVar

class VideoCapture2:
    def set(self,prop:int,value:Any)->None:
        ...

    def get(self,prop:int)->Any:
        ...

    def read(self)->tuple[bool,Mat]:
        ...

    def release(self)->None:
        ...

TimeIntervalRange:TypeAlias=tuple[float,float]
"""a time duration random. float seconds time"""

TimeIntervalRangeMs:TypeAlias=tuple[int,int]

class DesiredIntervalTime(BaseModel):
    averageTime:float
    interval:TimeIntervalRange