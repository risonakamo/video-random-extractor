"""helpers dealing with video objects"""

from cv2 import CAP_PROP_POS_MSEC,imwrite,Mat,CAP_PROP_FRAME_COUNT,CAP_PROP_FPS
from loguru import logger

from video_summarise.types.vid_extract_types import VideoCapture2

def extractFrame(video:VideoCapture2,position:float,outputFile:str)->None:
    """given a seconds position in file, extract and save as file"""

    video.set(CAP_PROP_POS_MSEC,int(position*1000))

    success:bool
    frame:Mat|None
    success,frame=video.read()

    if not success or frame is None:
        logger.error("failed to read frame")

        if not frame:
            logger.error("likely end of file")

        raise Exception("frame read death")

    imwrite(outputFile,frame)

def getVidDuration(video:VideoCapture2)->float:
    """get seconds in video"""

    frames:float=video.get(CAP_PROP_FRAME_COUNT)
    fps:float=video.get(CAP_PROP_FPS)

    duration:float=frames/fps

    return duration