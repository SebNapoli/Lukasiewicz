from z3 import *
from flask import Flask, render_template, request
from services.scansioni import *
from services.debug import *
from services.risoluzione import *
from services.ricercaStringa import *
from services.ragionamento import *
from services.scansioneIniziale import *

app=Flask(__name__)

#stampa della pagina iniziale della web app
@app.route("/")
def pagina_iniziale():
  return render_template("pagina iniziale.html") #richiama il file html per la scelta iniziale



#Funzione che, a seconda della scelta fatta dall'utente nella pagina iniziale, sceglia la modalità corretta del programma
@app.route("/scelta", methods=["GET", "POST"])
def scelta_modalità():
  if request.method=="GET": #se entrato attraverso URL e non la scelta, da messagio di errore
    return "<h1> ERRORE! </h1>"
  
  if request.method=="POST":
    try:
      scelta=request.form["scelta"] #prende in input la scelta
      if scelta=='help':
        return render_template("aiuto.html") #stampa il manuale in formato html

      elif scelta=='1':
        return render_template("inputSoddisfacibilità.html", errore=False, ID=None)

      elif scelta=='2':
        return render_template("inputConseguenza.html", errore=False, ID=None)

      elif scelta=='3':
        return render_template("inputDimensioni.html", errore=False)

      elif scelta=='4':
        return render_template("inputDatabase.html", errore=False, ID=None, query=True)

      elif scelta=='5':
        return render_template("inputDatabase.html", errore=False, ID=None, query=False)
    
    except: #se non è stata selezionata nessuna opzione
      return render_template("pagina iniziale.html")




#programmma in modalità risolutore di una singola formula
@app.route("/soddisfacibilita", methods=["GET", "POST"])
def singolaFormula(): 
  if request.method=="GET":
    return "<p> ERRORE </p>"
  
  if request.method=="POST":  
    s=Solver()
    
    try:
      formula=request.form["formula"] #input formula
      N=int(request.form["N"]) #input numero di soluzioni alternative da dare
    
    except: #Se non è stato inserito nessun numero, stampa un messaggio di errore
      return render_template("inputSoddisfacibilità.html", errore=True, ID="KeyError")
    

    formula=formula.replace(' ', '') #elimina gli spazi

    try:
      if len(formula)==0: #Se la formula è vuota da un messaggio di errore
        raise AttributeError

      scansioneIniziale(formula) #controlla che la sintassi sia corretta
      [formula, formulaC]=debugFormula(formula) #effettua il debug e il parsing automatico della formula
      var=generaVariabili(formulaC, s) #costruzione lista delle variabili
        
      if len(var)>1:
          formula=formula[1:-1]
      
      x=risolvi(formulaC, var) #calcolo valore di verità della formula
      s.add(x==1) #aggiunta condizione verità formula          
      if s.check()==sat: #se la formula è soddisfacibile
        if len(var)>0: #se sono presenti variabili proposizionali è possibile dare un modello
          modello=s.model() 
          alternative=AltreSoluzioni(modello, var, N, s)
          return render_template("outputSoddisfacibilità.html", formula=formula, alternative=alternative, output=str(modello)[1:-1], sodd=True)
                
        else: #se sono presenti solo constanti, non è possibile generare un modello
          return render_template("outputSoddisfacibilità.html", formula=formula, alternative=None, output=None, sodd=True)
          
      else:
        return render_template("outputSoddisfacibilità.html", formula=formula, alternative=None, output=None, sodd=False)

      #gestione errori della sintassi
        
    except NotImplementedError:
      return render_template("inputSoddisfacibilità.html", errore=True, ID='IOError')
    except IndentationError:
      return render_template("inputSoddisfacibilità.html", errore=True, ID='IndentationError')
    except SyntaxError:
      return render_template("inputSoddisfacibilità.html", errore=True, ID='SyntaxError')
    except ImportError:
      return render_template("inputSoddisfacibilità.html", errore=True, ID='ImportError')      
    except:
      return render_template("inputSoddisfacibilità.html", errore=True, ID='NoFormula')



