"""functions dealing in segmenting time"""

from random import randint

from video_summarise.types.vid_extract_types import TimeIntervalRange,TimeIntervalRangeMs

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