#file principare per le funzioni per il ragionamento logico
from z3 import *
from services.algoritmiNumerici import *
from services.costruzioneFormule import *
from services.debug import debugFormula
from services.scansioneIniziale import *
from services.controlloRagionamento import *
from services.modalitaRagionamento import *
from services.linguaggioNaturale import *


def costruzioneFormule(tabella, nome_var, confronti, rig, col, N): #costruzione delle formule che codificano le tabelle
  insieme=[]

  [massimi, minimi]=MassimiMinimi(tabella, rig, col)

  for i in range(rig):
    for j in range(col):
      den=massimi[j]-minimi[j]
      if confronti[j]=='max':
        num=tabella[i][j]-minimi[j]
      else:
        num=massimi[j]-tabella[i][j]

      if num==den:
        insieme.append(nome_var[i][j]+'=1')

      elif num==0:
        insieme.append(nome_var[i][j]+'=0')

      else:
        div=MCD(den, num)
        den=int(den/div)
        num=int(num/div)
        if N=="inf":
          f1=Cformula(float(num/den), den, 1-num, nome_var[i][j])
          f2=Cformula2(float(num/den), -den, 1+num, nome_var[i][j])
          insieme.append('('+f1+')^('+f2+')')

        else:
          N=int(N)
          if N>=den:
            f1=Cformula(float(num/den), den, 1-num, nome_var[i][j])
            f2=Cformula2(float(num/den), -den, 1+num, nome_var[i][j])
            insieme.append('('+f1+')^('+f2+')')
          
          else:  
            for k in range(N):
              if float(num/den)<float((k+1)/N):
                if k==0:
                  f1='1'
                else:  
                  f1=Cformula(float(k/N), N, 1-k, nome_var[i][j])

                if k==(N-1):
                  f2='1'
                else:
                  f2=Cformula2(float((k+1)/N), -N, 1+(k+1), nome_var[i][j])
                insieme.append('('+f1+')^('+f2+')')
                break
         
  return insieme






def Rag(rig, col, proprieta, oggetti, tabella, confronti, decisione, den, modalita):
  nome_var=[]  


  controlloProprietà(proprieta, oggetti, rig, col)
  #crea il nome di tutte le varibili logiche, definite come nome proprietà più il codice dell'oggetto
  for i in range(rig):
    nome_var.append([])
    for j in range(col):
      nome_var[i].append(proprieta[j]+str(i+1))

  if ("molto " in decisione) or ("abbastanza " in decisione):
    decisione=linguaggioNaturale(decisione)
  else:
    scansioneIniziale(decisione)

  decisione=decisione.replace(' ', '') #costruzione della formula che codifica il valore di bontà da calcolare
  [query, decisione]=debugFormula(decisione)
  count=controlloQuery(proprieta, decisione)
  
  if count==0:
    raise ArgumentError

  #crea la lista delle formule che codificano la graudatoria per ogni proprietà
  if den=="inf" or den.isdecimal():
    formule=costruzioneFormule(tabella, nome_var, confronti, rig, col, den)
  else:
    raise TypeError

  
  con=''
  for stringa in formule:
    [u, f]=debugFormula(stringa)
    con=con+'&('+f+')'
  con=con[1:]

  #a secondo della modalità che si vuole, si richiama la funzione adatta
  if modalita=='1':
    return formule, query, Rsoddisfacibilita(decisione, nome_var, proprieta, oggetti, congiun=con)
  else:
    return formule, query, Rclassifica(nome_var, decisione, proprieta, con, oggetti)