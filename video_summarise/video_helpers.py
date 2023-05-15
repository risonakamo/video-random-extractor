"""helpers dealing with video objects"""

from cv2 import CAP_PROP_POS_MSEC,imwrite,Mat,CAP_PROP_FRAME_COUNT,CAP_PROP_FPS

from video_summarise.types.vid_extract_types import VideoCapture2

def extractFrame(video:VideoCapture2,position:float,outputFile:str)->None:
    """given a seconds position in file, extract and save as file"""

    video.set(CAP_PROP_POS_MSEC,int(position*1000))

    success:bool
    frame:Mat
    success,frame=video.read()

    if not success:
        raise Exception("died")

    imwrite(outputFile,frame)

def getVidDuration(video:VideoCapture2)->float:
    """get seconds in video"""

    frames:float=video.get(CAP_PROP_FRAME_COUNT)
    fps:float=video.get(CAP_PROP_FPS)

    duration:float=frames/fps

    return duration