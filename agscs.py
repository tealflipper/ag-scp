from random import choice, randint, random, sample, uniform
from tools import generateGraph, generate_blocks, merge, overlap, prefix, merge
import csv
import sys



def ag (n, d, m, sel, pc, cruza, pm, mut, selnat, numiter):
    """
    Algoritmo genético para resolver el problema del viajante
    Parametros:
    n - numero de ciudades
    d - vector de costos
    m - tamaño de la poblacion
    sel - metodo de seleccion
    pc - probabilidad de cruza
    cruza - operador de cruza
    pm - probabilidad de mutacion
    mut - operador de mutacion
    selnat - metodo de seleccion natural
    numiter - numero de generaciones sin mejora
    """

    # Se crea una poblacion de soluciones aleatorias
    # y se calcula la aptitud de cada una
    padres, aptitud = poblacionInicial(m, n, d)
    mejoraptitud = max(aptitud)
    mejorpadre = padres[aptitud.index(mejoraptitud)]
  
    generacion = 0
    generacionesSinMejora = 0
    while (generacionesSinMejora < numiter):
        generacion = generacion + 1
        
        # Se eligen m/2 pares de padres
        indpadres = seleccionPadres(m, aptitud, sel)
        
        # Se recombinan los m/2 pares de padres para obtener una
        # poblacion de hijos
        # Se evaluan los hijos
        hijos, aptitudhijos = recombinacion(padres, indpadres, pc, cruza, d)

        # Se mutan los hijos
        # y se evaluan en la funcion objetivo
        hijos, aptitudhijos = mutacion (hijos, aptitudhijos, pm, mut, d)

        padres, aptitud = seleccionNatural (padres, aptitud, hijos, aptitudhijos, selnat)
        
#        padres.extend(hijos)
#        aptitud.extend(aptitudhijos)
#
#        comb = list(zip(padres, aptitud))
#        comb = sorted(comb, key = lambda sol: sol[1], reverse = True)
#        # Se seleccionan los mejores m
#        padres = [elem[0] for elem in comb[:m]]
#        aptitud = [elem[1] for elem in comb[:m]]

        # Si la mejor solucion actual es mejor que la
        # anterior, se actualiza la actual
        if aptitud[0] > mejoraptitud:
            mejorpadre = padres[0]
            mejoraptitud = aptitud[0]
            generacionMejor = generacion
            generacionesSinMejora = 0
        else:
            generacionesSinMejora = generacionesSinMejora + 1
    
    return mejorpadre, 1 / mejoraptitud, generacionMejor, generacion


# Se crea una poblacion inicial aleatoria
def poblacionInicial(m, n, d):
    # Se crea un conjunto de soluciones aleatorias y
    # se calcula su valor y peso
    padres = [1] * m
    aptitud = [1] * m
    for i in range(m):
        # Crea una permutacion aleatoria de {1..n}
        padres[i] = sample(range(n), n)
        aptitud[i] = calcularAptitud(padres[i], d)
    return padres, aptitud


# Calcula el costo del recorrido en x
def calcularAptitud (x, d):
    n = len(x)
    costo = distancia(x[n-1], x[0], n, d)
    for i in range(n-1):
        costo = costo + distancia(x[i], x[i+1], n, d)
    return 1.0 / costo


# Obtiene la distancia de la ciudad i a la ciudad j
def distancia(i, j, n, d):
    return d[(i * n) + j] 


# Se seleccionan m padres.
def seleccionPadres(m, aptitud, sel):
    indpadres = [None] * m
    for i in range(m):
      indpadres[i]= seleccion(aptitud, sel)
    return indpadres


# Operador de seleccion.
# Selecciona un individuo de acuerdo con la tecnica de seleccion utilizada.
def seleccion (aptitud, sel):
  if sel == "torneo":
    ind = torneo(aptitud, 2)
  else:
    ind = ruleta(aptitud)
  return ind


# Seleccion por torneo.
# Devuelve el indice del mejor individuo de t seleccionados aleatoriamente.
def torneo(aptitud, t):
  # Se eligen t individuos de forma aleatoria
  sel = sample(range(len(aptitud)), t)
  
  # Se obtienen las aptitudes de los individuos seleccionados
  aptitudsel = list(aptitud[i] for i in sel)
  
  #Se encuentra al individuo con mejor aptitud
  win = aptitudsel.index(max(aptitudsel))

  return sel[win]


