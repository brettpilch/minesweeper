from __future__ import division
import config as cfg
from board import Board

def frames_to_string(frames, frame_rate):
    total_seconds = frames // frame_rate
    minutes = str(total_seconds // 60)
    seconds = total_seconds % 60
    if seconds < 10:
        seconds = '0' + str(seconds)
    else:
        seconds = str(seconds)
    return minutes + ':' + seconds

def string_to_frames(string, frame_rate):
    minutes, seconds = string.split(':')
    return (int(minutes) * 60 + int(seconds)) * frame_rate

def load_map(number, extension = '.txt'):
    filename = 'map' + number + extension
    territory_str = ''
    with open(filename, 'r') as file_obj:
        territory_str = file_obj.read()
    if territory_str:
        return Board(territory_str)
    else:
        print filename + 'not found.'