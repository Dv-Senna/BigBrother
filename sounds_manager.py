import pygame
from pygame import mixer
import os
import glob
import sys

AUDIO_FILE_PATH = os.path.join('assets', 'audio')

class SoundManager:
    sounds = {}
    ambient_sounds = {}
    current_ambient = None

    @staticmethod
    def load_all():
        pygame.mixer.init()
        all_audios = (glob.glob(os.path.join(AUDIO_FILE_PATH, "**/*.wav"), recursive=True))
        n = len(all_audios)


        for i, audio_path in enumerate(all_audios):
            perc = i / n
            #Get the name of the audio file without the .wav
            name = audio_path.split('/')[-1].split('.')[0]
            print(f'[SOUND-MANAGER] Loading sound {name[:10]:>10} ({100*perc:.0f}%)', end='\r')
            ambient = 'ambient' in audio_path
            SoundManager.load_sound(name, audio_path, ambient=ambient)

        print(f'[SOUND-MANAGER] {n} sound loaded                                       ') # space to remove previous

    @staticmethod
    def load_sound(name, filepath, ambient=False):
        """Load a sound effect or ambient sound."""
        sound = mixer.Sound(filepath)
        if ambient:
            SoundManager.ambient_sounds[name] = sound
        else:
            SoundManager.sounds[name] = sound

    @staticmethod
    def play_sound(name, volume=0.5):
        """Play a sound effect."""
        if name in SoundManager.sounds:
            SoundManager.sounds[name].play(1)
            SoundManager.set_volume(name, volume)
        else:
            print(f"Sound {name} not found.")

    @staticmethod
    def play_ambient(name, volume=0.5):
        """Play an ambient sound, does not stop the previous one."""

        if name in SoundManager.ambient_sounds:
            current_ambient = SoundManager.ambient_sounds[name]
            current_ambient.set_volume(volume)
            current_ambient.play(loops=-1)  # -1 means the sound will loop indefinitely
        else:
            print(f"Ambient sound {name} not found.")

    @staticmethod
    def stop_ambient():
        """Stop the current ambient sound."""
        if current_ambient:
            current_ambient.stop()
            current_ambient = None

    @staticmethod
    def set_volume(name, volume):
        """Set the volume for a specific sound."""
        if name in SoundManager.sounds:
            SoundManager.sounds[name].set_volume(volume)
        elif name in SoundManager.ambient_sounds:
            SoundManager.ambient_sounds[name].set_volume(volume)
        else:
            print(f"Sound {name} not found.")

    @staticmethod
    def stop_all_sounds():
        """Stop all sounds."""
        for sound in SoundManager.sounds.values():
            sound.stop()
        SoundManager.stop_ambient()

# Example usage
if __name__ == "__main__":

    SoundManager.load_all()

    SoundManager.play_sound("door_1")
    pygame.time.wait(300)
    SoundManager.play_sound("beep_only")
    
    # Play ambient sound
    SoundManager.play_ambient("morning_highway_birds", volume=1)
    
    # Change ambient sound after some action
    pygame.time.wait(5000)  # Wait for 5 seconds
    SoundManager.play_ambient("empty_room_background")
    
    # Stop all sounds
    pygame.time.wait(5000)  # Wait for another 5 seconds
    SoundManager.stop_all_sounds()
