import pandas as pd
import numpy as np
import os
from urllib import request
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import SGD
from sklearn.metrics import classification_report
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense

base_dir = 'data/imgs/imgs'

train_dir = os.path.join(base_dir, 'train')
val_dir = os.path.join(base_dir, 'test')
test_dir = os.path.join(base_dir, 'val')

batch_size = 64

train_datagen = ImageDataGenerator(rescale = 1.0/255., 
                                   shear_range=0.2,
                                   zoom_range=0.15,
                                   horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale = 1.0/255.)
val_datagen = ImageDataGenerator(rescale = 1.0/255.)

train_gen = train_datagen.flow_from_directory(train_dir, target_size = (150,150), 
                                              batch_size=batch_size, 
                                              class_mode = 'categorical')
val_gen = test_datagen.flow_from_directory(val_dir, target_size = (150,150), 
                                              batch_size=batch_size, 
                                              class_mode = 'categorical')
test_gen = val_datagen.flow_from_directory(test_dir, target_size = (150, 150),
                                          batch_size=2, class_mode='categorical',
                                          shuffle=False)

base_model = VGG16(weights='imagenet', include_top=False, input_tensor=Input(shape=(150, 150, 3)))

x = base_model.output
x = Flatten(name="flatten")(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(30, activation='softmax')(x)

# Initializing the model
model = Model(inputs=base_model.input, outputs=x)

# Freezing all pre-trained layers at first
for layer in base_model.layers:
	layer.trainable = False

opt = SGD(lr=1e-4, momentum=0.9)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

# Training the fully connected layers for 50 epochs
H = model.fit_generator(
	train_gen,
	steps_per_epoch = 51300 // batch_size,
	validation_data = val_gen,
	validation_steps = 5700 // batch_size,
	epochs=50)

train_gen.reset()
val_gen.reset()

# Unfreezing some of the pre-trained layers to further tailor to the training data
for layer in base_model.layers[15:]:
  layer.trainable = True

opt = SGD(lr=1e-4, momentum=0.9)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
 
# Training unfrozen layers for another 20 epochs
H = model.fit_generator(
	train_gen,
	steps_per_epoch = 51300 // batch_size,
	validation_data = val_gen,
	validation_steps = 5700 // batch_size,
	epochs=20)

model.save('pretrained_vgg_model.hd5')