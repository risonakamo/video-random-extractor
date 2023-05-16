from genericpath import isfile
from uuid import uuid4
from cv2 import VideoCapture
from devtools import debug
from rich import print as printr,pretty
from loguru import logger
from os.path import join,realpath,isdir
from os import makedirs

from video_summarise.types.vid_extract_types import VideoCapture2,DesiredIntervalTime
from video_summarise.interval_calc import intervalCalc3
from video_summarise.video_helpers import extractFrame,getVidDuration
from video_summarise.segmenter import segmentTimeRandom
from video_summarise.args import VidExtractArgs, getArgs

pretty.install()

@logger.catch()
def main():
    args:VidExtractArgs=getArgs()
    args.outputDir=realpath(args.outputDir)

    namehash:str=uuid4().hex[:6]

    # opening the file
    if not isfile(args.videoFile):
        printr("[red]could not find target video file[/red]")
        exit()

    vidFile:VideoCapture2=VideoCapture(args.videoFile)
    duration:float=getVidDuration(vidFile)

    # calculating the interval increment range
    randomisationRange:DesiredIntervalTime=intervalCalc3(
        minSegments=args.minSegments,
        maxSegments=args.maxSegments,
        maxTime=duration
    )

    # calculating the extraction segments
    segments:list[float]=segmentTimeRandom(
        randomIntervalRange=randomisationRange.interval,
        maxTime=duration,
        shuffle=args.shuffle
    )

    # printing out information
    printr("[cyan]INFORMATION:[/cyan]")
    printr("requested number of target images: [yellow]{}-{}[/yellow]".format(
        args.minSegments,
        args.maxSegments
    ))
    printr("video duration: [yellow]{:.2f}[/yellow]s".format(duration))

    printr("average screenshot interval: [magenta]{:.2f}[/magenta]s".format(randomisationRange.averageTime))
    printr("screenshot interval range: [magenta]{:.2f}[/magenta]~[magenta]{:.2f}[/magenta]s".format(
        randomisationRange.interval[0],
        randomisationRange.interval[1]
    ))
    printr("shuffling: {}".format(args.shuffle))
    printr("output hash: [cyan]{}[/cyan]".format(namehash))

    printr("pending output images: [bright_yellow]{}[/bright_yellow]".format(len(segments)))
    printr(f"output dir: [green]{args.outputDir}[/green]")

    printr()
    printr("will create [bright_yellow]{}[/bright_yellow] images. proceed?".format(len(segments)))
    printr("y: proceed")
    printr("n: cancel")
    printr("s: reshuffle")

    # handling confirmation
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

    # ensuring output location
    makedirs(args.outputDir,exist_ok=True)

    # executing generation
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
            join(args.outputDir,f"{namehash}-{i+1}.jpg")
        )

    printr("[green]complete[/green]")
    vidFile.release()

if __name__=="__main__":
    main()