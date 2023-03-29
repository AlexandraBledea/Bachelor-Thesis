import tensorflow as tf

from src.data_processing.english.ravdess_dataset import RavdessDataset
from src.data_processing.english.savee_dataset import SaveeDataset
from src.data_processing.english.tess_dataset import TessDataset
from src.ui.ui import UI

if __name__ == '__main__':

    # ui = UI()
    # ui.append_command(TessDataset(1, 'tess'))
    # command = TessDataset(1, 'tess')
    # command = SaveeDataset(2, 'ravdess')
    # command.execute()
    # print(command.paths[:10])
    # print(command.labels[:10])

    a = []
    a = a + [1, 2, 3]
    print(a)

    if tf.test.is_gpu_available():
        #     print("yes")
        # else:
        #     print("no")
        print('Default GPU Device:{}'.format(tf.test.gpu_device_name()))
    else:
        print("Please install GPU version of TF")
    print(tf.config.list_physical_devices('GPU'))

