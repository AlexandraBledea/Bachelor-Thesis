import unittest
from features.DataProcessing import DataProcessing

import librosa


class TestDataProcessing(unittest.TestCase):
    __path = "C:\\Users\\night\\Desktop\\Alexandra\\happiness\\"
    sig, sr = librosa.load(__path + '1-h-1.wav')

    def test_extract_mfcc_mean(self):
        mfcc = DataProcessing.extract_mfcc_mean(self.sig, self.sr)
        assert len(mfcc) == 40

    def test_extract_mel_spectrogram_mean(self):
        mel = DataProcessing.extract_mel_spectrogram_mean(self.sig, self.sr)
        assert len(mel) == 128

    def test_extract_mel_spectrogram_multi_time_steps(self):
        mel = DataProcessing.extract_mel_spectrogram_multi_time_steps(self.sig, self.sr)
        assert mel.shape == (107, 128)
        assert mel.shape[0] == 107
        assert mel.shape[1] == 128

    def test_extract_mfcc_multi_time_steps(self):
        mfcc = DataProcessing.extract_mfcc_multi_time_steps(self.sig, self.sr)
        assert mfcc.shape == (107, 40)
        assert mfcc.shape[0] == 107
        assert mfcc.shape[1] == 40

    def test_extract_mel_spect_and_mfcc_mean(self):
        mel_mfcc = DataProcessing.extract_mel_spect_and_mfcc_mean(self.sig, self.sr)
        assert len(mel_mfcc) == 168

    def test_extract_mel_mfcc_multi_time_steps(self):
        mel_mfcc = DataProcessing.extract_mel_mfcc_multi_time_steps(self.sig, self.sr)
        assert mel_mfcc.shape == (107, 168)
        assert mel_mfcc.shape[0] == 107
        assert mel_mfcc.shape[1] == 168

    def test_extract_mfcc_features(self):
        mfcc = DataProcessing.extract_mfcc_features(self.sig, self.sr)
        assert len(mfcc) == 40

    def test_extract_mel_spect_features(self):
        mel = DataProcessing.extract_mel_spect_features(self.sig, self.sr)
        assert len(mel) == 128