@app.route("/conseguenza", methods=["GET", "POST"])
def ConseguenzaLogica():

  if request.method=="GET":
    return "<p> ERRORE </p>"
  
  if request.method=="POST":  
    try: #continua fin quando non trova un errore
      s=Solver()
      insieme=request.form["insieme"].split("\n") #divide la stringa per tutte le volte che è stato digitato invio
      for i in range(len(insieme)): #parsing di tutte le formule di Gamma
        insieme[i]=insieme[i].replace('\r', '')
        insieme[i]=insieme[i].replace(' ', '')
        #eliminazioni di caratteri indesiderati

      while '' in insieme:
        insieme.remove('')
      #rimozione dall'insieme di tutte le formule vuote
      
      insiemeC=[] 
      for i in range(len(insieme)): #parsing di tutte le formule di Gamma
        insiemeC.append('')
        scansioneIniziale(insieme[i])
        [insieme[i], insiemeC[i]]=debugFormula(insieme[i])
        [argomento, u]=riconoscimentoVariabile(insiemeC[i], 0)
        if argomento!=insiemeC[i]:
          insieme[i]=insieme[i][1:-1]

      formula=request.form["formula"]
      formula=formula.replace(' ', '')
      if len(formula)==0:
        raise AttributeError

      scansioneIniziale(formula)
      [formula, formulaC]=debugFormula(formula) #parsing e debug formula da verificare
      [argomento, u]=riconoscimentoVariabile(formulaC, 0)
      if argomento!=formulaC:
        formula=formula[1:-1]

      con=''
      if len(insieme)!=0: #se l'insieme Gamma è un insieme non vuoto
        for i in range(len(insieme)): #sostituisce l'insieme Gamma con una serie di congiunzioni
          if i==0:
            con='('+insiemeC[0]+')'
          else:
            con=merge('&', con, '('+insiemeC[i]+')')

        var=generaVariabili(con, s) #generazione e semplificazione delle formule
        varN=generaVariabili(formulaC, s) 
        x=risolvi(con, var)
        y=risolvi(formulaC, varN)

        s.add(And(x==1, y<1)) #crea la condizione "l'insieme è soddisfacibile ma non la formula"

        interpetrazione=[]

        for formulaG in insieme:
          interpetrazione.append(formulaG)
          
        if s.check()==unsat: #se la condizione non è soddisfacibile (se la formula è conseguenza)
          risultato="La formula è conseguenza logica"
          return render_template("outputConseguenza.html", interpetrazione=interpetrazione, formula=formula ,risultato=risultato, controesempio=None)
            
        else: #altrimenti
          if (len(var)+len(varN))>0: #se la formula ha almeno una variabile proposizionale (è possibile dare un controesempio)
            risultato="La formula non è conseguenza logica. "
            controesempio= "Un possibile controesempio è dato da queste assegnazioni: "+str(s.model())[1:-1]
            return render_template("outputConseguenza.html", interpetrazione=interpetrazione, formula=formula, risultato=risultato, controesempio=controesempio)
          else:
            risultato="La formula non è conseguenza logica."
            return render_template("outputConseguenza.html", interpetrazione=interpetrazione, formula=formula, risultato=risultato, controesempio=None)

      else: #se l'insieme è vuoto (verifica che la formula è tautologia)
        var=generaVariabili(formulaC, s)
        x=risolvi(formulaC, var)
        s.add(x<1) #aggiunge la condizione "la formula non è una tautologia"

        interpetrazione=["Insieme vuoto."]

        if s.check()==unsat: #se la condizione non è soddisfacibile (se la formula è conseguenza)
          risultato="La formula è conseguenza logica"
          return render_template("outputConseguenza.html", interpetrazione=interpetrazione, formula=formula, risultato=risultato, controesempio=None)
            
        else: #altrimenti
          if (len(var))>0: #se la formula ha almeno una variabile proposizionale (è possibile dare un controesempio)
            risultato="La formula non è conseguenza logica. "
            controesempio= "Un possibile controesempio è dato da queste assegnazioni: "+str(s.model())[1:-1]
            return render_template("outputConseguenza.html", interpetrazione=interpetrazione, formula=formula, risultato=risultato, controesempio=controesempio)
            
          else:
            risultato="La formula non è conseguenza logica."
            return render_template("outputConseguenza.html", interpetrazione=interpetrazione, formula=formula, risultato=risultato, controesempio=None)          

    except NotImplementedError:
      return render_template("inputConseguenza.html", errore=True, ID='IOError')
    except IndentationError:
      return render_template("inputConseguenza.html", errore=True, ID='IndentationError')
    except SyntaxError:
      return render_template("inputConseguenza.html", errore=True, ID='SyntaxError')
    except ImportError:
      return render_template("inputConseguenza.html", errore=True, ID='ImportError')      
    except:
      return render_template("inputConseguenza.html", errore=True, ID="NoFormula")
      

#Se viene scelta il ragionamento vago con inserimento tabella, prende in input le dimensioni
@app.route("/ragionamento", methods=["GET", "POST"])
def dim_tabella():
  if request.method=="GET":
    return "<p> ERRORE </p>"
  
  if request.method=="POST":
    try:
      r=int(request.form["rig"])
      col=int(request.form["col"])
      rig=r+1
      return render_template("inputTabella.html", errore=False, ID=None, rig=rig, col=col)
    
    except: #se almeno uno dei due campi è vuoto
      return render_template("inputDimensioni.html", errore=True)



