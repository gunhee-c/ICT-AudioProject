
import streamlit as st
import librosa as lr
import numpy as np
import scipy.signal as signal
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.io import wavfile
#import IPython.display as ipd
import io
import noisereduce as nr
import torch
import psola



#impulse_response, sr_ir = lr.load(impulse_file)


# for the case we need non-linear blending
def summing (origin, mod, ratio, adder = 1):
    
    ratioMod = (float(ratio)/100) ** (1/adder)
    audio_sum = ratioMod * mod + (1-ratioMod) * origin
    return audio_sum


def butter_bandpass(fs, order=5):
    lowcut = 500
    highcut = 2800
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, fs, order=5):
    b, a = butter_bandpass(fs, order=order)
    y = signal.lfilter(b, a, data)
    return y


#I: phone filter
#apply phone Filter to your sound
def phone(audio, sr, ratio):

    #ratioMod = float(ratio)/100
    b, a = butter_bandpass(sr, order=5)
    y = signal.lfilter(b, a, audio)
    #audio_sum = ratioMod * y + (1-ratioMod) * audio
    return summing(audio, y, ratio, adder = 3)

#E: Exciter
#Boost Air in your sound
def air(input_audio, sr, ratio):
    ratioMod = float(ratio)/100
    Q = 1.0  # Quality factor
    gain = 3  # Gain in dB
    freq = 7000 
    # Design a peaking EQ filter to boost 7 kHz
    b, a = signal.iirpeak(freq / (sr / 2), Q, gain)

    # Apply the filter
    audio_filtered = signal.lfilter(b, a, input_audio)
    audio_sum = ratioMod * audio_filtered + (1-ratioMod) * input_audio
    return audio_sum



def pad_to_match(array_to_extend, reference_array):
    target_length = len(reference_array)
    current_length = len(array_to_extend)
    padding_size = target_length - current_length
    if padding_size > 0:
        array_to_extend = np.pad(array_to_extend, (0, padding_size), mode='constant')
    return array_to_extend

#R: Reverb
#apply reverb to your sound
def reverb(audio, sr, impulse_audio, sr_ir, ratio):
    # Load the impulse response (replace 'path_to_your_impulse_response.wav' with the actual file path)
    ratioMod = float(ratio)/100 * 0.5

    # Apply reverb by convolving the audio with the impulse response
    reverberated_audio = signal.fftconvolve(audio, impulse_audio, mode='full')

    # Adjust the decay rate (replace 'decay_rate' with the desired value)
    decay_rate =  0.5 * ratioMod
    reverberated_audio *= decay_rate

    # Adjust the wet ratio (replace 'wet_ratio' with the desired value)
    wet_ratio = ratioMod
    audio = pad_to_match(audio, reverberated_audio)
    duration_to_trim = 12  # Duration to trim (in seconds)
    samples_to_trim = sr * duration_to_trim

    if samples_to_trim < len(audio):
        trimmed_audio = audio[:-samples_to_trim]
        trimmed_audio_rev = reverberated_audio[:-samples_to_trim]
    else:
    # Handle case where the audio is shorter than the trim duration
        trimmed_audio = audio
    return (1 - wet_ratio) * trimmed_audio + wet_ratio * trimmed_audio_rev

def basic_compressor(signal, threshold, ratio):
    # Applying basic compression (no attack, release, or knee)
    compressed_signal = np.copy(signal)
    for i in range(len(compressed_signal)):
        if abs(compressed_signal[i]) > threshold:
            multfactor = (abs(compressed_signal[i]) - threshold ) ** 0.2
            if compressed_signal[i] > 0:
                compressed_signal[i] = threshold + (compressed_signal[i] - threshold) / (ratio / multfactor)
            else:
                compressed_signal[i] = -threshold + (compressed_signal[i] + threshold) / (ratio / multfactor)
    return compressed_signal

def compressor(input_audio, sr, ratio):
    ratiomod = (float(ratio)/100 + 1)/2
# Compression settings (example values, you should adjust these)
    threshold = 0.1  # Threshold (linear amplitude)
    ratio_comp = 1 + ratio/20     # Compression ratio
# Apply compression
    compressed_audio = basic_compressor(input_audio, threshold, ratio_comp)

# Mix compressed audio with original (50/50 mix)
    return input_audio * (1-ratiomod) + compressed_audio * ratiomod

#F: Octave higher
# Sum the original audio with the pitch shifted audio
def octHigh(input_audio, sr, ratio):
    ratioMod = float(ratio)/100
# Pitch shift the audio by 12 semitones (1 octave)
    octave_higher_audio = lr.effects.pitch_shift(input_audio, sr = sr, n_steps=12)

# Save the pitch-shifted audio
    audio_sum = ratioMod * octave_higher_audio + (1-ratioMod) * input_audio
    return audio_sum

#T: Octave Lower
def octLow(input_audio, sr, ratio):
    ratioMod = float(ratio)/100
