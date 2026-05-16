from itertools import product
import numpy as np
from copy import deepcopy
from typing import List, Dict 
from random import choice, uniform, randint


'''
Librería con las clases y funciones
para lógica proposicional
'''
''' 
CÓDIGO PARA PROYECTO DE LÓGICA
'''

from typing import Set, List, Dict
from itertools import product
import numpy as np

CONECTIVOS = ['-', 'Y','O','>','=']
CONECTIVOS_BINARIOS = ['Y','O','>','=']


class Formula :

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        if type(self) == Letra:
            return self.letra
        elif type(self) == Negacion:
            return '-' + str(self.subf)
        elif type(self) == Binario:
            return "(" + str(self.left) + self.conectivo + str(self.right) + ")"

    def letras(self):
        if type(self) == Letra:
            return set(self.letra)
        elif type(self) == Negacion:
            return self.subf.letras()
        elif type(self) == Binario:
            return self.left.letras().union(self.right.letras())

    def subforms(self) -> List[str]:
        if type(self) == Letra:
            return [str(self)]
        elif type(self) == Negacion:
            return list(set([str(self)] + self.subf.subforms()))
        elif type(self) == Binario:
            return list(set([str(self)] + self.left.subforms() + self.right.subforms())) 
    def num_conec(self):
        if type(self) == Letra:
            return 0
        elif type(self) == Negacion:
            return 1 + self.subf.num_conec()
        elif type(self) == Binario:
            return 1 + self.left.num_conec() + self.right.num_conec()

    def valor(self, I:Dict[str, bool]) -> bool:
        if type(self) == Letra:
            return I[self.letra]
        elif type(self) == Negacion:
            return not self.subf.valor(I)
        elif type(self) == Binario:
            if self.conectivo == 'Y':
                return self.left.valor(I) and self.right.valor(I)
            if self.conectivo == 'O':
                return self.left.valor(I) or self.right.valor(I)
            if self.conectivo == '>':
                return not self.left.valor(I) or self.right.valor(I)
            if self.conectivo == '=':
                return (self.left.valor(I) and self.right.valor(I)) or (not self.left.valor(I) and not self.right.valor(I))
    def SATtabla(self):
        letras = list(self.letras())
        n = len(letras)
        valores = list(product([True, False], repeat=n))
        for v in valores:
            I = {letras[x]: v[x] for x in range(n)}
            if self.valor(I):
                return I
        return None 
    def clasifica_para_tableaux(self):
        if type(self) == Letra:
            return None, 'literal'
        elif type(self) == Negacion:
            if type(self.subf) == Letra:
                return None, 'literal'
            elif type(self.subf) == Negacion:
                return 1, 'alfa'
            elif type(self.subf) == Binario:
                if self.subf.conectivo == 'O':
                    return 3, 'alfa'
                elif self.subf.conectivo == '>':
                    return 4, 'alfa'
                elif self.subf.conectivo == 'Y':
                    return 1, 'beta'
        elif type(self) == Binario:
            if self.conectivo == 'Y':
                return 2, 'alfa'
            elif self.conectivo == 'O':
                return 2, 'beta'
            elif self.conectivo == '>':
                return 3, 'beta' 
    def SATtableaux_anchura(self):
        estado = nodos_tableaux([self])
        res = estado.es_hoja()
        if res == 'cerrada':
            return None
        elif res == 'abierta':
            return estado.interp()
        frontera = [estado]
        while len(frontera) > 0:
            estado = frontera.pop(0)
            hijos = estado.expandir()
            for a in hijos:
                if a != None:
                    res = a.es_hoja()
                    if res == 'abierta':
                        return a.interp()
                    elif res == None:
                        frontera.append(a)
        return None 
    def SATtableaux_profundidad(self):
        estado = nodos_tableaux([self])
        res = estado.es_hoja()
        if res == 'cerrada':
            return None
        elif res == 'abierta':
            return estado.interp()
        frontera = [estado]
        while len(frontera) > 0:
            estado = frontera.pop(0)
            hijos = estado.expandir()
            for a in hijos:
                if a != None:
                    res = a.es_hoja()
                    if res == 'abierta':
                        return a.interp()
                    elif res == None:
                        frontera.append(a)
        return None  
    def SATtableaux_backtracking(self, nodo=None):
        # 1. Para la primera llamada transformamos la fórmula a nodo
        if nodo is None:
            estado = nodos_tableaux([self])
        else:
            # 2. Para las recursiones ya son nodos asi que no pasa nada
            estado = nodo
        res = estado.es_hoja()
        if res == 'cerrada':
            return None
        elif res == 'abierta':
            return estado.interp()
        for hijo in estado.expandir(): 
            resultado = self.SATtableaux_backtracking(hijo) 
            if resultado != None: 
                return resultado
        return None 
    
    
    def ver(self, D):
        '''
        Visualiza una fórmula A (como string en notación inorder) usando el descriptor D
        '''
        vis = []
        A = str(self)
        for c in A:
            if c == '-':
                vis.append(' no ')
            elif c in ['(', ')']:
                vis.append(c)
            elif c in ['>', 'Y', 'O']:
                vis.append(' ' + c + ' ')
            elif c == '=':
                vis.append(' sii ')
            else:
                try:
                    vis.append(D.escribir(c))
                except:
                    raise("¡Caracter inválido!")
        return ''.join(vis) 
    
    def eliminar_imp(self):
        if type(self) == Letra:
            return self
        elif type(self) == Negacion:
            return Negacion(self.subf.eliminar_imp())
        elif type(self) == Binario:
            if self.conectivo == '>':
                return Binario('O',
                               Negacion(self.left.eliminar_imp()),
                               self.right.eliminar_imp()
                              )
            else:
                return Binario(self.conectivo,
                               self.left.eliminar_imp(),
                               self.right.eliminar_imp()
                              )

    def eliminar_doble_imp(self):
        if type(self) == Letra:
            return self
        elif type(self) == Negacion:
            return Negacion(self.subf.eliminar_doble_imp())
        elif type(self) == Binario:
            if self.conectivo == '=':
                return Binario('Y',
                               Binario('O',
                                   Negacion(self.left.eliminar_doble_imp()),
                                   self.right.eliminar_doble_imp(),
                                  ),
                               Binario('O',
                                   Negacion(self.right.eliminar_doble_imp()),
                                   self.left.eliminar_doble_imp(),
                                  ))
            else:
                return Binario(self.conectivo,
                           self.left.eliminar_doble_imp(),
                           self.right.eliminar_doble_imp()
                          )

    def eliminar_doble_negacion(self):
        if type(self) == Letra:
            return self
        elif type(self) == Negacion:
            if type(self.subf) == Negacion:
                return deepcopy(self.subf.subf.eliminar_doble_negacion())
            else:
                return Negacion(self.subf.eliminar_doble_negacion())
        elif type(self) == Binario:
            return Binario(self.conectivo,
                           self.left.eliminar_doble_negacion(),
                           self.right.eliminar_doble_negacion())

    def cambiar_de_morgan_y(self):
        if type(self) == Letra:
            return self
        elif type(self) == Negacion:
            if type(self.subf) == Binario:
                if self.subf.conectivo == 'Y':
                    return Binario('O',
                                   Negacion(self.subf.left.cambiar_de_morgan_y()),
                                   Negacion(self.subf.right.cambiar_de_morgan_y())
                                  )
                else:
                    return Negacion(self.subf.cambiar_de_morgan_y())
            else:
                return Negacion(self.subf.cambiar_de_morgan_y())
        elif type(self) == Binario:
            return Binario(self.conectivo,
                           self.left.cambiar_de_morgan_y(),
                           self.right.cambiar_de_morgan_y()
                          )

    def cambiar_de_morgan_o(self):
        if type(self) == Letra:
            return self
        elif type(self) == Negacion:
            if type(self.subf) == Binario:
                if self.subf.conectivo == 'O':
                    return Binario('Y',
                                   Negacion(self.subf.left.cambiar_de_morgan_o()),
                                   Negacion(self.subf.right.cambiar_de_morgan_o())
                                  )
                else:
                    return Negacion(self.subf.cambiar_de_morgan_o())
            else:
                return Negacion(self.subf.cambiar_de_morgan_o())
        elif type(self) == Binario:
            return Binario(self.conectivo,
                           self.left.cambiar_de_morgan_o(),
                           self.right.cambiar_de_morgan_o()
                          )

    def distribuir_o_en_y(self):
        if type(self) == Letra:
            return self
        elif type(self) == Negacion:
            return Negacion(self.subf.distribuir_o_en_y())
        elif type(self) == Binario:
            if self.conectivo == 'O':
                # print('O')
                if type(self.right) == Binario:
                    # print('right binario')
                    if self.right.conectivo == 'Y': # B O (C Y D)
                        # print('right Y')
                        B = self.left.distribuir_o_en_y()
                        C = self.right.left.distribuir_o_en_y()
                        D = self.right.right.distribuir_o_en_y()
                        return Binario('Y',
                                       Binario('O', B, C),
                                       Binario('O', B, D)
                                      )
                if type(self.left) == Binario:
                    # print('left binario')
                    if self.left.conectivo == 'Y': # (B Y C) O D
                        # print('left Y')
                        B = self.left.left.distribuir_o_en_y()
                        C = self.left.right.distribuir_o_en_y()
                        D = self.right.distribuir_o_en_y()
                        return Binario('Y',
                                       Binario('O', B, D),
                                       Binario('O', C, D)
                                      )
        return Binario(self.conectivo,
                       self.left.distribuir_o_en_y(),
                       self.right.distribuir_o_en_y()
                      )

