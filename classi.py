from z3 import *

class Var_Prop: #classe che ragruppa i nomi e le variabili z3 in un unico oggetto, e inoltre si occupa di porre la variabile compresa tra 0 e 1
  def __init__(self, nome, s):
      self.nome=nome
      self.variabile=Real(nome)
      s.add(And(self.variabile<=1, self.variabile>=0))



class Soluzione: #classe di tutti i valori numerici ottenuti da z3
  def __init__(self, nome, valore):
    self.nome=nome
    self.variabile=valore