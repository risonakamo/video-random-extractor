from cv2 import VideoCapture,CAP_PROP_POS_MSEC,imwrite,Mat,CAP_PROP_FRAME_COUNT,CAP_PROP_FPS
from devtools import debug
import devtools
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
    DESIRED_SEGMENTS:int=100
    MAX_DEVIATION:int=15
    JITTER:float=2.5
    OUTPUT_DIR:str=join(HERE,"output3")
    DRY_RUN:bool=False
    MIN_SEGMENTS:int=60
    MAX_SEGMENTS:int=500

    makedirs(OUTPUT_DIR,exist_ok=True)

    vidFile:VideoCapture2=VideoCapture("test.webm")
    duration:float=getVidDuration(vidFile)

    logger.info("output dir: {}",OUTPUT_DIR)
    logger.info("target number of output images: {}",DESIRED_SEGMENTS)
    logger.info("interval jitter: {}s",JITTER)
    logger.info("video duration: {}s",duration)

    debug("desired avg",duration/DESIRED_SEGMENTS)

    # randomisationRange:DesiredIntervalTime=intervalTimeCalc2(
    #     desiredSegments=DESIRED_SEGMENTS,
    #     segmentDeviation=MAX_DEVIATION,
    #     maxTime=duration
    # )

    randomisationRange:DesiredIntervalTime=intervalCalc3(
        minSegments=MIN_SEGMENTS,
        maxSegments=MAX_SEGMENTS,
        maxTime=duration
    )

    logger.info("average capture interval: {}s",randomisationRange.averageTime)

    debug(randomisationRange)
    segments:list[float]=segmentTimeRandom(
        randomIntervalRange=randomisationRange.interval,
        maxTime=duration
    )

    logger.info("actual number of output images: {}",len(segments))

    if not DRY_RUN:
        for i,time in enumerate(segments):
            i:int
            time:float

            logger.info("extracting {}/{} @ {}s",
                i+1,
                len(segments),
                time
            )
            extractFrame(
                vidFile,
                time,
                join(OUTPUT_DIR,f"{i+1}.jpg")
            )

    logger.info("complete")
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

    debug(timeRangeMs)

    times:list[float]=[]
    currTime:int=0
    maxTimeMs:int=int(maxTime*1000)

    while True:
        currTime+=randint(timeRangeMs[0],timeRangeMs[1])

        if currTime>=maxTimeMs:
            return times

        times.append(currTime/1000)

def intervalTimeCalc1(
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

def intervalTimeCalc2(
    desiredSegments:int,
    segmentDeviation:int,
    maxTime:float
)->DesiredIntervalTime:
    """calculate interval range based on desired number of segments and a segment deviation. segment
    deviation is how much the final amount of segments can be.

    ex:
    desired: 100 segments
    deviation: 50 segments
    possible range of segments created: 50-150

    max time should be in seconds. output range values are all in seconds"""

    minSegments:int=desiredSegments-segmentDeviation
    maxSegments:int=desiredSegments+segmentDeviation

    if minSegments<=0:
        logger.error("min segments cannot be below 0")
        raise Exception("min segments error")

    return intervalCalc3(
        minSegments=minSegments,
        maxSegments=maxSegments,
        maxTime=maxTime
    )

def intervalCalc3(
    minSegments:int,
    maxSegments:int,
    maxTime:float
)->DesiredIntervalTime:
    """calculate interval range based on min and max desired number of segments"""

    minIntervalTime:float=maxTime/minSegments
    maxIntervalTime:float=maxTime/maxSegments

    avgTime:float=(minIntervalTime+maxIntervalTime)/2

    return DesiredIntervalTime(
        averageTime=avgTime,
        interval=(
            # flipped because min time makes the higher value
            maxIntervalTime,
            minIntervalTime
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