class Letra(Formula) :
    def __init__ (self, letra:str) :
        self.letra = letra

class Negacion(Formula) :
    def __init__(self, subf:Formula) :
        self.subf = subf

class Binario(Formula) :
    def __init__(self, conectivo:str, left:Formula, right:Formula) :
        assert(conectivo in CONECTIVOS_BINARIOS), f'Símbolo {conectivo} no es aceptado como conectivo binario. Debe usar uno de {CONECTIVOS_BINARIOS}'
        self.conectivo = conectivo
        self.left = left
        self.right = right
        

def inorder_to_tree(cadena:str) -> Formula:
    if len(cadena) == 1:
        assert(cadena not in CONECTIVOS)
        return Letra(cadena)
    elif cadena[0] == '-':
        return Negacion(inorder_to_tree(cadena[1:]))
    elif cadena[0] == "(":
        assert(cadena[-1] == ")"), f'¡Cadena inválida! Falta un paréntesis final en {cadena}'
        counter = 0 #Contador de parentesis
        for i in range(1, len(cadena)):
            if cadena[i] == "(":
                counter += 1
            elif cadena[i] == ")":
                counter -=1
            # ------ CORRECCIÓN AQUÍ ------
            elif cadena[i] in CONECTIVOS_BINARIOS and counter == 0:
            # -----------------------------
                return Binario(cadena[i], inorder_to_tree(cadena[1:i]),inorder_to_tree(cadena[i + 1:-1]))
    else:
        raise Exception('¡Cadena inválida! Revise la composición de paréntesis de la fórmula.\nRecuerde que solo los conectivos binarios incluyen paréntesis en la fórmula.')
        
        
