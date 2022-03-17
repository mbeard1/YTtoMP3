from argparse import ArgumentParser as ap
import os
import subprocess as sp
import pytube
from pytube.cli import on_progress


def cleanup(destination: str):

    temp_path = os.path.join(destination, 'tempvideo.mp4')

    if os.path.exists(temp_path):
        os.remove(temp_path)
    else:
        print('Video File Unable to be Removed')

    return


def rip_audio(destination: str):

    sp.call(['ffmpeg',
             '-loglevel', '0',
             '-y',
             '-i', os.path.join(destination, 'tempvideo.mp4'),
             os.path.join(destination, 'someoutputfile.wav')])

    return


def yt_dl(url: str, destination: str):

    yt = pytube.YouTube(url)
    yt.register_on_progress_callback(on_progress)
    yt.streams.get_highest_resolution().download(destination, filename='tempvideo.mp4')

    return


def yt_to_mp3(url: str, destination: str, video: bool):

    yt_dl(url, destination)
    if not video:
        rip_audio(destination)

    return


if __name__ == '__main__':

    parser = ap(description='Rip Audio From Given YouTube Video')
    parser.add_argument('-u', '--url', type=str, help='URL for the youtube video', required=True)
    parser.add_argument('-d', '--destination', type=str, help='Destination for the output file', required=True)
    parser.add_argument('-v', '--video', action='store_true')

    args = parser.parse_args()

    yt_to_mp3(args.url, args.destination, args.video)
    if not args.video:
        cleanup(args.destination)
