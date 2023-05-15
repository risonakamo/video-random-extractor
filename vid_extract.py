from cv2 import VideoCapture,CAP_PROP_POS_MSEC,imwrite,Mat,CAP_PROP_FRAME_COUNT,CAP_PROP_FPS
from devtools import debug
from loguru import logger
from random import randint
from pydantic import BaseModel
from os.path import join,dirname,realpath
from os import makedirs

from typing import Any, TypeAlias,TypeVar

T=TypeVar("T")
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

@logger.catch()
def main():
    HERE:str=dirname(realpath(__file__))
    DESIRED_SEGMENTS:int=30
    JITTER:float=2.5
    OUTPUT_DIR:str=join(HERE,"output")

    makedirs(OUTPUT_DIR,exist_ok=True)

    logger.info("output dir: {}",OUTPUT_DIR)
    logger.info("target number of output images: {}",DESIRED_SEGMENTS)
    logger.info("interval jitter: {}s",JITTER)

    vidFile:VideoCapture2=VideoCapture("test.webm")

    duration:float=getVidDuration(vidFile)
    logger.info("video duration: {}s",duration)

    randomisationRange:DesiredIntervalTime=calcIntervalRangeFromDesiredSegments(
        desiredSegments=DESIRED_SEGMENTS,
        maxTime=duration,
        jitter=JITTER
    )

    logger.info("average capture interval: {}s",randomisationRange.averageTime)

    segments:list[float]=segmentTimeRandom(
        randomIntervalRange=randomisationRange.interval,
        maxTime=duration
    )

    logger.info("actual number of output images: {}",len(segments))
    # debug(segments)

    for i,time in enumerate(segments):
        i:int
        time:float

        logger.info("extracting {}/{} @ {}s",i,len(segments),time)
        extractFrame(
            vidFile,
            time,
            join(OUTPUT_DIR,f"{i+1}.jpg")
        )

    vidFile.release()

def getVidDuration(video:VideoCapture2)->float:
    """get seconds in video"""

    frames:float=video.get(CAP_PROP_FRAME_COUNT)
    fps:float=video.get(CAP_PROP_FPS)

    duration:float=frames/fps

    return duration

def segmentTimeRandom(randomIntervalRange:TimeIntervalRange,maxTime:float)->list[float]:
    """given a maximum value, generate random points up to that value at a random intervals.
    time range and maxvalue should be in seconds. output times are also in seconds"""

    timeRangeMs:TimeIntervalRangeMs=(
        int(randomIntervalRange[0]*1000),
        int(randomIntervalRange[1]*1000)
    )

    times:list[float]=[]
    currTime:int=0
    maxTimeMs:int=int(maxTime*1000)

    while True:
        currTime+=randint(timeRangeMs[0],timeRangeMs[1])

        if currTime>=maxTimeMs:
            return times

        times.append(currTime/1000)

def calcIntervalRangeFromDesiredSegments(
    desiredSegments:int,
    maxTime:float,
    jitter:float
)->DesiredIntervalTime:
    """based on a user's desired amount of segments and jitter, compute a time interval range
    that is likely to get the number of segments. higher jitter means more chance it will
    not hit the desired range.

    - maxTime: seconds
    - jitter: seconds
    - output interval: seconds"""

    averageIntervalTime:float=maxTime/desiredSegments

    return DesiredIntervalTime(
        averageTime=averageIntervalTime,
        interval=(
            averageIntervalTime-jitter,
            averageIntervalTime+jitter
        )
    )

def extractFrame(video:VideoCapture2,position:float,outputFile:str)->None:
    """given a seconds position in file, extract and save as file"""

    video.set(CAP_PROP_POS_MSEC,int(position*1000))

    success:bool
    frame:Mat
    success,frame=video.read()

    if not success:
        raise Exception("died")

    imwrite(outputFile,frame)

if __name__=="__main__":
    main()