class Descriptor :

    '''
    Codifica un descriptor de N argumentos mediante un solo caracter
    Input:  args_lista, lista con el total de opciones para cada
                     argumento del descriptor
            chrInit, entero que determina el comienzo de la codificación chr()
    Output: str de longitud 1
    '''

    def __init__ (self,args_lista,chrInit=256) -> None:
        self.args_lista = args_lista #Argumentos
        assert len(args_lista) > 0, "Debe haber por lo menos un argumento"
        self.chrInit = chrInit #Caracter inicial para codificar (256)
        self.rango = [chrInit, chrInit + len(args_lista[0])*args_lista[1]] #Todas las letras proposicionales 

        assert type(args_lista[0]) == list, "El primer valor debe ser una lista con tuplas"
        for i in args_lista[0]: 
            assert type(i) == tuple, f"Error: {i} no es una tupla"
        
        assert type(args_lista[1]) == int, "El segundo valor debe ser un entero"

    def check_lista_valores(self,lista_valores) -> None: 
        #CLAVE: EN EL ARGUMENTO 1 DE LISTA VALORES DEBE HABER UNA TUPLA Y EN EL ARGUMENTO 2 
        #UN TIEMPO 
        #lista_valores[0]: Una tupla (A,B) que representa que el vértice A se dirige al vértice B

        #Verificamos que el formato sea [('A','B'), int tiempo]
        assert type(lista_valores[0]) == tuple, "El primer valor debe ser una tupla"
        assert type(lista_valores[1]) == int, "El segundo valor debe ser un entero"    

        #Verificamos que la tupla ingresada se encuentre en args_lista[0]        
        assert lista_valores[0] in self.args_lista[0], f"Error: {lista_valores[0]} no está presente en {self.args_lista[0]}"
        #Condición del tiempo máximo tiempo=8: 
        assert lista_valores[1]<= self.args_lista[1] and lista_valores[1] >= 0


    #Se quito la condición de que lista_valores debe ser unicamente de enteros
    def codifica(self,lista_valores) -> int:
        # Se crea una copia para no modificar la lista original ingresada
        valores = list(lista_valores) 
        self.check_lista_valores(valores) 
        
        # Convertimos la tupla en su índice numérico (0 a 15) de esta manera se comportará como un entero
        valores[0] = self.args_lista[0].index(valores[0]) 
        
        cod = valores[0]
        n_columnas = 1

        
        for i in range(0, len(lista_valores) - 1) :
            #n_columnas se va a multiplicar por la longitud de la tupla en la primera iteración y por 
            #la cantidad de turnos en el 
            
            dimension = len(self.args_lista[i]) if isinstance(self.args_lista[i], list) else self.args_lista[i]
            n_columnas = n_columnas * dimension
            cod = n_columnas * valores[i+1] + cod
        return cod

    def decodifica(self,n: int) -> int:
        decods = [] 
        # 1. Creamos una lista de ENTEROS con las dimensiones
        # Si el argumento es una lista se usa len()
        # Si ya es un entero (como el tiempo 8), lo dejamos igual
        dimensiones = [len(x) if isinstance(x, list) else x for x in self.args_lista]
        if len(self.args_lista) > 1:
            for i in range(0, len(dimensiones) - 1) :
                #Recibe una lista de enteros con las dimeniones [16,8]
                n_columnas = np.prod(dimensiones[:-(i+1)]) 

                #Se extrae el indice de la posición actual
                decods.insert(0, int(n / n_columnas)) 
                #Se actualiza n con el residuo
                n = n % n_columnas

        # 5. El último valor se saca con el primer tamaño de la lista
        decods.insert(0, n % dimensiones[0])
        return decods

    #Se quito la restricción de que la lista debe ser unicamente de enteros
    def ravel(self,lista_valores) -> chr:
        codigo = self.codifica(lista_valores)
        return chr(self.chrInit+codigo)

    def unravel(self,codigo: chr) -> int:
        n = ord(codigo)-self.chrInit
        return self.decodifica(n)
    
    def escribir(self, literal: chr) -> str:
        if '-' in literal:
            atomo = literal[1:]
            neg = ' no'
        else:
            atomo = literal
            neg = ''
        x, y, n  = self.unravel(atomo)
        return f"PREDICADO({x, y, n})"        
    
  

