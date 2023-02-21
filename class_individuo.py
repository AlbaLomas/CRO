import random 
import secrets 
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import Flatten, Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D, Dropout 
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD


######PROVISIONAL ANN FOR TESTING CRO ALGORITHM 
#########################################################################################################
FILENAME = "data_2.csv"

# Descargar el set de datos.
dataset = pd.read_csv(FILENAME)

dataset1 = dataset.to_numpy()

#Calcular el numero de filas que se utilizaran tanto para el test como el train set
n_train = round(dataset1.shape[0]* 0.75)

#SET DE ENTRENAMIENTO
X = dataset1[:n_train,1:4]
Y = dataset1[:n_train,4:5]
#SET DE TRAINING
test_data = dataset1[(n_train+1):,1:4]
test_targets = dataset1[(n_train+1):,4:5]

#Modelo de red neuronal
def build_model():
    activation = tf.keras.layers.LeakyReLU(alpha=0.3)
    model1 = keras.Sequential([
        layers.Dense(55, activation=activation, input_shape=[3]),
        layers.Dense(90, activation=activation),
        layers.Dense(55, activation=activation),
        layers.Dense(4, activation = "linear")
    ])

    optimizer2 = tf.keras.optimizers.Adam(learning_rate=0.001)
    optimizer3 = tf.keras.optimizers.RMSprop(0.001)
    model1.compile(optimizer=optimizer2,loss= "mse", metrics=['mae', 'mse'])

    return(model1)
  

model = build_model()

#Entrenamiento del modelo
history = model.fit(X,Y, batch_size=15, epochs=350, validation_split = 0.2, verbose=0)
##########################################################################################################


#CLASS CONTAINING THE CHROMOSOMES OF POSSIBLE SOLUTIONS
##########################################################################################################
class individuo:
	def __init__(self, name):
		self.name = name
		self.nanoclay = self.obt_nanoclay()
		self.CNTs = self.obt_cnts()
		self.HDI_GO = self.obt_hdi_go()
		self.modulo_young = self.obt_young(self.nanoclay, self.CNTs, self.HDI_GO)
		self.tensile_strength = self.obt_tensile_strength(self.nanoclay, self.CNTs, self.HDI_GO)
		self.strain_at_break = self.obt_strain_break(self.nanoclay, self.CNTs, self.HDI_GO)
		self.impact_strength = self.obt_impact_strength(self.nanoclay, self.CNTs, self.HDI_GO)
		
	def obt_nanoclay(self):
		nanoclay = random.randint(0,5)
		return(nanoclay)

	def obt_cnts(self):
		cnts = random.randint(0,5)
		return(cnts)

	def obt_hdi_go(self):
		hdi_go= random.randint(0,5)
		return(hdi_go)

	def obtain_all(self, nanoclay, CNTs, HDI_GO):
		lst = [[nanoclay, CNTs, HDI_GO]]
		arr = np.array(lst)
		result = model.predict(arr)
		return(result)

	def obt_tensile_strength(self, nanoclay, CNTs, HDI_GO):
		result = self.obtain_all(nanoclay, CNTs, HDI_GO)
		tensile_strength = float(result[:,1]) * 10
		return(tensile_strength)

	def obt_strain_break(self, nanoclay, CNTs, HDI_GO):
		result = self.obtain_all(nanoclay, CNTs, HDI_GO)
		strain_at_break = float(result[:,2])
		return(strain_at_break)

	def obt_impact_strength(self, nanoclay, CNTs, HDI_GO):
		result = self.obtain_all(nanoclay, CNTs, HDI_GO)
		impact_strength = float(result[:,3]) * 10
		return(impact_strength)

	def obt_young(self, nanoclay, CNTs, HDI_GO):
		result = self.obtain_all(nanoclay, CNTs, HDI_GO)
		modulo_young = float(result[:,0])
		return(modulo_young) 