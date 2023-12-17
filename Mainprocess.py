import librosa as lr
import numpy as np
import scipy.signal as signal
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.io import wavfile
import IPython.display as ipd
import io
import noisereduce as nr
import torch

#Get Main Audio Sample AUdio Sample Rat
# e 
def audio_addAir(input_audio, ratio):
    ratioMod = float(ratio)/100
    Q = 1.0  # Quality factor
    gain = 3  # Gain in dB
    freq = 7000 
    # Design a peaking EQ filter to boost 7 kHz
    b, a = signal.iirpeak(freq / (sr / 2), Q, gain)

    # Apply the filter
    audio_filtered = signal.lfilter(b, a, input_audio)

    audio_sum = ratioMod * audio_filtered + (1-ratioMod) * input_audio
    # Save the filtered audio
    sf.write('your_audio_file_filtered.wav', audio_sum, sr)

    return audio_sum

# Sum the original audio with the pitch shifted audio
def audio_addOctaveHigher(input_audio, ratio):
    ratioMod = float(ratio)/100
# Pitch shift the audio by 12 semitones (1 octave)
    octave_higher_audio = lr.effects.pitch_shift(mono_audio, sr = sr, n_steps=12)

# Save the pitch-shifted audio
    audio_sum = ratioMod * octave_higher_audio + (1-ratioMod) * input_audio
    return audio_sum

def audio_addOctaveLower(input_audio, ratio):
    ratioMod = float(ratio)/100
# Pitch shift the audio by 12 semitones (1 octave)
    octave_lower_audio = lr.effects.pitch_shift(mono_audio, sr = sr, n_steps=-12)

# Save the pitch-shifted audio
    audio_sum = ratioMod * octave_lower_audio + (1-ratioMod) * input_audio
    return audio_sum

def audio_addReverb(input_audio, ratio):
    ratioMod = float(ratio)/100
    # Convolve the signal with the impulse response
    audio_reverb = signal.convolve(input_audio, ir)

    # Save the reverberated audio
    audio_sum = ratioMod * audio_reverb + (1-ratioMod) * input_audio
    return audio_sum