def visualizar_formula(A: Formula, D: Descriptor) -> str:
    '''
    Visualiza una fórmula A (como string en notación inorder) usando el descriptor D
    '''
    vis = []
    for c in A:
        if c == '-':
            vis.append(' no ')
        elif c in ['(', ')']:
            vis.append(c)
        elif c in ['>', 'Y', 'O']:
            vis.append(' ' + c + ' ')
        elif c == '=':
            vis.append(' sii ')
        else:
            try:
                vis.append(D.escribir(c))
            except:
                raise("¡Caracter inválido!")
    return ''.join(vis)
def Ytoria(lista_forms):
    form = ''
    inicial = True
    for f in lista_forms:
        if inicial:
            form = f
            inicial = False
        else:
            form = '(' + form + 'Y' + f + ')'
    return form

def Otoria(lista_forms):
    form = ''
    inicial = True
    for f in lista_forms:
        if inicial:
            form = f
            inicial = False
        else:
            form = '(' + form + 'O' + f + ')'
    return form 



class nodos_tableaux:

    def __init__(self, fs):
        clasfs = [(A, str(A), *A.clasifica_para_tableaux()) for A in fs]
        self.alfas = [c for c in clasfs if c[3] == 'alfa']
        self.betas = [c for c in clasfs if c[3] == 'beta']
        self.literales = [c for c in clasfs if c[3] == 'literal']

    def __str__(self):
        cadena = f'Alfas:{[str(c[1]) for c in self.alfas]}\n'
        cadena += f'Betas:{[str(c[1]) for c in self.betas]}\n'
        cadena += f'Literales:{[str(c[1]) for c in self.literales]}'
        return cadena

    def tiene_lit_comp(self):
        lits = [c[1] for c in self.literales]
        l_pos = [l for l in lits if '-' not in l]
        l_negs = [l[1:] for l in lits if '-' in l]
        return len(set(l_pos).intersection(set(l_negs))) > 0

    def es_hoja(self):
        if self.tiene_lit_comp():
            return 'cerrada'
        elif ((len(self.alfas) == 0) and (len(self.betas) == 0)):
            return 'abierta'
        else:
            return None

    def interp(self):
        I = {}
        for lit in self.literales:
            l = lit[1]
            if '-' not in l:
                I[l] = True
            else:
                I[l[1:]] = False
        return I

    def expandir(self):
        '''Escoge última alfa, si no última beta, si no None'''
        f_alfas = deepcopy(self.alfas)
        f_betas = deepcopy(self.betas)
        f_literales = deepcopy(self.literales)
        if len(self.alfas) > 0:
            f, s, num_regla, cl = f_alfas.pop(0)
            if num_regla == 1:
                formulas = [f.subf.subf]
            elif num_regla == 2:
                formulas = [f.left, f.right]
            elif num_regla == 3:
                formulas = [Negacion(f.subf.left), Negacion(f.subf.right)]
            elif num_regla == 4:
                formulas = [f.subf.left, Negacion(f.subf.right)]
            for nueva_f in formulas:
                clasf = nueva_f.clasifica_para_tableaux()
                if clasf[1]== 'alfa':
                    lista = f_alfas
                elif clasf[1]== 'beta':
                    lista = f_betas
                elif clasf[1]== 'literal':
                    lista = f_literales
                strs = [c[1] for c in lista]
                if str(nueva_f) not in strs:
                    lista.append((nueva_f, str(nueva_f), *clasf))
            nuevo_nodo = nodos_tableaux([])
            nuevo_nodo.alfas = f_alfas
            nuevo_nodo.betas = f_betas
            nuevo_nodo.literales = f_literales
            return [nuevo_nodo]
        elif len(self.betas) > 0:
            f, s, num_regla, cl = f_betas.pop(0)
            if num_regla == 1:
                B1 = Negacion(f.subf.left)
                B2 = Negacion(f.subf.right)
            elif num_regla == 2:
                B1 = f.left
                B2 = f.right
            elif num_regla == 3:
                B1 = Negacion(f.left)
                B2 = f.right
            f_alfas2 = deepcopy(f_alfas)
            f_betas2 = deepcopy(f_betas)
            f_literales2 = deepcopy(f_literales)
            clasf = B1.clasifica_para_tableaux()
            if clasf[1]== 'alfa':
                lista = f_alfas
            elif clasf[1]== 'beta':
                lista = f_betas
            elif clasf[1]== 'literal':
                lista = f_literales
            strs = [c[1] for c in lista]
            if str(B1) not in strs:
                lista.append((B1, str(B1), *clasf))
            clasf = B2.clasifica_para_tableaux()
            if clasf[1]== 'alfa':
                lista = f_alfas2
            elif clasf[1]== 'beta':
                lista = f_betas2
            elif clasf[1]== 'literal':
                lista = f_literales2
            strs = [c[1] for c in lista]
            if str(B2) not in strs:
                lista.append((B2, str(B2), *clasf))
            n1 = nodos_tableaux([])
            n1.alfas = f_alfas
            n1.betas = f_betas
            n1.literales = f_literales
            n2 = nodos_tableaux([])
            n2.alfas = f_alfas2
            n2.betas = f_betas2
            n2.literales = f_literales2
            return [n1, n2]
        else:
            return [] 
    
