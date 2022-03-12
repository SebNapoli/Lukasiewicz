#file di funzioni di controllo correttezza parametri per il ragionamento vago
from services.costruzioneFormule import *
from services.debug import con

#controlla che il nome delle proprietà e degli oggetti non sia errato
def controlloProprietà(proprieta, oggetti, rig, col):
  for i in range(col):
    proprieta[i]=proprieta[i].replace(' ', '')
    if proprieta[i]=='':
      raise KeyError
    elif proprieta[i].isalnum():
      if 'P' in proprieta[i]:
        raise PermissionError
    else:
      raise NameError

  for i in range(rig): #controllo sui nomi degli oggetti (non possono essere stringe vuote)
    stringa=oggetti[i].replace(' ', '')
    if stringa=='':
      raise KeyError
    elif stringa.isalnum():
      if 'P' in stringa:
        raise PermissionError
    else:
      raise NameError


#controlla che nella query non siano presenti proprietà differenti da quelle in tabella
def controlloQuery(proprieta, decisione):
    count=0
    lista=[]

    #definizione della lista di nomi delle proprietà presenti nella query
    ini=0
    for i in range(len(decisione)):
        if not(decisione[i].isdecimal()) and not(decisione[i].isalpha()):
            lista.append(decisione[ini:i])
            ini=i+1
        elif i==len(decisione)-1:
            lista.append(decisione[ini:])

    #effettivo controllo
    for j in range(len(proprieta)):
      if proprieta[j] in lista:
        count+=1
    return count




