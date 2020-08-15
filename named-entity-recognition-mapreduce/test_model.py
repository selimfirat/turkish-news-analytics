from format_charner import FormatCharNER
from model_charner import ModelBiLSTM

dataset = FormatCharNER(train_file="data/train.txt", validation_file="data/dev.txt", test_file="data/test.txt")

model = ModelBiLSTM(dataset)

history = model.fit(dataset.train_x, dataset.train_y, dataset.val_x, dataset.val_y)

model.save_weights("model.h5")