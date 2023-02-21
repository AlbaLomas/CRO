import random 
import secrets 
import math
import pandas as pd
import numpy as np
import itertools
from class_individuo import individuo

#m_young FUNCTION
################################################################################################################
#La funcion m_young compara el modulo de young de dos individuos 
#La puntuacion que se otorga depende de la importancia (porcentaje) de la propiedad en la optimizacion
#El individuo ganador obtiene una puntuacion correspondiente a 1 x porcentaje
#El individuo perdedor obtiene una puntuacion de 0
#Si ambos individuos tienen el mismo valor del modulo ambos obtendran una puntuacion de 0.5 x porcentaje
#La funcion devuelve un diccionario cuyas llaves son los individuos, y los valores las puntuaciones de cada uno
################################################################################################################
################################################################################################################
#t_strength FUNCTION
################################################################################################################
#La funcion t_strength compara el valor de tensile strength de dos individuos 
#La puntuacion que se otorga depende de la importancia (porcentaje) de la propiedad en la optimizacion
#El individuo ganador obtiene una puntuacion correspondiente a 1 x porcentaje
#El individuo perdedor obtiene una puntuacion de 0
#Si ambos individuos tienen el mismo valor de stength ambos obtendran una puntuacion de 0.5 x porcentaje
#La funcion devuelve un diccionario cuyas llaves son los individuos, y los valores las puntuaciones de cada uno
################################################################################################################
################################################################################################################
#st_break FUNCTION
################################################################################################################
#La funcion st_break compara el valor de strain at break de dos individuos 
#La puntuacion que se otorga depende de la importancia (porcentaje) de la propiedad en la optimizacion
#El individuo ganador obtiene una puntuacion correspondiente a 1 x porcentaje
#El individuo perdedor obtiene una puntuacion de 0
#Si ambos individuos tienen el mismo valor de strain at break ambos obtendran una puntuacion de 0.5 x porcentaje
#La funcion devuelve un diccionario cuyas llaves son los individuos, y los valores las puntuaciones de cada uno
################################################################################################################
################################################################################################################
#i_strength FUNCTION
################################################################################################################
#La funcion i_strength compara el valor de tensile strength de dos individuos 
#La puntuacion que se otorga depende de la importancia (porcentaje) de la propiedad en la optimizacion
#El individuo ganador obtiene una puntuacion correspondiente a 1 x porcentaje
#El individuo perdedor obtiene una puntuacion de 0
#Si ambos individuos tienen el mismo valor de stength ambos obtendran una puntuacion de 0.5 x porcentaje
#La funcion devuelve un diccionario cuyas llaves son los individuos, y los valores las puntuaciones de cada uno
################################################################################################################
################################################################################################################
def scoring(ind1, ind2, propiedad, porcentaje):
	score = {}

	if propiedad == "modulo_young":
		individuo1_propiedad = ind1.modulo_young
		individuo2_propiedad = ind2.modulo_young

	elif propiedad == "tensile_strength":
		individuo1_propiedad = ind1.tensile_strength
		individuo2_propiedad = ind2.tensile_strength

	elif propiedad == "strain_at_break":
		individuo1_propiedad = ind1.strain_at_break
		individuo2_propiedad = ind2.strain_at_break

	else:
		individuo1_propiedad = ind1.impact_strength
		individuo2_propiedad = ind2.impact_strength

	#################################################


	if individuo1_propiedad > individuo2_propiedad: 

		score[ind1] = porcentaje * 1
		score[ind2] = porcentaje * 0

	elif individuo1_propiedad  < individuo2_propiedad:

		score[ind2] = porcentaje * 1
		score[ind1] = porcentaje * 0

	else:
		score[ind2] = porcentaje * 0.5
		score[ind1] = porcentaje * 0.5
		
	return(score)

###############################################################################################################
#mergeDictionary FUNCTION
###############################################################################################################
#La funcion mergeDictionary es una funcion auxiliar (buscar procedencia) 
#que une dos diccionarios en uno por los valores de sus llaves
###############################################################################################################
def mergeDictionary(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = [value , dict_1[key]]
   return dict_3
###############################################################################################################
#torneo FUNCTION
###############################################################################################################
#Esta funcion calcula el fitness de los dos individuos a comparar sumando las puntuaciones para cada propiedad
#La funcion devuelve el individuo ganador y el perdedor
###############################################################################################################
def torneo(ind1, ind2):
	young_score = scoring(ind1, ind2, "modulo_young", 0.5 )
	tensile_score = scoring(ind1, ind2, "tensile_strength", 0.2)
	st_break_score = scoring(ind1, ind2, "tensile_strength",0.1)
	impact_strength = scoring(ind1, ind2, "impact_strength", 0.2)

	merge_1 = mergeDictionary(young_score,tensile_score)
	merge_2 = mergeDictionary(st_break_score,impact_strength)
	final_merge = mergeDictionary(merge_1,merge_2)

	#print(final_merge)
	fitness = {}
	for key in final_merge.keys():
		join = list(itertools.chain(*final_merge[key]))
		fitness[key] = sum(join)

	#print(fitness)

	#Torneo:
	if fitness[ind1] > fitness[ind2]:
		ganador = ind1
		perdedor = ind2

	elif fitness[ind1] < fitness[ind2]:
		ganador = ind2
		perdedor = ind1

	else: 

		ganador = ind1
		perdedor = ind2


	return(ganador, perdedor)

###############################################################################################################
#explore_reef FUNCTION
###############################################################################################################
#La funcion explore_reff es una funcion auxiliar que devuelve expora el arrrecife 
#cuadricula por cuadricula y devuelve el valor "empty" si está vacia,
#y el valor "full" si esta ocupada por un coral
###############################################################################################################
def explore_reef(a, b, arrecife):
    if arrecife[a][b] == 0:
        return("empty")
        
    else: 
        return("full")

###############################################################################################################
#larvae_setting_f FUNCTION
###############################################################################################################
#Esta funcion realiza el proceso de fijacion aleatoria de las larvas en el arrecife
#Primero se explora aleatoriamente un punto del arrecife, 
#si esta vacio se produce la fijacion de la larva y pasa a estar dentro de la lista "population",
#si esta ocupado por otro coral se produce una competicion entre el coral y la larva para ver cual es mas apto
#para ocupar el sitio. En el caso de que gane la larva, el coral ocupante es eliminado del arrecife y de la lista
###############################################################################################################
def larvae_setting_f(larva, arrecife, arrecife_names, population, values1, values2):
    coord1 = secrets.choice(values1)
    coord2 = secrets.choice(values2)
    test = explore_reef(coord1, coord2, arrecife)
    

    if test == "empty":
        ganador = larva
        arrecife[coord1][coord2] = larva
        arrecife_names[coord1][coord2] = larva.name
        marcador = "ganador"
        population.append(larva)
    
        return(marcador)
        
    else:
        coral = arrecife[coord1][coord2]
        ganador, perdedor = torneo(coral, larva)  
        if ganador == larva:
            arrecife[coord1][coord2] = larva 
            arrecife_names[coord1][coord2] = larva.name
            marcador = "ganador"
            population.append(larva)
            population.remove(coral)
            
            return(marcador)
            
        else:
            marcador = "perdedor"
            
            return(marcador)
################################################################################################################
