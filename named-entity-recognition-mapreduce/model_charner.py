import keras as K
from keras import Sequential, Input
from keras.layers import Embedding, Dropout, Bidirectional, LSTM, TimeDistributed, Dense
from keras import optimizers
from keras.optimizers import SGD, Adam

from f1_score import metrics
from tagger import Tagger


class ModelBiLSTM:

    def __init__(self, dataset, cfg=None):
        self.cfg = cfg
        self.dataset = dataset

        if cfg is None:
            self.cfg = {
                "char_embedding": {
                    "input_dim": self.dataset.num_chars, # Char alphabet vocabulary
                    "output_dim": 30, # char embedding size,
                    "mask_zero": True # 0 values should be masked out since input is variable length
                },
                "char_embedding_dropout": {
                    "rate": 0.5
                },
                "lstms_all": {
                    "return_sequences": True
                },
                "lstms": [
                    { "units": 100 },
                    { "units": 75 },
                    { "units": 50 }
                ],
                "compilation": {
                    "loss": "mean_squared_error",
                    "optimizer": SGD(lr=0.01, clipnorm=1.0)
                },
                "lstm_end_dropout": {
                    "rate": 0.5
                },
                "softmax": {
                    "units": 8,
                    "activation": "softmax"
                },
                "training": {
                    "epochs": 2,
                    "batch_size": 32,
                    "validation_split": 0.1,
                    "shuffle": True
                },
                "sentence_max_length": 250
            }


        self._model = self.model()
        print(self._model.summary())

    def save_weights(self, fp):
        self._model.save_weights(fp)

    def load_weights(self, fp):
        self._model.load_weights(filepath=fp)

    def extract_named_entities(self, str):
        tagger = Tagger(self._model, preprocessor=self.dataset.pp)

        return tagger.analyze(str.split())

    def model(self):
        m = Sequential()

        m.add(Embedding(**self.cfg["char_embedding"]))
        m.add(Dropout(**self.cfg["char_embedding_dropout"]))

        for lstm in self.cfg["lstms"]:
            m.add(Bidirectional(LSTM(**lstm, **self.cfg["lstms_all"])))

        m.add(Dropout(**self.cfg["lstm_end_dropout"]))

        m.add(TimeDistributed(Dense(**self.cfg["softmax"])))

        m.compile(**self.cfg["compilation"])

        return m

    def fit(self, train_x, train_y, val_x, val_y):
        return self._model.fit(train_x, train_y, validation_data=(val_x, val_y), **self.cfg["training"], callbacks=[metrics])