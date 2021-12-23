import os
import random


def shuffle_tracks(dir_path='/static/player/tracks/'):    
    default_dir = '/static/player/tracks/'
    tracks=[]
    for file_name in os.listdir(dir_path):       
        tracks.append(os.path.join(default_dir, file_name))        
    random.shuffle(tracks)  
    return tracks