def a_clausal(A):
    # Subrutina de Tseitin para encontrar la FNC de
    # la formula en la pila
    # Input: A (cadena) de la forma
    #                   p=-q
    #                   p=(qYr)
    #                   p=(qOr)
    #                   p=(q>r)
    # Output: B (cadena), equivalente en FNC
    assert(len(A)==4 or len(A)==7), u"Fórmula incorrecta!"
    B = ''
    p = A[0]
    # print('p', p)
    if "-" in A:
        q = A[-1]
        # print('q', q)
        B = "-"+p+"O-"+q+"Y"+p+"O"+q
    elif "Y" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O-"+p+"Y"+r+"O-"+p+"Y-"+q+"O-"+r+"O"+p
    elif "O" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = "-"+q+"O"+p+"Y-"+r+"O"+p+"Y"+q+"O"+r+"O-"+p
    elif ">" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        B = q+"O"+p+"Y-"+r+"O"+p+"Y-"+q+"O"+r+"O-"+p
    elif "=" in A:
        q = A[3]
        # print('q', q)
        r = A[5]
        # print('r', r)
        #qO-rO-pY-qOrO-pY-qO-rOpYqOrOp
        B = q+"O"+"-"+r+"O"+"-"+p+"Y"+"-"+q+"O"+r+"O"+"-"+p+"Y"+"-"+q+"O"+"-"+r+"O"+p+"Y"+q+"O"+r+"O"+p
    else:
        print(u'Error enENC(): Fórmula incorrecta!')
    B = B.split('Y')
    B = [c.split('O') for c in B]
    return B 

