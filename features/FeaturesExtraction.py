import librosa
import numpy as np


class FeaturesExtraction(object):

    @staticmethod
    def extract_ZCR(signal):
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=signal).T, axis=0)
        return zcr

    @staticmethod
    def extract_root_mean_square_value(signal):
        rms = np.mean(librosa.feature.rms(y=signal).T, axis=0)
        return rms

    @staticmethod
    def extract_mel_spectrogram(signal, sample_rate):
        mel = np.mean(librosa.feature.melspectrogram(y=signal, sr=sample_rate).T, axis=0)
        return mel

    @staticmethod
    def extract_mfcc(signal, sample_rate):
        # signal, sample_rate = librosa.load(file_name, duration=3, offset=0.5)
        mfcc = np.mean(librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40).T, axis=0)
        return mfcc

    @staticmethod
    def extract_features(sig, sr):
        result = np.array([])

        # We are stacking the features horizontally

        result = np.hstack((result, FeaturesExtraction.extract_ZCR(sig)))
        result = np.hstack((result, FeaturesExtraction.extract_mel_spectrogram(sig, sr)))
        result = np.hstack((result, FeaturesExtraction.extract_root_mean_square_value(sig)))
        result = np.hstack((result, FeaturesExtraction.extract_mfcc(sig, sr)))

        return result