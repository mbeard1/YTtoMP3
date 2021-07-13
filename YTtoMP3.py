import sys
from argparse import ArgumentParser as ap
import subprocess as sp
import os
from pytube import YouTube
from pytube.cli import on_progress
import ffpb
import tqdm


def cleanup(destination: str):
    if os.path.exists(destination + '/tempvideo.mp4'):
        os.remove(destination + '/tempvideo.mp4')
    else:
        print('Video File Unable to be Removed')
    return


def ffmpeg_callback(infile: str, outfile: str, vstats_path: str):
    return sp.Popen(['ffmpeg',
                     '-nostats',
                     '-loglevel', '0',
                     '-y',
                     '-vstats_file', vstats_path,
                     '-i', infile,
                     outfile]).pid


def rip_audio(destination: str):
    ffmpeg_args = ['-loglevel', '0',
                   '-y',
                   '-i', destination + '/tempvideo.mp4',
                   destination + '/someoutputfile.wav']
    ffpb.main(argv=ffmpeg_args, stream=sys.stdout, tqdm=tqdm.tqdm)
    return


def yt_dl(url: str, destination: str):
    yt = YouTube(url)
    yt.register_on_progress_callback(on_progress)
    yt.streams.get_highest_resolution().download(destination, filename='tempvideo')
    return


def yt_to_mp3(url: str, destination: str):
    yt_dl(url, destination)
    rip_audio(destination)
    return


if __name__ == '__main__':
    parser = ap(description='Rip Audio From Given YouTube Video')
    parser.add_argument('-u', '--url', type=str, help='URL for the youtube video', required=True)
    parser.add_argument('-d', '--destination', type=str, help='Destination for the output file', required=True)

    args = parser.parse_args()

    yt_to_mp3(args.url, args.destination)
    cleanup(args.destination)
