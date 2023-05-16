from argparse import ArgumentParser,Namespace
from devtools import debug
from loguru import logger

from pydantic import BaseModel, validator

class VidExtractArgs(BaseModel):
    """command line arguments"""
    outputDir:str
    videoFile:str

    minSegments:int
    maxSegments:int

    shuffle:bool

def getArgs()->VidExtractArgs:
    """get arguments from commandline for vid extract program"""

    parser=ArgumentParser(
        prog="Video Summariser",
        usage="target a video file to extract screenshots from the video at random intervals"
    )

    parser.add_argument(
        "-v",
        "--video-file",
        type=str,
        required=True,
        help="target video file",
        dest="videoFile"
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        required=True,
        help="output directory to place output files. will be created if doesn't exist",
        dest="outputDir"
    )

    parser.add_argument(
        "-n1",
        "--min",
        type=int,
        required=True,
        help="minimum target number of images to produce",
        dest="minSegments"
    )

    parser.add_argument(
        "-n2",
        "--max",
        type=int,
        required=True,
        help="maximum target number of images to produce",
        dest="maxSegments"
    )

    parser.add_argument(
        "-s",
        "--shuffle",
        required=False,
        action="store_true",
        help="shuffle generation order",
        dest="shuffle"
    )

    args:VidExtractArgs=VidExtractArgs.parse_obj(vars(parser.parse_args()))

    if args.minSegments>args.maxSegments:
        logger.error("min segments must be lower than max segments")
        raise Exception("min segments error")

    return args