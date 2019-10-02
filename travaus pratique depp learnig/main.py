import resaus_de_neurone as rdn
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3: 13].values
y = dataset.iloc[:, 13].values

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]
print(type(X))
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)



consturucteur = rdn.reseau()

consturucteur.add(8, "sigmoide", couche_dantre = 11)
consturucteur.add(6, "sigmoide")
consturucteur.add(1, "sigmoide")



consturucteur.compile()

consturucteur.fit(X_train, y_train, batch_size = 10, epochs = 100)



predictions = consturucteur.predict(X_test, seuie = 0.5)


poursentage = consturucteur.prousentage(y_test, predictions)