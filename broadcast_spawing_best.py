import random 
import secrets 
import math
import pandas as pd
import numpy as np
from class_individuo import individuo

##BROADCAST SPAWING (reproduccion sexual externa)
#######################################################################
#Fb = fraccion de los corales existentes que se seleccionan para la reproduccion sexual externa

#La funcion emparejamientos busca aleatoriamente parejas entre los individuos seleccionados para la reproduccion
#Cada individuo seleccionado solo podrá formar parte de una pareja y tener un hijo
#Fuente:https://www.quora.com/How-do-you-create-random-nonrepetitive-pairs-from-a-list-in-Python
#######################################################################
def emparejamientos(lista): 
  random.shuffle(lista) 
  parejas = list(zip(lista[::2],lista[1::2]))
  return(parejas)


#######################################################################


#La función descendencia crea un nuevo individuo a partir de una pareja 
#Se eligen chromosomas al azar de cada parental
#######################################################################
def descendencia(ind_1, ind_2, i):
    descendiente = individuo("individuo_" + str(i + 1))
    descendiente.nanoclay = secrets.choice([ind_1.nanoclay, ind_2.nanoclay])
    descendiente.CNTs = secrets.choice([ind_2.CNTs, ind_2.CNTs])
    descendiente.HDI_GO = secrets.choice([ind_1.HDI_GO, ind_2.HDI_GO])
    descendiente.obt_young(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
    descendiente.obt_impact_strength(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
    descendiente.obt_strain_break(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
    descendiente.obt_tensile_strength(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
	
    return(descendiente)

#######################################################################