#programma in modalità ragionamento da tabella presa in input
@app.route("/tabella", methods=["GET", "POST"])
def Ragionamento_Vago():

  if request.method=="GET":
    return "<p> ERRORE </p>"
  
  if request.method=="POST":
    tab=list(request.form) #restituisce i nomi di tutti i box per l'input
    #liste utili per maneggiare le informazioni
    lista=[]
    proprieta=[]
    oggetti=[]
    confronti=[]
    tabella=[]
    col=0
    rig=0

    try:
      for i in range(len(tab)): #suddiviose dell'input secondo il suo tipo 
        x=request.form[tab[i]] 

        if "proprieta" in tab[i]:
          col+=1
          proprieta.append(x)

        elif "nome" in tab[i]:
          rig+=1
          oggetti.append(x)
          
        elif "entrata" in tab[i]:
          lista.append(x)
          
        elif "scelta" in tab[i]:
          confronti.append(x)

        elif "condizione" in tab[i]:
          decisione=x

        elif "den" in tab[i]:
          den=x
        
        elif "modalita" in tab[i]:
          modalita=x

      for i in range(rig): #sistemazione dei valori numerici in tabella e forzatura del tipo in int
        tabella.append(lista[i*col: (i+1)*col])
        for j in range(col):
          tabella[i][j]=int(tabella[i][j])        
        #impongo che i valori siano degli interi (di base sono stati presi in input come stringhe)

      [formule, decisione, output]=Rag(rig, col, proprieta, oggetti, tabella, confronti, decisione, den, modalita)

      return render_template("outputRagionamento.html", formule=formule, decisione=decisione, output=output)
    
    #gestione di tutti i possibili errori
    except NameError:
      return render_template("inputTabella.html", errore=True, ID="NameError", rig=rig+1, col=col)
    except PermissionError:
      return render_template("inputTabella.html", errore=True, ID="PermissionError", rig=rig+1, col=col)
    except ArgumentError:
      return render_template("inputTabella.html", errore=True, ID="ArgumentError", rig=rig+1, col=col)
    except TypeError:
      return render_template("inputTabella.html", errore=True, ID="TypeError", rig=rig+1, col=col)
    except NotImplementedError:
      return render_template("inputTabella.html", errore=True, ID='IOError', rig=rig+1, col=col)
    except IndentationError:
      return render_template("inputTabella.html", errore=True, ID='IndentationError', rig=rig+1, col=col)
    except SyntaxError:
      return render_template("inputTabella.html", errore=True, ID='SyntaxError', rig=rig+1, col=col)
    except ImportError:
      return render_template("inputTabella.html", errore=True, ID='ImportError', rig=rig+1, col=col)      
    except: #almeno uno dei campi è vuoto
      return render_template("inputTabella.html", errore=True, ID="KeyError", rig=rig+1, col=col)


#programma in modalità ragionamento da database esterno
@app.route("/database", methods=["POST", "GET"])
def database():

  if request.method=="GET":
      return "<p> ERRORE </p>"
    
  if request.method=="POST":
    if "condizione" in list(request.form):
      query=True
    else:
      query=False

    try:
      with open(request.form["database"]) as f: #apertura database
        oggetti=[]
        tabella=[]
        confronti=[]

        #estazione di tutti i dati nella tabella
        data=f.readlines()
        rig=len(data)-1

        for i in range(len(data)):
          riga=data[i].split(',')


          riga[len(riga)-1]=riga[len(riga)-1].replace('\n', '')
          if i==0:
            proprieta=riga[1:]
            col=len(riga)-1

          else:
            oggetti.append(riga[0])
            tabella.append(riga[1:])
        
        for j in range(col):
          confronti.append("max")

        for i in range(rig):
          for j in range(col):
            tabella[i][j]=int(tabella[i][j])

        den=request.form["den"]

        if query:
          decisione=request.form["condizione"]
          modalita=request.form["modalita"]
          #chiamata della funzione principale del ragionamento
          [formule, decisione, output]=Rag(rig, col, proprieta, oggetti, tabella, confronti, decisione, den, modalita)

        else:
          nome_var=[]
          controlloProprietà(proprieta, oggetti, rig, col)
          #crea il nome di tutte le varibili logiche, definite come nome proprietà più il codice dell'oggetto
          for i in range(rig):
            nome_var.append([])
            for j in range(col):
              nome_var[i].append(proprieta[j]+str(i+1))

          formule=costruzioneFormule(tabella, nome_var, confronti, rig, col, den)
          decisione=output=None

        return render_template("outputRagionamento.html", formule=formule, decisione=decisione, output=output)
        
    #gestione di tutti i possibili errori
    except NameError:
      return render_template("inputDatabase.html", errore=True, ID="NameError", query=query)
    except PermissionError:
      return render_template("inputDatabase.html", errore=True, ID="PermissionError", query=query)
    except ArgumentError:
      return render_template("inputDatabase.html", errore=True, ID="ArgumentError", query=query)
    except TypeError:
      return render_template("inputDatabase.html", errore=True, ID="TypeError", query=query)
    except NotImplementedError:
      return render_template("inputDatabase.html", errore=True, ID='IOError', query=query)
    except IndentationError:
      return render_template("inputDatabase.html", errore=True, ID='IndentationError', query=query)
    except SyntaxError:
      return render_template("inputDatabase.html", errore=True, ID='SyntaxError', query=query)
    except ImportError:
      return render_template("inputDatabase.html", errore=True, ID='ImportError', query=query)      
    except:
      return render_template("inputDatabase.html", errore=True, ID="KeyError", query=query)