# Seleccion por ruleta.
# Devuelve el indice del individuo que gano en la ruleta.
def ruleta (aptitud):
    phi = sum(aptitud)
    rho = random()
    suma = 0
    while suma < rho:
        i = choice(range(len(aptitud)))
        suma = suma + aptitud[i] / phi
    return i


# Operador de cruza.
# Devuelve una poblacion de hijos, resultado de la cruza de pares de padres.
def recombinacion(padres, indpadres, pc, cruza, d):
    m = len(padres)
    hijos = [None] * m
    aptitudhijos = [None] * m
    for i in range(int(m/2)):
        p1 = indpadres[2*i]
        p2 = indpadres[2*i+1]
        
        if random() <= pc:
            if cruza == "orden":
                ch = orden(padres[p1], padres[p2])
            else:
                ch = posicion(padres[p1], padres[p2])
            hijos[2*i] = ch[0]
            hijos[2*i+1] = ch[1]
        else:
            hijos[2*i] = padres[p1]
            hijos[2*i+1] = padres[p2]

        aptitudhijos[2*i] = calcularAptitud(hijos[2*i], d)
        aptitudhijos[2*i+1] = calcularAptitud(hijos[2*i+1], d)
    return hijos, aptitudhijos


# Operador de cruza por orden
# Se crea un individuo a partir de dos padres p1 y p2.
def orden (p1, p2):
    n = len(p1)
    cp1 = choice(range(n))
    cp2 = choice(range(n))
    while cp2 == cp1:
            cp2 = choice(range(n))
    if cp2 < cp1:
        temp = cp1
        cp1 = cp2
        cp2 = temp
    ch1 = crearHijoOrden(p1, p2, cp1, cp2)
    ch2 = crearHijoOrden(p2, p1, cp1, cp2)
    return [ch1, ch2]


def crearHijoOrden(p1, p2, cp1, cp2):
    n = len(p1)
    ch = [None] * n
    ch[cp1:cp2+1] = p1[cp1:cp2+1]
    i = (cp2+1) % n
    j = (cp2+1) % n
    elems = cp2 - cp1 + 1
    while elems < n:
        if p2[j] not in ch:
            ch[i] = p2[j]
            i = (i+1) % n
            elems = elems + 1
        j = (j+1) % n
    return ch


# Operador de cruza por posicion
# Se crea un individuo a partir de dos padres p1 y p2.
def posicion (p1, p2):
    n = len(p1)
    k = choice(range(n+1))
    cp = sample(range(n), k)
    ch1 = crearHijoPosicion(p1, p2, cp)
    ch2 = crearHijoPosicion(p2, p1, cp)
    return [ch1, ch2]


def crearHijoPosicion(p1, p2, cp):
    n = len(p1)
    ch = [None] * n
    for i in cp:
        ch[i] = p1[i]
    elems = len(cp)
    i = 0
    j = 0
    while elems < n:
        while ch[i] is not None:
            i = i + 1
        while p2[j] in ch:
            j = j + 1
        ch[i] = p2[j]
        elems = elems + 1
    return ch


# Operador de mutacion.
# Aplica el operador de mutacion a los individuos seleccionados.
def mutacion (hijos, aptitudhijos, pm, mut, d):
    m = len(hijos)
    for i in range(m):
        if random() <= pm:
            # Se muta el hijo i
            # y se evalua en la funcion de aptitud
            if mut == 'int':
                hijos[i] = intercambio(hijos[i])
            elif mut == 'ins':
                hijos[i] = insercion(hijos[i])
            elif mut == 'inv':
                hijos[i] = inversion(hijos[i])
            else:
                if random() <= 1.0/3:
                    hijos[i] = insercion (hijos[i])
                elif random() <= 0.5:
                    hijos[i] = intercambio (hijos[i])
                else:
                    hijos[i] = inversion (hijos[i])
            aptitudhijos[i] = calcularAptitud(hijos[i], d)
    return hijos, aptitudhijos
            

