###########################################################################
#PYTHON PACKAGES
import random 
import secrets 
import pandas as pd
import numpy as np
from class_individuo import individuo
from brooding import brooding_f
from larvae_setting_best import larvae_setting_f
from broadcast_spawing_best import emparejamientos
from broadcast_spawing_best import descendencia
import time

###########################################################################
#Performance time
st = time.time()

#REEF FORMATION
###########################################################################
#REEF DIMENSIONS [m x n]
m = 10
n = 10
num_generations = 5
population_members = 10
population = []
dimension = m * n
f = open("report.txt", "w")

for generation in range(num_generations):
  if generation == 0:
  #arrecife is the multidimensional array for storing individuals 
  #at first it is empty (full of 0) 
    arrecife = [[0 for x in range(n)] for x in range(m)]
    #arrecife_names is created with testing puporses (it will store individulas names)
    arrecife_names = [[0 for x in range(n)] for x in range(m)]
  	############################################################################

  	#CREATE INITIAL POPULATION
  	############################################################################
    for member in range(population_members):
      ind = individuo("individuo_" + str(member))
      naclay = ind.obt_nanoclay()
      cnt = ind.obt_cnts()
      hdi_go = ind.obt_hdi_go()
      ind.obt_young(naclay, cnt, hdi_go)
      ind.obt_tensile_strength(naclay, cnt, hdi_go)
      ind.obt_strain_break(naclay, cnt, hdi_go)
      ind.obt_impact_strength(naclay, cnt, hdi_go)
      population.append(ind)

    #a = number of corals already created (start from 0)
    a = len(population) - 1

    #RANDOMLY FIX INDIVIDUALS ON THE REEF
	  ###########################################################################
    #Now it is necessary to locate each individual in the reef 
    #Each point on the reef is randomly scanned, 
    #if it is unoccupied the individual is fixed, 
    #otherwise it is searched again for another point
    #if the size of the reef is smaller than the number of individuals, 
    #it is not possible to continue, 
    #as there would be no place to fix the individuals

    values1 = list(range(m))
    values2= list(range(n))

    if dimension >= len(population):
      population_located = []
      while len(population) != 0:
        for individuo in population:
          coord1 = secrets.choice(values1)
          coord2 = secrets.choice(values2)
          if arrecife[coord1][coord2] == 0:
            arrecife[coord1][coord2] = individuo
            arrecife_names[coord1][coord2] = individuo.name
            population.remove(individuo)
            population_located.append(individuo)

          else:
            pass

    else: 
      print("Your number of initial corals exceed the number of reef positions")
      sys.exit(0)


	    #Test the fixing
	    #print(arrecife_names)
	###########################################################################

  else:
    population_located = winner_population
    arrecife = arrecife
    arrecife_names = arrecife_names
    a = a
  ##########################################################################
  print("GENERACIÓN" + str(generation) + "\n")
  print("ARRECIFE INICIAL"+ "\n")
  for i in range(0,m):
    print(arrecife_names[i])

  ##########################################################################
  #BROADCAST SPAWING
  ###########################################################################
  #fb = fraction of existing corals that are selected for external sexual reproduction
  #fb = 30%
  fb = round(len(population_located) * 0.3)
  print(fb)
  #water = list to store larvas
  #In each generation water list is emptied
  water = []

  ###ATENCION HAY QUE CAMBIAR POPULATION PORQUE AQUI VAN TODOS Y YO NO QUIERO QUE SE REPRODUZCAN TODOS
  mates = emparejamientos(population_located[:fb])
  print(mates)
  ###Larvas obtaining for sexual external reproduction
  ###Larvas are stored in water list
  for mate in mates:
    indi_des = descendencia(mate[0], mate[1], a)
    water.append(indi_des)
    a +=1
  ##########################################################################

  #BROODING
  ##########################################################################
  #brooding_fraction = 1-fb
  ###ATENCION HAY QUE CAMBIAR POPULATION PORQUE AQUI VAN TODOS Y YO NO QUIERO QUE SE REPRODUZCAN TODOS
  ###Generating new larvas using internal sexual reproduction
  ###brooding_larvas is the list for storing brooding larvas
  #bf = len(population_located) - fb
  brooding_population = population_located[fb:]
  brooding_larvas, a = brooding_f(brooding_population, a)
  #########################################################################

  #Join larvas from both types of reproduction
  water.extend(brooding_larvas)
  #########################################################################
  print("LISTA_AGUA")
  for element in water:
    print(element.name)
  #########################################################################  
  #FIXING LARVAE
  #########################################################################
  #This step is for fixing larvaes from water to the reef
  #Firstly, it is selected a point of the reef. If this point is already occupied,
  #the larvae has to compete with the coral. In case the larvae wins, it would occupy this point
  #and the loser coral is discarded
  #If the point is empty, the larvae is fixed
  #This process is carried out k times when the fixing fails, after k times the larvae is depredated
  #k: number of tries of fixing
  k = 2

  for larva in water:
  	#for each larva the counter is set to 0 
    oportunidad = 0
    #print(larva.name)
    marcador = "perdedor"
    while marcador == "perdedor" and oportunidad <= k:
      marcador = larvae_setting_f(larva, arrecife, arrecife_names, population_located, values1, values2)
      #print(marcador, oportunidad)
      #print(arrecife_names)
      oportunidad += 1  

    pass

  ########################################################################
  print("ARRECIFE DESPUÉS DE FIJAR"+ "\n")
  for i in range(0,m):
    print(arrecife_names[i])
  ##########################################################################
  
  #BUDDING
  ########################################################################
  #Doubling a percentage of corals 
  ##ATENCION EL PORCENTAJE A DUPLICAR SERIA ELEGIDO ENTRE LOS MEJORES
  #POR AHORA SE ELIGE ALEATORIAMENTE ENTRE TODOS LOS CORALES DISPONIBLES

  budding_percentage = 0.4
  budding_num = round(len(population_located) * budding_percentage)

  #¡PROBLEMA! random.sample() ¿puede elegir varias veces el mismo item?
  budding_candidates = random.sample(population_located, budding_num)

  ########################################################################
  #It is used the same function for fixing budding candidates as for larvaes
  for bud in budding_candidates:
  #for each larva the counter is set to 0 
    oportunidad = 0
    #print(bud.name)
    marcador = "perdedor"
    while marcador == "perdedor" and oportunidad <= k:
      marcador = larvae_setting_f(bud, arrecife, arrecife_names, population_located, values1, values2)
      #print(marcador, oportunidad)
      #print(arrecife_names)
      oportunidad += 1  

      pass

  ##########################################################################
  print("ARRECIFE DESPUÉS DE BUDDING"+ "\n")
  for i in range(0,m):
    print(arrecife_names[i])

  print("POPULATION DESPUÉS DE BUDDING"+ "\n")
  for element in population_located:
    print(element.name)
  ##########################################################################
  
  #DEPREDATION PHASE ¿SE PUEDE MEJORAR ESTA PARTE DEL CODIGO?
  ##########################################################################
  #This is the last step of each generation, a percentage of the fixed corals
  #is depredated and removed from the reef
  porcentaje_depredation = 0.2
  depredation_num = round(len(population_located) * porcentaje_depredation)

  #There is random choice of a coral percentage and it is created a dict
  #which keys are the coordinates and the values the individual class
  dict_depreaded = {}
  #targets_list = []
  while len(dict_depreaded) < depredation_num:
    coord1 = secrets.choice(values1)
    coord2 = secrets.choice(values2)
    target = arrecife[coord1][coord2]
    if target != 0:
      dict_depreaded[coord1, coord2] = [target]
      #targets_list.append(target)
    else:
      continue   

    pass

  ##########################################################################
  print("LISTA DE DEPREDADOS"+ "\n")
  print(dict_depreaded)

  ##########################################################################
  #Finally the selected corals are eliminated
  for coords in dict_depreaded.keys():
    target = dict_depreaded[coords]
    arrecife_names[coords[0]][coords[1]] = 0
    arrecife[coords[0]][coords[1]] = 0

  ##########################################################################
  #winner_population is the final list of fixed corals
  winner_population = []
  for i in range(0,m):
    for j in range(0,n):
      if arrecife[i][j] != 0:
        winner_population.append(arrecife[i][j])
      else:
        pass

  #Showing the final population and reef
  print("POPULATION WINNER"+ "\n")
  for i in range(0,m):
    print(arrecife_names[i])

  for element in winner_population:
    print(element.name)

  #Creating a dataframe (df_winners) with the final corals and its chromosomes
  dict_winners = {}
  for member in winner_population:
    dict_winners[member.name] = [member.nanoclay], [member.CNTs], [member.HDI_GO],[member.modulo_young], [member.tensile_strength], [member.strain_at_break], [member.impact_strength]

  df_winners = pd.DataFrame(dict_winners.values(), columns=['Nanoclay', 'CNTs', 'HDI_GO','modulo_young', 'tensile_strength', 'strain_at_break', 'impact_strength'],index=dict_winners.keys()).sort_index()

  #Write the dataframe in report file
  f.write("GANADORES" + "\n")
  f.write(df_winners.to_string(header = True))
  f.write("\n")

  ##########################################################################


et = time.time()
elapsed_time = et - st

f.write("Execution time:" + str(elapsed_time) + "seconds")

print("Execution time:" + str(elapsed_time) + "seconds")
