from itertools import combinations
from logica import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from types import MethodType 

def escribir_grafos(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' no'
    else:
        atomo = literal
        neg = ''
    
    # Se descodifica el átomo
    p, t = self.unravel(atomo) 
    
    # p es el índice de la tupla en la lista de recorridos
    # t es el tiempo
    recorridos = self.args_lista[0] # Usamos self en lugar de To
    tupla = recorridos[p]
    
    return f"El vértice {tupla[0]}{neg} va al vértice {tupla[1]} en el turno {t}"

class Grafos:  
    '''Clase para representar el problema de determinar la existencia de 
    un camino en un grafo no dirigido de 7 nodos 
    que conecte el nodo H con el nodo B bajo
    la restricción de recorrer cada arista exactamente una vez'''

def __init__(self): 
        # Definición de las aristas del grafo (no dirigidas)
        aristas_base = [ 
        ('H','G'),('H','B'),('H','E'),('G','A'),('A','B'),('B','C'),('C','D'),('D','E')
        ] 
        recorridos = []
        for u, v in aristas_base:
            recorridos.append((u, v))
            recorridos.append((v, u)) 
        turnos = 8
        
        self.To = Descriptor([recorridos, turnos])
        self.To.escribir = MethodType(escribir_grafos, self.CenC)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        self.reglas = [r1, r2, r3] 

        def regla1(self): 
            #TODO
            pass 

        def regla2(self):
             #TODO 
             pass  
        
        def regla3(self): 
            #TODO
            pass 

        def regla4(self):
             #TODO 
             pass   
        def regla5(self):
             #TODO 
             pass  
        
        def visualizar(self): 
             #TODO 
             pass 
        
        
        
