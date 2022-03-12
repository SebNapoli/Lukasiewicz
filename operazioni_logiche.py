#file per tutte le operazioni logiche
from z3 import *

def minimo(p, q): #calcola il minimo fra due variabili proposizionali
  if ((type(p)==int or type(p)==float) and (type(q)==int or type(q)==float)):
    return min(p, q)
  else:
    return If(p<=q, p, q)


def massimo(p, q): #calcola il massimo fra due variabili proposizionali
  if ((type(p)==int or type(p)==float) and (type(q)==int or type(q)==float)):
    return max(p, q)
  else:
    return If(p>=q, p, q)


def tnorm(p, q): #t-norma, funzione di verità della congiunzione forte (valore numerico max{p+q-1, 0})
  return massimo(p+q-1, 0)

def residuo(p, q): #calcolo residuo, funzione di verità dell'implicazione (valore numerico min{q-p+1, 1})
  return minimo(-p+q+1, 1)

def compl(p): #calcolo valore di verità implicazione
  return 1-p

def sommat(p, q): #calcolo valore di verità disgiunzione forte (valore numerico min{p+q, 1})
  return minimo(p+q, 1)

def doppiaimp(p, q): #calcolo valore di verità doppia implicazione
  return tnorm(residuo(p, q), residuo(q, p))

def difft(p, q): #calcolo differenza troncata
  return tnorm(p, compl(q))
