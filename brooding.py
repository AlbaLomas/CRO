import random 
import secrets 
import math
import pandas as pd
import numpy as np
from class_individuo import individuo

#BROODING (reproducción sexual interna)
#La funcion broading se encarga de obtener larvas por autofecundacion de los parentales
#Las larvas son copias de los parentales con una mutacion en uno de sus cromosomas
#######################################################################################
def brooding_f(lista_individuos,i):
    #mutamos
    opt_mutacion = ["naclay", "cnt", "hdi_go"]
    brooding_larvas = []
    for clase in lista_individuos:
        descendiente = individuo("individuo_" + str(i + 1))
        objetivo = secrets.choice(opt_mutacion)
        #print(objetivo)
        
        if objetivo == "naclay":
            descendiente.nanoclay = descendiente.obt_nanoclay()
            descendiente.CNTs = clase.CNTs
            descendiente.HDI_GO = clase.HDI_GO
            
        elif objetivo == "cnt":
            descendiente.nanoclay = clase.nanoclay
            descendiente.CNTs = descendiente.obt_cnts()
            descendiente.HDI_GO = clase.HDI_GO
        
        else:
            descendiente.nanoclay = clase.nanoclay
            descendiente.CNTs = clase.CNTs
            descendiente.HDI_GO = descendiente.HDI_GO
            
        
        descendiente.modulo_young = descendiente.obt_young(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
        descendiente.tensile_strength = descendiente.obt_tensile_strength(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
        descendiente.strain_at_break = descendiente.obt_strain_break(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
        descendiente.impact_strength = descendiente.obt_impact_strength(descendiente.nanoclay, descendiente.CNTs, descendiente.HDI_GO)
      
        brooding_larvas.append(descendiente)
        
        i += 1
    
    return(brooding_larvas, i)
#######################################################################################
