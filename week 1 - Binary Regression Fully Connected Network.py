# -*- coding: utf-8 -*-
"""Week 1- Binary Regression Fully Connected Network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mZO-H_m4JeAVHUnryjLtE2meVVaiIja2
"""

!wget https://storage.googleapis.com/nicksdemobucket/titanic-train.csv

!ls

import pandas as pd
import numpy as np

df = pd.read_csv("titanic-train.csv")
df.head(10)

df.describe()

#To see what data is missing
total = df.isnull().sum().sort_values(ascending=False)
percent_1 = df.isnull().sum()/df.isnull().count()*100
percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '%'])
missing_data.head(5)

#Fill the missing data for Age with its median, Embarked with mode 0
df['Age'].fillna(df['Age'].median(),inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0],inplace=True)
df.head()

#Convert categorical Sex and Embarked to numerical
df1=pd.get_dummies(df,columns=['Sex','Embarked'])
df1.head(10)

import seaborn as sns
sns.pairplot(df1,vars=["Age","Pclass","Parch","SibSp","Sex_female","Sex_male","Embarked_C","Embarked_Q","Embarked_S","Survived"],hue="Survived")

#Drop PassengerId, Name, Ticket and Cabin (missing many data) since they seem not contributing to Survived
features=df1.drop(['PassengerId','Name','Ticket','Cabin','Survived'],axis=1).values
labels=df1[['Survived']].values
features.shape,labels.shape

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

model = Sequential()
model.add(Dense(30,activation='relu',input_shape=(10,)))
model.add(Dense(30,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(optimizer='adam',
             loss='binary_crossentropy',
             metrics=['accuracy'])

early_stopping_monitor=EarlyStopping(monitor='val_acc', patience=5)
h=model.fit(features,labels,epochs=20,batch_size=25,validation_split=0.3,callbacks=[early_stopping_monitor])

import matplotlib.pyplot as plt

plt.plot(h.history['val_acc'],'b')
plt.plot(h.history['val_loss'],'r')
plt.xlabel('Epochs')
plt.ylabel('Validation score')
plt.show()

model.save("model2_file.h5")

#Try with a new data (just randomly created) to see what probability that person could survive
import numpy as np

some_new_data = np.array([[1.0,38.0,1.0,0.0,14.0,1.0,0.0,0.0,0.0,1.0]])
some_new_data.shape

predicted_labels = model.predict(some_new_data)
predicted_labels