'''
-----------------------------------------------
-----------------DPLLL -----------------------
----------------------------------------------

'''



def tseitin(A):
    '''
    Algoritmo de transformacion de Tseitin
    Input: A (cadena) en notacion inorder
    Output: B (cadena), Tseitin
    '''
    # Creamos letras proposicionales nuevas
    f = inorder_to_tree(A)
    letrasp = f.letras()
    cods_letras = [ord(x) for x in letrasp]
    m = max(cods_letras) + 256
    letrasp_tseitin = [chr(x) for x in range(m, m + f.num_conec())]
    letrasp = list(letrasp) + letrasp_tseitin
    L = [] # Inicializamos lista de conjunciones
    Pila = [] # Inicializamos pila
    i = -1 # Inicializamos contador de variables nuevas
    s = A[0] # Inicializamos símbolo de trabajo
    while len(A) > 0: # Recorremos la cadena
        # print("Pila:", Pila, " L:", L, " s:", s)
        if (s in letrasp) and (len(Pila) > 0) and (Pila[-1]=='-'):
            i += 1
            atomo = letrasp_tseitin[i]
            Pila = Pila[:-1]
            Pila.append(atomo)
            L.append(atomo + "=-" + s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]
        elif s == ')':
            w = Pila[-1]
            O = Pila[-2]
            v = Pila[-3]
            Pila = Pila[:len(Pila)-4]
            i += 1
            atomo = letrasp_tseitin[i]
            L.append(atomo + "=(" + v + O + w + ")")
            s = atomo
        else:
            Pila.append(s)
            A = A[1:]
            if len(A) > 0:
                s = A[0]
    if i < 0:
        atomo = Pila[-1]
    else:
        atomo = letrasp_tseitin[i]
    B = [[[atomo]]] + [a_clausal(x) for x in L]
    B = [val for sublist in B for val in sublist]
    return B 

