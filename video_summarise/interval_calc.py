"""functions for calculating desired interval time"""

from loguru import logger

from video_summarise.types.vid_extract_types import DesiredIntervalTime

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