# Mutacion por intercambio
def intercambio (x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    temp = xprima[i]
    xprima[i] = xprima[j]
    xprima[j] = temp
    return xprima


# Mutacion por insercion
def insercion (x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    if j < i:
        temp = i
        i = j
        j = temp
    xprima.pop(j)
    xprima.insert(i, x[j])
    return xprima


# Mutacion por inversion
def inversion (x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    for k in range(j - i + 1):
        xprima[i+k] = x[j-k]
    return xprima


# Metodo de seleccion natura.
# Aplica el metodo de seleccion natural elegido
# y devuelve la siguiente generacion
def seleccionNatural (padres, aptitud, hijos, aptitudhijos, selnat):
    if selnat == "generacional":
        padres, aptitud = seleccionGeneracional (padres, aptitud, hijos, aptitudhijos)
    else:
        padres, aptitud = seleccionElitista(padres, aptitud, hijos, aptitudhijos)
    return padres, aptitud


# Aplica seleccion generacional a padres e hijos
def seleccionGeneracional (padres, aptitud, hijos, aptitudhijos):
    # Se selecciona el mejor padre
    mejor = aptitud.index(max(aptitud))
    # Se selecciona el peor hijo
    peor = aptitudhijos.index(min(aptitudhijos))
    # Se reemplaza el peor hijo por el mejor padre
    hijos[peor] = padres[mejor]
    aptitudhijos[peor] = aptitud[mejor]
    # Se reemplaza la poblacion de padres por la de hijos
    padres = hijos
    aptitud = aptitudhijos
    return padres, aptitud


# Aplica seleccion elitista a padres e hijos
def seleccionElitista(padres, aptitud, hijos, aptitudhijos):
    m = len(padres)
    padres.extend(hijos)
    aptitud.extend(aptitudhijos)
        
    comb = list(zip(padres, aptitud))
    comb = sorted(comb, key = lambda sol: sol[1], reverse = True)
    # Se seleccionan los mejores m
    padres = [elem[0] for elem in comb[:m]]
    aptitud = [elem[1] for elem in comb[:m]]
    return padres, aptitud


# Lee datos del problema del archivo de texto
def preproceso (problema):
    # Se lee la informacion del caso de prueba
    arch = open('scs/' + problema + '.scs')
    info = list(map(int, arch.read().split()))
    arch.close()
    n = info[0]
    info = info[1:]
    # with open('tsp/best-known.atsp') as f:
    #     reader = csv.reader(f, delimiter=' ')
    #     data = [(col1, int(col2)) for col1, col2 in reader]
    
    # i = 0
    # while problema not in data[i][0]:
    #     i = i+1
    # opt = int(data[i][1])
    # n <- problema 
    # blocks = generate_blocks(n)
    # info = generateGraph(blocks)
    print("DATOS DEL CASO DEL PROBLEMA")
    print("Nombre: scs")
    print("Numero de cadenas:", n)
    # print("Costo del recorrido de la solucion optima:", opt)
    
    return n, info


# Despliega los resultados
def resultado(x, costo, promcosto, generacionMejor, generacion):
    print("\nMEJOR SOLUCION ENCONTRADA")
    print("Recorrido:", x)
    print("Costo:", costo)
    print("Generacion encontrada:", generacionMejor)
    print("Generaciones:", generacion)
    print("Costo promedio:", promcosto, "\n")



def agtsp (problema, m, sel, pc, cruza, pm, mutacion, selnat, generaciones, repeticiones):
    n, d = preproceso(problema)
    mejorcosto = 100**100
    promcosto = 0.0
    for i in range(repeticiones):
        x, costo, genMejor, gen = ag(n, d, m, sel, pc, cruza, pm, mutacion, selnat, generaciones)
        promcosto = promcosto + costo
        if mejorcosto > costo:
            mejorx = x
            mejorcosto = costo
            generacionMejor = genMejor
            generaciones = gen
    resultado(mejorx, mejorcosto, promcosto/repeticiones, generacionMejor, generaciones)



if __name__ == "__main__":
    if(len(sys.argv) < 11):
        print("Sintaxis: agtsp.py <problema> <m> <sel> <pc> <cruza> <pm> <mutacion> <selnat> <numiter> <repeticiones>")
    else:
        agtsp(sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4]), sys.argv[5], float(sys.argv[6]), sys.argv[7], sys.argv[8], int(sys.argv[9]), int(sys.argv[10]))
