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
        self.recorridos = []
        for u, v in self.aristas_base:
            self.recorridos.append((u, v))
            self.recorridos.append((v, u)) 
        turnos = 8
        
        self.To = Descriptor([self.recorridos, turnos])
        self.To.escribir = MethodType(escribir_grafos, self.To)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3()
        self.reglas = [r1, r2, r3] 

    def regla1(self): 
        h_conec = [(a,b) for (a,b) in self.recorridos if a=='H'] 
        formula_final = []
        t = 1

        formula_final = ""

        for recorrido in h_conec: 
            # El inicio es el movimiento actual de H
            # No lleva "-" porque este es el que "ocurre"
            formula_actual = self.To.ravel([recorrido, t])
            
            # Filtramos los otros movimientos
            otros_movimientos = [m for m in self.recorridos if m != recorrido]    
            
            # CONSTRUCCIÓN DE LA FORMULA
            # Por cada iteración vamos concatenando lo que ya teníamos
            for mov in otros_movimientos: 
                formula_actual = "(" + formula_actual + "Y-" + self.To.ravel([mov, t]) + ")"
            
            # VAMOS AÑADIENDO A LA FORMULA FINAL LAS FORMULAS QUE VAMOS HACIENDO
            if formula_final =="":
                formula_final = formula_actual 
            else:
                formula_final = "(" + formula_final + "O" + formula_actual + ")" 
        return formula_final


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
    

    def visualizar_grafo(self, dict_atomos=None):   
        plt.figure(figsize=(5, 6))
        G = nx.Graph()        
        G.add_edges_from(self.aristas_base)    
        pos = {
            'C': (1, 2), 'D': (3, 2),
            'A': (0, 1), 'B': (2, 1), 'E': (4, 1),
            'G': (1, 0), 'H': (3, 0)
        } 
        nx.draw_networkx_nodes(G, pos, node_color='white', node_size=1000,  edgecolors="black")
        nx.draw_networkx_labels(G, pos, font_weight='bold')
        nx.draw_networkx_edges(G, pos, width=2, edge_color='black',)
        
        if dict_atomos is not None: 
            movement_list = [] 
            #IMPORTANTE: DEL DICCIONARIO SOLO TOMAMOS AQUELLOS VALORES QUE SON VERDADEROS
            for atomo in dict_atomos: 
                if dict_atomos[atomo] == True:  
                    #Decodifica el atomo y lo vuelve una tripla
                    triple = self.triple_conversion(atomo)  
                    movement_list.append(triple)

            propiedades_caja = dict(
                boxstyle='round,pad=0.3',
                edgecolor='red',          
                facecolor='white',        
                alpha=0.9                
            )
            #NO QUEREMOS QUE UN TIEMPO TAPE AL OTRO, ASI QUE CADA VEZ QUE SE REPITAN LAS ARISTAS 
            #IREMOS ACUMULANDO LOS TIEMPOS MEDIANTE UN DICCIONARIO QUE TENDRÁ LA FORMA DE 
            #{(TUPLA1):[TIEMPOS], (TUPLA2):[TIEMPOS]
            aristas_ocupadas = {}

            for triple in movement_list:  
                v1, v2, turno = triple  #Tripla

                #PEQUEÑO ALGORITMO PARA QUE SE GUARDEN LOS TIEMPOS DE CADA ARISTA EN UNA LISTA
                if((v1,v2) not in aristas_ocupadas):
                    aristas_ocupadas[v1,v2] =[turno]
                    aristas_ocupadas[v2,v1] = [turno]
                else:
                    item_aristas1 = aristas_ocupadas.get((v1,v2), f"ERROR OBTENIENDO LA INFORMACIÓN DE LA ARISTA {v1},{v2}") 
                    item_aristas2 = aristas_ocupadas.get((v2,v1), f"ERROR OBTENIENDO LA INFORMACIÓN DE LA ARISTA {v1},{v2}")
                    
                    item_aristas1.append(turno) 
                    item_aristas2.append(turno) 

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
                    edge_labels={(v1, v2): f"Turno {",".join(map(str, aristas_ocupadas[(v1,v2)]))}"},
                    font_color='red',
                    font_weight='bold',
                    bbox=propiedades_caja
                ) 
        
        plt.title("Problema de grafos")
        plt.axis('off')
        plt.show()
        

        
        
        
