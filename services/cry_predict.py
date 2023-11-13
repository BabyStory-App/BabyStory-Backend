import numpy as np
import tensorflow as tf
import librosa
import os
from io import BytesIO
from skimage.transform import resize
from typing import Dict

from constants.path import PROJECT_DIR

os.environ['NUMBA_DISABLE_JIT'] = "1"


class CryPredictService:
    def __init__(self):
        self.model = tf.keras.models.load_model(
            os.path.join(PROJECT_DIR, 'assets', 'crnn.h5'))

    async def get_input_vector_from_uploadfile(self, byteFile) -> np.ndarray:
        y, sr = librosa.load(BytesIO(byteFile), sr=16000)

        y = y[:(2 * sr)]

        mel_spec = librosa.feature.melspectrogram(
            y=y, sr=sr, n_mels=128, n_fft=2048, hop_length=501)
        mel_spec_dB = librosa.power_to_db(mel_spec, ref=np.max)
        RATIO = 862 / 64
        mel_spec_dB_resized = resize(mel_spec_dB, (mel_spec_dB.shape[0], mel_spec_dB.shape[1] * RATIO),
                                     anti_aliasing=True, mode='reflect')
        mel_spec_dB_stacked = np.stack([mel_spec_dB_resized] * 3, axis=-1)
        return mel_spec_dB_stacked[np.newaxis, ]

    async def get_predict_class(self, input_vector):
        classes = ['sad', 'hug', 'diaper', 'hungry',
                   'sleepy', 'awake', 'uncomfortable']
        predictions = self.model.predict(input_vector)[0]
        predictMap = {}
        for i in range(len(classes)):
            predictMap[classes[i]] = float(predictions[i])
        return dict(sorted(predictMap.items(), key=lambda item: item[1], reverse=True))

    async def __call__(self, bytes: bytes) -> Dict[str, float]:
        input_vector = await self.get_input_vector_from_uploadfile(bytes)
        predictMap = await self.get_predict_class(input_vector)
        return predictMap


cry_predict = CryPredictService()
