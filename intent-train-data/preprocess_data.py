import csv
import pandas as pd
import random

labels = ['AddToPlaylist', 'BookRestaurant', 'GetWeather', 'PlayMusic', 'RateBook', 'SearchCreativeWork', 'SearchScreeningEvent']
files = ['AddToPlaylist.txt', 'BookRestaurant.txt', 'GetWeather.txt', 'PlayMusic.txt', 'RateBook.txt', 'SearchCreativeWork.txt', 'SearchScreeningEvent.txt']
with open('./data.csv', mode='w', encoding='Latin-1') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(7):
        pre_data = open(files[i], mode='r', encoding='Latin-1')
        data = pre_data.read().splitlines()
        for line in data:
            data_writer.writerow([labels[i], line.encode().decode('Latin-1')])
        pre_data.close()

df = pd.read_csv('./data.csv', header=None, sep=',')
df = df.sample(frac=1).reset_index(drop=True)
df_train = df.head(138*80)
df2 = df.tail(138*20)
df_dev = df2.head(138*10)
df_test = df2.tail(138*10)
df_train.to_csv('./data/train.csv')
df_dev.to_csv('./data/dev.csv')
df_test.to_csv('./data/test.csv')

    
    

