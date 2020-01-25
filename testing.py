import pandas as pd
import numpy as np
import os
from urllib import request
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

# Reading in dataframe with filepaths for all 200,000 book images and dropping books that are included in the training set
books = pd.read_csv('data/book32-listing.csv', encoding = "ISO-8859-1")

books = books.rename(columns={'761183272': 'amazon index', '0761183272.jpg': 'filename',
                                'http://ecx.images-amazon.com/images/I/61Y5cOdHJbL.jpg': 'url',
                               "Mom's Family Wall Calendar 2016": 'title', 'Sandra Boynton': 'author',
                               '3': 'category id', 'Calendars': 'genre'})

train_df = pd.read_csv('data/trainmeta.csv', encoding = "ISO-8859-1")
train_df = train_df[['[FILENAME]', '[CATEGORY ID]', '[CATEGORY]']]
train_df = train_df.rename(columns={'[FILENAME]': 'file',
                      '[CATEGORY ID]': 'id',
                      '[CATEGORY]': 'genre'})

train_dict = {train_df.loc[i, 'file']: True for i in range(len(train_df))}

drop_list = []
for i in range(len(books)):
    if books.loc[i, 'filename'] in train_dict:
        drop_list.append(i)
books = books.drop(drop_list)

genres = ['Arts & Photography', 'Biographies & Memoirs', 'Business & Money',
 'Calendars', "Children's Books", 'Comics & Graphic Novels', 'Computers & Technology',
 'Cookbooks, Food & Wine', 'Crafts, Hobbies & Home', 'Christian Books & Bibles',
 'Engineering & Transportation', 'Health, Fitness & Dieting', 'History',
 'Humor & Entertainment', 'Law', 'Literature & Fiction', 'Medical Books',
 'Mystery, Thriller & Suspense', 'Parenting & Relationships', 'Politics & Social Sciences',
 'Reference', 'Religion & Spirituality', 'Romance', 'Science & Math',
 'Science Fiction & Fantasy', 'Self-Help', 'Sports & Outdoors', 'Teen & Young Adult',
 'Test Preparation', 'Travel']

# Generating a test set by randomly sampling from the larger dataset, then downloaded test images from AWS
test_sample = pd.DataFrame()
for g in genres:
    sdf = books[books['genre'] == g]
    sample = sdf.sample(200, replace=False, random_state=12)
    test_sample = test_sample.append(sample).reset_index(drop=True)

for i in range(len(test_sample)):
    fname = test_sample.loc[i, 'filename']
    url = test_sample.loc[i, 'url']
    downloaded_img = request.urlopen(url)
    f = open(f'../imgs/val/val/{fname}', mode='wb')
    f.write(downloaded_img.read())
    downloaded_img.close()
    f.close()

test_sample = test_sample.sort_values(by='filename').reset_index(drop=True)

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

STEP_SIZE_TEST=test_gen.n//test_gen.batch_size

loaded_model = load_model('pretrained_vgg_model.hd5')

pred=loaded_model.predict(test_gen, steps=STEP_SIZE_TEST, verbose=1)

predicted_class_indices=np.argmax(pred,axis=1)
labels = (train_gen.class_indices)
labels = dict((v,k) for k,v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]

test_sample['pred_genre'] = predictions

acc = sum([1 for i in range(len(test_sample)) if test_sample.loc[i,'category id'] == test_sample.loc[i, 'pred_genre']])/6000

def find_splits(genre):
    df = test_sample[test_sample['genre'] == genre].reset_index(drop=True)
    num_right = 0
    for i in range(len(df)):
        c = df.loc[i,'category id']
        pg = df.loc[i,'pred_genre']
        if c == pg:
            num_right +=1
    ap = round(num_right*100/len(df),3)
    return ap

results = []
for g in genres:
    results.append(find_splits(g))

result_frame = pd.DataFrame(data ={'genre': genres, 'accuracy percentage': results})
result_frame.to_csv('accuracy_by_genre.csv', index=False)