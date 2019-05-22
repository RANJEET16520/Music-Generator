import os
import subprocess
import regex as re

def extract_song_snippet(generated_text):
    pattern = '\n\n(.*?)\n\n'
    search_results = re.findall(pattern, generated_text, overlapped=True, flags=re.DOTALL)
    songs = [song for song in search_results]
    print("Found {} possible songs in generated texts".format(len(songs)))
    return songs

def save_song_to_abc(song, filename="tmp"):  # Save the file to songs to .abc file.
    save_name = "{}.abc".format(filename)
    with open(save_name, "w") as f:
        f.write(song)
    return filename

def abc2wav(abc_file):  # To convert abc2wav file.
    abc,ext = abc_file.split('.') # Split to filename + .abc
    if ext != 'abc': # If it is not .abc file then return.
        return False
    mid_file = abc+'.mid' # converting to .mid file.
    wav_file = abc+'.wav' # converting to .wav file.

    if os.path.exists(mid_file): # If files already exist then remove the files and replace with new files.
        print('\n!!!!File exists and we are removing it.!!!!\n')
        os.system('rm {} {}'.format(mid_file,wav_file)) # Accessing the terminal to remove the existing files

    # For following operation you must download abcmidi and timidity packages.
    # sudo apt-get install abcmidi
    # sudo apt-get install timidity
    os.system('abc2midi {} -o {}'.format(abc_file,mid_file))
    os.system('timidity {} -Ow {}'.format(mid_file,wav_file)) 

    return wav_file
   
def play_wav(wav_file):
    os.system('play {}'.format(wav_file)) # Executing the .wav file to sound music
    return

def play_generated_song(generated_text):  # Enter
    songs = extract_song_snippet(generated_text) # Total generated songs.
    if len(songs) == 0:
        print("No valid songs found in generated text. Try training the model longer or increasing the amount of generated music to ensure complete songs are generated!")

    for song in songs:
        basename = save_song_to_abc(song)
        wav_file = abc2wav(basename+'.abc') 

        if wav_file != False: 
            return play_wav(wav_file)
    print("None of the songs were valid, try training longer to improve syntax.")