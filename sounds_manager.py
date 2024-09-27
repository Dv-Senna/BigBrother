import pygame
from pygame import mixer
import os
import glob
import sys

AUDIO_FILE_PATH = os.path.join('assets', 'audio')

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.ambient_sounds = {}
        self.current_ambient = None

    def load_all(self):
        all_audios = (glob.glob(os.path.join(AUDIO_FILE_PATH, "**/*.wav"), recursive=True))
        n = len(all_audios)


        for i, audio_path in enumerate(all_audios):
            perc = i / n
            #Get the name of the audio file without the .wav
            name = audio_path.split('/')[-1].split('.')[0]
            print(f'[SOUND-MANAGER] Loading sound {name[:10]:>10} ({100*perc:.0f}%)', end='\r')
            ambient = 'ambient' in audio_path
            sound_manager.load_sound(name, audio_path, ambient=ambient)

        print(sound_manager.ambient_sounds)

        print(f'[SOUND-MANAGER] {n} sound loaded                                       ') # space to remove previous


    def load_sound(self, name, filepath, ambient=False):
        """Load a sound effect or ambient sound."""
        sound = mixer.Sound(filepath)
        if ambient:
            self.ambient_sounds[name] = sound
        else:
            self.sounds[name] = sound

    def play_sound(self, name, loops=0):
        """Play a sound effect."""
        if name in self.sounds:
            self.sounds[name].play(loops)
        else:
            print(f"Sound {name} not found.")

    def play_ambient(self, name, volume=0.5):
        """Play an ambient sound, does not stop the previous one."""
        
        if name in self.ambient_sounds:
            self.current_ambient = self.ambient_sounds[name]
            self.current_ambient.set_volume(volume)
            self.current_ambient.play(loops=-1)  # -1 means the sound will loop indefinitely
        else:
            print(f"Ambient sound {name} not found.")

    def stop_ambient(self):
        """Stop the current ambient sound."""
        if self.current_ambient:
            self.current_ambient.stop()
            self.current_ambient = None

    def set_volume(self, name, volume):
        """Set the volume for a specific sound."""
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        elif name in self.ambient_sounds:
            self.ambient_sounds[name].set_volume(volume)
        else:
            print(f"Sound {name} not found.")

    def stop_all_sounds(self):
        """Stop all sounds."""
        for sound in self.sounds.values():
            sound.stop()
        self.stop_ambient()

# Example usage
if __name__ == "__main__":
    # Initialize the sound manager
    sound_manager = SoundManager()
    sound_manager.load_all()

    # Play sound effect
    sound_manager.play_sound("door_1")
    pygame.time.wait(300)
    sound_manager.play_sound("beep_only")
    
    # Play ambient sound
    sound_manager.play_ambient("morning_highway_birds", volume=1)
    
    # Change ambient sound after some action
    pygame.time.wait(5000)  # Wait for 5 seconds
    #sound_manager.play_ambient("cave")
    sound_manager.play_ambient("empty_room_background")
    
    # Stop all sounds
    pygame.time.wait(5000)  # Wait for another 5 seconds
    sound_manager.stop_all_sounds()
