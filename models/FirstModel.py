import array
import contextlib
import io
import wave

import audioread
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import joblib
import codecs


class FirstModel:

    def __init__(self):
        self.__path = "C:\\Users\\night\\Desktop\\Facultate An 3\\Thesis\\EXPERIMENTS\\Model 1\\"
        self.__model = load_model(self.__path + "training_model_experiment_x.h5")
        self.__encoder = self.__load_one_hot_encoder()
        self.__scaler = self.__load_standard_scaler()

    def __load_one_hot_encoder(self):
        features = pd.read_csv(self.__path + 'features.csv')
        Y = features['labels'].values
        enc = OneHotEncoder()
        enc.fit_transform(Y.reshape(-1, 1))

        return enc

    def __load_standard_scaler(self):
        scaler = joblib.load(self.__path + 'scaler.pk1')
        return scaler

    def receive_recording(self, recording, actual_label):
        byte_array = bytes(recording)
        self.__save_temporary_file(byte_array)



    def __save_temporary_file(self, bytes):
        with open('bueno.wav', mode='wb') as f:
            f.write(bytes)



        # # Create a BytesIO object from the byte array
        # bytes_data = bytes_io.read()
        #
        # # audio parameters
        # sample_rate = 44100
        # num_channels = 1
        # sample_width = 2  # for 16-bit sample width
        #
        # # convert byte array to numpy array
        # audio_data = np.frombuffer(byte_array, dtype=np.int16)
        #
        # # create wave file
        # with io.BytesIO() as wav_file:
        #     with wave.open(wav_file, 'wb') as output_file:
        #         output_file.setnchannels(num_channels)
        #         output_file.setframerate(sample_rate)
        #         output_file.setsampwidth(sample_width)
        #         output_file.setnframes(len(audio_data) // num_channels)
        #         output_file.setcomptype('NONE', 'not compressed')
        #         output_file.writeframes(audio_data.tobytes())
        #         frames = output_file.getnframes()
        #         rate = output_file.getframerate()
        #         duration = frames / float(rate)
        #         print(duration)
        #     # get wave file as bytes
        #     wav_bytes = wav_file.getvalue()
        #
        # # write bytes to a file
        # with open('output.wav', 'wb') as output_file:
        #     output_file.write(wav_bytes)
        #

        # with wave.open('audio.wav', 'wb') as wav_file:
        #     wav_file.setnchannels(1)  # Set the number of channels (1 for mono, 2 for stereo)
        #     wav_file.setsampwidth(2)  # Set the sample width (2 bytes for a 16-bit audio file)
        #     wav_file.setframerate(44100)  # Set the sample rate (44100 Hz is the standard for audio CDs)
        #     wav_file.writeframes(bytes_io.getbuffer())  # Write the audio data to the file

        # # Assuming 'bytes_array' is a byte array containing audio data
        # with wave.open('audio3.wav', 'wb') as wav_file:
        #     wav_file.setnchannels(1)  # Set the number of channels (1 for mono, 2 for stereo)
        #     wav_file.setsampwidth(3)  # Set the sample width (2 bytes for a 16-bit audio file)
        #     wav_file.setframerate(44100)  # Set the sample rate (44100 Hz is the standard for audio CDs)
        #     wav_file.setcomptype('NONE', 'Not Compressed')
        #     wav_file.setframerate(48)
        #     wav_file.writeframes(byte_array)

        # with open('audio.wav', 'rb') as f:
        #     audio_data = f.read()

        # print(f"Duration: {duration:.2f} seconds")

        # self.get_audio_format(bytes_data)

        # with contextlib.closing(wave.open(bytes_io, 'r')) as f:
        #     frames = f.getnframes()
        #     rate = f.getframerate()
        #     duration = frames / float(rate)
        #     print(duration)
        # #
        # df_predict = pd.DataFrame()
        # df_predict['speech'] =

    def get_audio_format(self, data):
        with data as f:
            with audioread.audio_open(f) as audio_file:
                return audio_file.format

        # Example usage
        my_data = b'...'  # your byte array here
        format = get_audio_format(my_data)
        print(f"The audio format is {format}")