# Pitch shift the audio by 12 semitones (1 octave)
    octave_lower_audio = lr.effects.pitch_shift(input_audio, sr = sr, n_steps=-12)

# Save the pitch-shifted audio
    audio_sum = ratioMod * octave_lower_audio + (1-ratioMod) * input_audio
    return audio_sum

#P: Noise Cancellation
#reduce the rate of noise in the audio: Audio, Sample Rate, Ratio
def noisereduce(y,sr, ratio):
# Process the audio data (y) here if needed
    ratioMod = float(ratio)/100
# Convert the floating-point audio data to 16-bit PCM format for WAV file
    y_16bit = np.int16(y / np.max(np.abs(y)) * 32767)

    reduced_noise = nr.reduce_noise(y=y_16bit, sr=sr, prop_decrease = ratioMod)
    data_float = reduced_noise.astype(np.float32) / 32768.0  # 16-bit PCM
    return data_float

SEMITONES_IN_OCTAVE = 12
def degrees_from(scale: str):
    """Return the pitch classes (degrees) that correspond to the given scale"""
    degrees = lr.key_to_degrees(scale)
    # To properly perform pitch rounding to the nearest degree from the scale, we need to repeat
    # the first degree raised by an octave. Otherwise, pitches slightly lower than the base degree
    # would be incorrectly assigned.
    degrees = np.concatenate((degrees, [degrees[0] + SEMITONES_IN_OCTAVE]))
    return degrees

def closest_pitch(f0):
    """Round the given pitch values to the nearest MIDI note numbers"""
    midi_note = np.around(lr.hz_to_midi(f0))
    # To preserve the nan values.
    nan_indices = np.isnan(f0)
    midi_note[nan_indices] = np.nan
    # Convert back to Hz.
    return lr.midi_to_hz(midi_note)

def closest_pitch_from_scale(f0, scale):
    """Return the pitch closest to f0 that belongs to the given scale"""
    # Preserve nan.
    if np.isnan(f0):
        return np.nan
    degrees = degrees_from(scale)
    midi_note = lr.hz_to_midi(f0)
    # Subtract the multiplicities of 12 so that we have the real-valued pitch class of the
    # input pitch.
    degree = midi_note % SEMITONES_IN_OCTAVE
    # Find the closest pitch class from the scale.
    degree_id = np.argmin(np.abs(degrees - degree))
    # Calculate the difference between the input pitch class and the desired pitch class.
    degree_difference = degree - degrees[degree_id]
    # Shift the input MIDI note number by the calculated difference.
    midi_note -= degree_difference
    # Convert to Hz.
    return lr.midi_to_hz(midi_note)
#J: Autotune
def autotune(audio, sr, ratio, plot=False):
    # Set some basis parameters.
    frame_length = 2048 
    hop_length = frame_length // 4
    fmin = lr.note_to_hz('C2')
    fmax = lr.note_to_hz('C7')

    # Pitch tracking using the PYIN algorithm.
    f0, voiced_flag, voiced_probabilities = lr.pyin(audio,
                                                         frame_length=frame_length,
                                                         hop_length=hop_length,
                                                         sr=sr,
                                                         fmin=fmin,
                                                         fmax=fmax)

    # Apply the chosen adjustment strategy to the pitch.
    corrected_f0 = closest_pitch(f0)

    if plot:
        # Plot the spectrogram, overlaid with the original pitch trajectory and the adjusted
        # pitch trajectory.
        stft = lr.stft(audio, n_fft=frame_length, hop_length=hop_length)
        time_points = lr.times_like(stft, sr=sr, hop_length=hop_length)
        log_stft = lr.amplitude_to_db(np.abs(stft), ref=np.max)
        fig, ax = plt.subplots()
        img = lr.display.specshow(log_stft, x_axis='time', y_axis='log', ax=ax, sr=sr, hop_length=hop_length, fmin=fmin, fmax=fmax)
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        ax.plot(time_points, f0, label='original pitch', color='cyan', linewidth=2)
        ax.plot(time_points, corrected_f0, label='corrected pitch', color='orange', linewidth=1)
        ax.legend(loc='upper right')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [M:SS]')
        plt.savefig('pitch_correction.png', dpi=300, bbox_inches='tight')
    modified = psola.vocode(audio, sample_rate=int(sr), target_pitch=corrected_f0, fmin=fmin, fmax=fmax)
    # Pitch-shifting using the PSOLA algorithm.
    return summing(audio, modified, ratio, adder = 1)

def normalize(audio, sr, target = 0.5):

    max_amp = np.max(np.abs(audio))
    normalized_audio = np.zeros(len(audio))
    #print(len(audio))
    #print(np.arange(max_amp))
    for i in range(len(audio)):
        normalized_audio[i] = audio[i]/ (max_amp * (1/target))
    
    return normalized_audio

def doAudioProcess(audio_mono, audio_sample, sr):
    st.title('Now we are talking')
    st.write('Choose the effect you want to apply to your audio')
    st.write('You can adjust the ratio of the effect you want to apply')
    st.write('You can apply multiple effects to your audio')
    