import librosa
import librosa.display
import numpy as np
from IPython.utils import data
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import librosa
import librosa.display
from IPython.display import Audio
import warnings
import tensorflow as tf
from sklearn.model_selection import train_test_split


def waveform(data, sample_rate, emotion):
    plt.figure(figsize=(10, 4))
    plt.title("Waveplot for audio with {} emotion".format(emotion), size=20)
    librosa.display.waveshow(data, sr=sample_rate)
    plt.show()


def spectrogram(data, sample_rate, emotion):
    # stft function converts the data into short term fourier transform
    x = librosa.stft(data)

    # converting the file to decibels
    xdb = librosa.amplitude_to_db(x)

    plt.figure(figsize=(11, 4))
    plt.title("Spectrogram for audio with {} emotion".format(emotion), size=20)
    librosa.display.specshow(xdb, sr=sample_rate, x_axis='time', y_axis='hz')
    plt.colorbar()


def extract_ZCR(signal):
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=signal).T, axis=0)
    return zcr


def extract_root_mean_square_value(signal, data):
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    return rms


def extract_mel_spectrogram(signal, sample_rate):
    mel = np.mean(librosa.feature.melspectrogram(y=signal, sr=sample_rate).T, axis=0)
    return mel


def extract_mfcc(signal, sample_rate):
    # signal, sample_rate = librosa.load(file_name, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40).T, axis=0)
    return mfcc

def extract_features(sig, sr):

    result = np.array([])

    # We are stacking the features horizontally

    result = np.hstack((result, extract_ZCR(sig)))
    result = np.hstack((result, extract_mel_spectrogram(sig, sr)))
    result = np.hstack((result, extract_root_mean_square_value(sig)))
    result = np.hstack((result, extract_mfcc(sig, sr)))

    return result

def noise(data):
    noise_amp = 0.035*np.random.uniform()*np.amax(data)
    data = data + noise_amp*np.random.normal(size=data.shape[0])
    return data

def stretch(data, rate=0.8):
    shift_range = int(np.random.uniform(low=-5, high=5)*1000)
    return np.roll(data, shift_range)

def pitch(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)