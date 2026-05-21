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
    recorridos = self.args_lista[0] 
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
        self.turnos = 8
        
        self.To = Descriptor([self.recorridos, self.turnos])
        self.To.escribir = MethodType(escribir_grafos, self.To)
        r1 = self.regla1()
        r2 = self.regla2()
        r3 = self.regla3() 
        r4= self.regla4() 
        r5 = self.regla5()
        self.reglas = [r1, r2, r3,r4,r5] 

    def regla1(self): 
        h_conec = [(a,b) for (a,b) in self.recorridos if a=='H'] 
        formula_final = []
        t = 0

        formula_final = ""

        for recorrido in h_conec: 
            # El inicio es el movimiento actual de H
            # No lleva "-" porque es el primero
            formula_actual = self.To.ravel([recorrido, t])
            
            # Filtramos los otros movimientos
            otros_movimientos = [m for m in self.recorridos if m != recorrido]    
            
            # CONSTRUCCIÓN DE LA FORMULA 
            # Se irá uniendo a la formula actual
            # Por cada iteración vamos concatenando lo que ya teníamos
            for mov in otros_movimientos: 
                formula_actual = "(" + formula_actual + "Y-" + self.To.ravel([mov, t]) + ")"
            
            # Vamos añadiendo cada formula_actual a la formula final
            if formula_final =="":
                formula_final = formula_actual 
            else:
                formula_final = "(" + formula_final + "O" + formula_actual + ")" 
        return formula_final


    def regla2(self):
        b_conec = [(a,b) for (a,b) in self.recorridos if b=='B' ]   

        formula_final = ""
        t = 7

        for recorrido in b_conec: 
            movimiento_actual = recorrido  #
            
            # Filtramos los otros movimientos
            otros_movimientos = [m for m in self.recorridos if m != movimiento_actual]    
            
            formula1 = ""
            inicial = True 
            
            for mov in otros_movimientos: 
                if inicial: 
                    formula1 = "-" + self.To.ravel([mov, t]) 
                    inicial = False 
                else: 
                    formula1 = "(" + formula1 + "Y-" + self.To.ravel([mov, t]) + ")" 
            
            bloque_actual = "(" + self.To.ravel([movimiento_actual, t]) + "Y" + formula1 + ")" 
            
            if formula_final == "":
                formula_final = bloque_actual 
            else:
                formula_final = "(" + formula_final + "O" + bloque_actual + ")"

        return formula_final
    
    def regla3(self):
        formula_final_lista = []

        # Recorremos cada arista NO DIRIGIDA
        for (v1, v2) in self.aristas_base:

            formula_turnos = ""

            # Para cada turno
            for t in range(self.turnos):

                # Dirección ida
                atomo1 = self.To.ravel([(v1, v2), t])

                # Dirección vuelta
                atomo2 = self.To.ravel([(v2, v1), t])


                bloque_turno = "(" + atomo1 + "O" + atomo2 + ")"

                # Armaremos la Otoria manualmente
                if formula_turnos == "":
                    formula_turnos = bloque_turno
                else:
                    formula_turnos = "(" + formula_turnos + "O" + bloque_turno + ")"

            # Guardamos la fórmula completa de esta arista
            formula_final_lista.append(formula_turnos)

    # Ytoria entre todas las aristas
        formula_final = formula_final_lista[0]

        for f in formula_final_lista[1:]:
            formula_final = "(" + formula_final + "Y" + f + ")"

        return formula_final

    def regla4(self):
        
        from itertools import combinations
    
        clausulas = []
    
        # Para cada arista base, ninguna de sus dos direcciones puede aparecer
        # en más de un turno. Tomamos todos los pares de turnos posibles.
        for (v1, v2) in self.aristas_base:
            # Todos los átomos relacionados con esta arista (ambas direcciones, todos los turnos)
            atomos_arista = []
            for t in range(self.turnos):
                atomos_arista.append(self.To.ravel([(v1, v2), t]))
                atomos_arista.append(self.To.ravel([(v2, v1), t]))
        
            # Para cada par de átomos, no pueden ser ambos verdaderos
            for a1, a2 in combinations(atomos_arista, 2):
                clausulas.append(f"(-{a1}O-{a2})")
    
        return Ytoria(clausulas) 
    


    def regla5(self):
        formula_lista = []  
        for t in range(1, self.turnos):
            for (i, j) in self.recorridos:

                # disyunción de todos los (j,k) en recorridos 
                salidas_desde_j = [(a, b) for (a, b) in self.recorridos if a == j]

                inicial = True
                formula_consecuente = ''
                for (a, b) in salidas_desde_j:
                    atomo = self.To.ravel([(a, b), t])
                    if inicial:
                        formula_consecuente = atomo
                        inicial = False
                    else:
                        formula_consecuente = "(" + formula_consecuente + "O" + atomo + ")"

                # antecedente: To(i,j,t-1)
                formula_antecedente = self.To.ravel([(i, j), t - 1])

                # implicación: (antecedente > consecuente) 
                formula_implicacion = "(" + formula_antecedente + ">" + formula_consecuente + ")"
                formula_lista.append(formula_implicacion)

        # conjunción de todas las implicaciones (cebolla con Y) 
        formula_completa = formula_lista[0]
        for f in formula_lista[1:]:
            formula_completa = "(" + formula_completa + "Y" + f + ")"

        return formula_completa  
    

    '''
    -----------------------------------VISUALIZAR_GRAFO-------------------------
    '''

    #ESTA ES UNA FUNCIÓN AUXILIAR QUE DEVUELVE UNA TRIPLA ("X","Y",t)
    def triple_conversion(self, atomo): 
        p, t = self.To.unravel(atomo)   
        recorridos = self.To.args_lista[0]
        tupla = recorridos[p]
        return (tupla[0], tupla[1], t)
    

    def visualizar_grafo(self, dict_atomos=None, custom_size=(5,6)):    
        
        
        plt.figure(figsize=custom_size)  
        G = nx.Graph()        
        G.add_edges_from(self.aristas_base)    
        pos = {
            #Cuadramos posiciones para que se vea como en el gráfico del enunciado
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
            #{(TUPLA1):[TIEMPOS], (TUPLA2):[TIEMPOS]}
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
                #Dibujamos las etiquetas de los turnos en los vertices ocupados
                nx.draw_networkx_edge_labels(
                    G,
                    pos,
                    edge_labels={(v1, v2): f"Turno {','.join(map(str, aristas_ocupadas[(v1,v2)]))}"},
                    font_color='red',
                    font_weight='bold',
                    bbox=propiedades_caja
                ) 
        
        plt.title("Problema de grafos")
        plt.axis('off')
        plt.show()
        

        
        
        
