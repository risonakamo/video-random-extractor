from cv2 import VideoCapture
from rich import print as printr,pretty
from loguru import logger
from os.path import join,dirname,realpath
from os import makedirs

from video_summarise.types.vid_extract_types import VideoCapture2,DesiredIntervalTime
from video_summarise.interval_calc import intervalCalc3
from video_summarise.video_helpers import extractFrame,getVidDuration
from video_summarise.segmenter import segmentTimeRandom

pretty.install()

@logger.catch()
def main():
    HERE:str=dirname(realpath(__file__))
    OUTPUT_DIR:str=join(HERE,"output3")
    DRY_RUN:bool=False
    MIN_SEGMENTS:int=30
    MAX_SEGMENTS:int=50

    vidFile:VideoCapture2=VideoCapture("test.webm")
    duration:float=getVidDuration(vidFile)

    printr("[cyan]INFORMATION:[/cyan]")
    printr("requested number of target images: [yellow]{}-{}[/yellow]".format(MIN_SEGMENTS,MAX_SEGMENTS))
    printr("video duration: [yellow]{}[/yellow]s".format(duration))

    randomisationRange:DesiredIntervalTime=intervalCalc3(
        minSegments=MIN_SEGMENTS,
        maxSegments=MAX_SEGMENTS,
        maxTime=duration
    )

    printr("average screenshot interval: {}s".format(randomisationRange.averageTime))

    segments:list[float]=segmentTimeRandom(
        randomIntervalRange=randomisationRange.interval,
        maxTime=duration
    )

    printr("pending output images: [yellow]{}[/yellow]".format(len(segments)))
    printr(f"output dir: [green]{OUTPUT_DIR}[/green]")

    printr()
    printr("will create [yellow]{}[/yellow] images. proceed?".format(len(segments)))
    printr("y: proceed")
    printr("n: cancel")
    printr("s: reshuffle")

    userInput:str=input(">")

    match userInput:
        case "n":
            printr("[red]quitting[/red]")
            exit()
        case "y":
            pass
        case other:
            printr("[red]invalid choice, quitting[/red]")
            exit()

    makedirs(OUTPUT_DIR,exist_ok=True)

    if not DRY_RUN:
        for i,time in enumerate(segments):
            i:int
            time:float

            printr("extracting {}/{} @ {}s".format(
                i+1,
                len(segments),
                time
            ))
            extractFrame(
                vidFile,
                time,
                join(OUTPUT_DIR,f"{i+1}.jpg")
            )

    printr("[green]complete[/green]")
    vidFile.release()

if __name__=="__main__":
    main()