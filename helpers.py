"""
Helper functions used by the other minesweeper python files.
"""

from __future__ import division
import config as cfg
from board import Board

def frames_to_string(frames, frame_rate):
    """
    Convert a number of frames to a time string, such as '11:45'.
    """
    total_seconds = frames // frame_rate
    minutes = str(total_seconds // 60)
    seconds = total_seconds % 60
    if seconds < 10:
        seconds = '0' + str(seconds)
    else:
        seconds = str(seconds)
    return minutes + ':' + seconds

def string_to_frames(string, frame_rate):
    """
    Convert a time string to the equivalent number of frames.
    """
    minutes, seconds = string.split(':')
    return (int(minutes) * 60 + int(seconds)) * frame_rate

def load_map(number, extension = '.txt'):
    """
    Given a certain map # n, open the file 'mapn.txt'.
    Return the Board object created from that text file.
    """
    filename = 'map' + number + extension
    territory_str = ''
    with open(filename, 'r') as file_obj:
        territory_str = file_obj.read()
    if territory_str:
        return Board(territory_str)
    else:
        print filename + 'not found.'
