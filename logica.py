from itertools import product
import numpy as np
from copy import deepcopy
from typing import List, Dict


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
    