def dpll(S, I):
    '''
    Algoritmo para verificar la satisfacibilidad de una formula, y encontrar un modelo de la misma
    Input:
        - S, conjunto de clausulas
        - I, interpretacion (diccionario literal->True/False)
    Output:
        - String, Satisfacible/Insatisfacible
        - I ,interpretacion (diccionario literal->True/False)
    '''
    S, I = unit_propagate(S, I)
    if len(S) == 0:
        return "Satisfacible", I
    if [] in S:
        return "Insatisfacible", {}
    l = choice(choice(S))
    lc = complemento(l)
    newS = eliminar_literal(S, l)
    newI = extender_I(I, l)
    sat, newI = dpll(newS, newI)
    if sat == "Satisfacible":
        return sat, newI
    else:
        newS = eliminar_literal(S, lc)
        newI = extender_I(I, lc)
        return dpll(newS, newI) 
    
def complemento(l):
    if '-' in l:
        return l[1:]
    else:
        return '-' + l
    
def eliminar_literal(S, l):
    S1 = [c for c in S if l not in c]
    lc = complemento(l)
    return [[p for p in c if p != lc] for c in S1] 

def extender_I(I, l):
    I1 = {k:I[k] for k in I if k != l}
    if '-' in l:
        I1[l[1:]] = False
    else:
        I1[l] = True
    return I1

def unit_propagate(S, I):
    '''
    Algoritmo para eliminar clausulas unitarias de un conjunto de clausulas, manteniendo su satisfacibilidad
    Input: 
        - S, conjunto de clausulas
        - I, interpretacion (diccionario {literal: True/False})
    Output: 
        - S, conjunto de clausulas
        - I, interpretacion (diccionario {literal: True/False})
    '''
    while [] not in S:
        l = ''
        for x in S:
            if len(x) == 1:
                l = x[0]
                S = eliminar_literal(S, l)
                I = extender_I(I, l)
                break
        if l == '': # Se recorrió todo S y no se encontró unidad
            break
    return S, I 


from random import choice, uniform, randint

class WalkSatEstado():

    def __init__(self, S):
        self.S = S
        self.letrasp = list(set([l[-1] for C in self.S for l in C]))
        self.I = interpretacion_aleatoria(self.letrasp)
        self.I_lits = set([p for p in self.letrasp if self.I[p]] + ['-'+p for p in self.letrasp if not self.I[p]])
        self.clausulas_sat = [C for C in self.S if any((True for x in self.I_lits if x in C))]
        self.clausulas_unsat = [C for C in self.S if C not in self.clausulas_sat]

    def actualizar(self, I):
        self.I = I
        self.I_lits = set([p for p in self.letrasp if self.I[p]] + ['-'+p for p in self.letrasp if not self.I[p]])
        self.clausulas_sat = [C for C in self.S if any((True for x in self.I_lits if x in C))]
        self.clausulas_unsat = [C for C in self.S if C not in self.clausulas_sat]

    def SAT(self):
        return len(self.clausulas_unsat) == 0

    def break_count(self, l):
        if l in self.I_lits:
            lit = l
        else:
            lit = complemento(l)
        clausulas_break_count = [C for C in self.clausulas_sat if set(C).intersection(self.I_lits)=={lit}]
        return len(clausulas_break_count)

def walkSAT(A, max_flips=1000, max_tries=100, p=.5):

    w = WalkSatEstado(A)
    for i in range(max_tries):
        w.actualizar(interpretacion_aleatoria(w.letrasp))
        for j in range(max_flips):
            if w.SAT():
                return 'Satisfacible', w.I
            C = choice(w.clausulas_unsat)
            breaks = sorted([(l,w.break_count(l)) for l in C], key=lambda x: x[1])
            min_breaks = breaks[0]
            if min_breaks[1] == 0:
                v = min_breaks[0]
            else:
                if uniform(0,1) < p:
                    assert(len(C)>0), f"{C}"
                    v = choice(C)
                else:
                    v = min_breaks[0]
            I = flip_literal(w.I, v)
            w.actualizar(I)
    return None, {}



