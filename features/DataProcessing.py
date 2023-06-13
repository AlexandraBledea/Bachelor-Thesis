import librosa
import numpy as np


class DataProcessing(object):

    @staticmethod
    def extract_mfcc_mean(signal, sample_rate):
        mfcc = np.mean(librosa.effects.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40).T, axis=0)
        return mfcc

    @staticmethod
    def extract_mel_spectrogram_mean(signal, sample_rate):
        mel = np.mean(librosa.effects.feature.melspectrogram(y=signal, sr=sample_rate).T, axis=0)
        return mel

    @staticmethod
    def extract_mel_spectrogram_multi_time_steps(signal, sample_rate):
        mel = librosa.effects.feature.melspectrogram(y=signal, sr=sample_rate)
        return mel.transpose()

    @staticmethod
    def extract_mfcc_multi_time_steps(signal, sample_rate):
        mfcc = librosa.effects.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=40)
        return mfcc.transpose()

    @staticmethod
    def extract_mel_spect_and_mfcc_mean(sig, sr):

        result = np.array([])
        mel_spect = DataProcessing.extract_mel_spectrogram_mean(sig, sr)
        mfcc = DataProcessing.extract_mfcc_mean(sig, sr)
        result = np.hstack((result, mel_spect))
        result = np.hstack((result, mfcc))

        return result

    @staticmethod
    def extract_mel_mfcc_multi_time_steps(sig, sr):

        mfcc = DataProcessing.extract_mfcc_multi_time_steps(sig, sr)
        spec = DataProcessing.extract_mel_spectrogram_multi_time_steps(sig, sr)
        result = np.concatenate((spec, mfcc), axis=1)

        return result

    @staticmethod
    def extract_mfcc_features(sig, sr):

        result = np.array([])
        mfcc = DataProcessing.extract_mfcc_mean(sig, sr)
        result = np.hstack((result, mfcc))

        return result

    @staticmethod
    def extract_mel_spect_features(sig, sr):
        result = np.array([])
        mel_spect = DataProcessing.extract_mel_spectrogram_mean(sig, sr)
        result = np.hstack((result, mel_spect))

        return result

    @staticmethod
    def pad_audio_alexandra(signal):
        length_diff = 221184 - len(signal)
        if length_diff > 0:
            audio = np.pad(signal, (0, length_diff), mode='constant')
            return audio

        elif length_diff < 0:

            cut_audio = signal[0:221184]
            return cut_audio

        return signal

    @staticmethod
    def pad_audio_ravdess(signal):
        length_diff = 253053 - len(signal)
        if length_diff > 0:
            audio = np.pad(signal, (0, length_diff), mode='constant')
            return audio

        elif length_diff < 0:

            cut_audio = signal[0:253053]
            return cut_audio

        return signal

    @staticmethod
    def normalize_volume(signal):
        max_amplitude = np.max(np.abs(signal))

        scale = 0.5 / max_amplitude

        signal = signal * scale

        return signal

    @staticmethod
    def trim_silence(signal, threshold=30):
        trimmed_signal, _ = librosa.effects.trim(signal, top_db=threshold)

        return trimmed_signal

    @staticmethod
    def decode_labels(prediction, encoder):
        labels = []

        for index in range(0, len(prediction[0])):
            prediction_index_2d = np.zeros_like(prediction)
            prediction_index_2d[0][index] = 1
            prediction_label_enc = encoder.inverse_transform(prediction_index_2d)
            prediction_label = prediction_label_enc[0][0]

            labels.append(prediction_label)

        return labels

    @staticmethod
    def create_percentages_for_emotions(labels, prediction):
        percentages = [round(val * 100, 2) for val in prediction]

        res = {}
        for index in range(0, len(labels)):
            labels[index] = labels[index].capitalize()
            res[labels[index]] = percentages[index]

        return res
