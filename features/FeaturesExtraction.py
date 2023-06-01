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
    def extract_f0(signal):
        f0 = np.mean(librosa.yin(signal, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7')))
        return f0

    @staticmethod
    def extract_features(sig, sr):
        result = np.array([])

        # We are stacking the features horizontally

        # result = np.hstack((result, FeaturesExtraction.extract_ZCR(sig)))
        # result = np.hstack((result, FeaturesExtraction.extract_mel_spectrogram(sig, sr)))
        # result = np.hstack((result, FeaturesExtraction.extract_root_mean_square_value(sig)))
        zcr = FeaturesExtraction.extract_ZCR(sig)
        mel_spectrogram = FeaturesExtraction.extract_mel_spectrogram(sig, sr)
        # root_mean_square_value = extract_root_mean_square_value(sig)
        mfcc = FeaturesExtraction.extract_mfcc(sig, sr)
        f0 = FeaturesExtraction.extract_f0(sig)
        result = np.hstack((result, zcr))
        result = np.hstack((result, mel_spectrogram))
        # result = np.hstack((result, root_mean_square_value))
        result = np.hstack((result, f0))
        result = np.hstack((result, mfcc))

        return result


    @staticmethod
    def extract_mfcc_features(sig, sr):
        result = np.array([])

        mfcc = FeaturesExtraction.extract_mfcc(sig, sr)

        result = np.hstack((result, mfcc))

        return result

    @staticmethod
    def extract_pitch_standard_deviation(signal, sample_rate):
        pitch_, _ = librosa.core.piptrack(y=signal, sr=sample_rate)
        pitch_dev = np.std(pitch_, axis=0)

        return pitch_dev.mean()

    @staticmethod
    def extract_mel_spect_pitch_dev(sig, sr):
        result = np.array([])

        pitch_dev = FeaturesExtraction.extract_pitch_standard_deviation(sig, sr)
        mel_spect = FeaturesExtraction.extract_mel_spectrogram(sig, sr)

        result = np.hstack((result, mel_spect))
        result = np.hstack((result, pitch_dev))

        return result

    @staticmethod
    def normalize_volume(signal):
        max_amplitude = np.max(np.abs(signal))

        scale = 0.5 / max_amplitude

        signal = signal * scale

        return signal

    @staticmethod
    def trim_silence(signal, threshold=30):
        # Trim leading and trailing silence
        trimmed_signal, _ = librosa.effects.trim(signal, top_db=threshold)

        return trimmed_signal

    @staticmethod
    def extract_mel_spect_features(sig, sr):
        result = np.array([])

        mel_spect = FeaturesExtraction.extract_mel_spectrogram(sig, sr)

        result = np.hstack((result, mel_spect))

        return result