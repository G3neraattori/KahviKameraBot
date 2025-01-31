
import tensorflow as tf

import pathlib
datadir = pathlib.Path("Imagepool").absolute()
images = len(list(datadir.glob("kahvia*")))
img_height = 256#180
img_width = 256#320
print(str(datadir))

num_classes = 2

model = tf.keras.models.Sequential([
  tf.keras.layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

model.compile(optimizer="adam",loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])

epochs= 10
max_loop = 50
for seed in range(0,max_loop): # Vaihdellaan datasettiä aina välillä :D
  print(f"Swapping dataset... Loop {seed} of {max_loop}")
  train_ds = tf.keras.utils.image_dataset_from_directory(datadir, seed=seed,validation_split=0.8, subset="training")
  val_ds = tf.keras.utils.image_dataset_from_directory(datadir, seed=seed,validation_split=0.2,subset="validation")

  history = model.fit( train_ds, validation_data= val_ds,epochs=epochs)

predictions = model.predict(tf.keras.utils.image_dataset_from_directory(datadir))
print(str(tf.nn.softmax(predictions[0])))

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('kahviAI.tflite', 'wb') as f:
    f.write(tflite_model)