from itertools import combinations
from logica import *
import matplotlib.pyplot as plt
import networkx as nx
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
        self.aristas_base = [ 
        ('H','G'),('H','B'),('H','E'),('G','A'),('A','B'),('B','C'),('C','D'),('D','E')
        ] 
        recorridos = []
        for u, v in self.aristas_base:
            recorridos.append((u, v))
            recorridos.append((v, u)) 
        turnos = 8
        
        self.To = Descriptor([recorridos, turnos])
        self.To.escribir = MethodType(escribir_grafos, self.To)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        self.reglas = [r1, r2, r3] 

    def regla1(self): 
        #TODO
        return "Por hacer"

    def regla2(self):
        #TODO 
        return "Por hacer"  
    
    def regla3(self): 
        #TODO
        return "Por hacer"  

    def regla4(self):
        #TODO 
        return "Por hacer"    
    def regla5(self):
        #TODO 
        return "Por hacer"   
    
    #ESTA ES UNA FUNCIÓN AUXILIAR PARA VISUALIZAR QUE DEVUELVE UNA TRIPLA ("X","Y",t)
    def triple_conversion(self, atomo): 
        p, t = self.To.unravel(atomo)   
        recorridos = self.To.args_lista[0]
        tupla = recorridos[p]
        return (tupla[0], tupla[1], t)
    

    def visualizar_grafo(self, dict_atomos=""):
        #Creamos una copia para asegurarnos que no pase 
        G = nx.Graph()        
        G.add_edges_from(self.aristas_base)    
        pos = nx.spring_layout(G, seed=6)
    
        plt.figure(figsize=(5, 6))
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
        nx.draw_networkx_labels(G, pos, font_weight='bold')
        nx.draw_networkx_edges(G, pos, width=2, edge_color='lightgray')
        movement_list = [] 
        

        if copia_dict_atomos: # 
            copia_dict_atomos = dict_atomos.copy()
            #IMPORTANTE: DEL DICCIONARIO SOLO TOMAMOS AQUELLOS VALORES QUE SON VERDADEROS
            for atomo in dict_atomos: 
                if copia_dict_atomos[atomo] == True:  
                    #Decodifica el atomo y lo vuelve una tripla
                    triple = self.triple_conversion(atomo)  
                    movement_list.append(triple)

            propiedades_caja = dict(
                boxstyle='round,pad=0.3',
                edgecolor='red',          
                facecolor='white',        
                alpha=0.9                
            )
            
            for triple in movement_list:  
                v1, v2, turno = triple  #Tripla
            
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=[(v1, v2)],
                    edge_color='red',
                    width=4,
                    arrows=True,
                    arrowstyle='->',
                    arrowsize=30
                )

                nx.draw_networkx_edge_labels(
                    G,
                    pos,
                    edge_labels={(v1, v2): f"Turno {turno}"},
                    font_color='red',
                    font_weight='bold',
                    bbox=propiedades_caja
                )
        
        plt.title("Problema de grafos")
        plt.axis('off')
        plt.show()
        

        
        
        
