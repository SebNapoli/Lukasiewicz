#importing libraries
from z3 import *
from flask import Flask, render_template, request
from services.Search_and_debug.start_scansion import *
from services.Search_and_debug.debug import *
from services.Resolutions.create_variables import *
from services.Resolutions.resolution import *
from services.Resolutions.alt_solutions import *
from services.Search_and_debug.search_on_string import *
from services.Vague_Reasoning.reasoning import *
from services.Vague_Reasoning.formulas_construction import *
from services.Vague_Reasoning.check_on_reasoning import *
from services.McNaughton_mode.McNaughton import *
from services.McNaughton_mode.print_McNaughton import *

#calling Flash library for HTML treatment
app=Flask(__name__)

#This function prints the home page of the web-app
@app.route("/")
def home_page():
  return render_template("home page.html") #calls the HTML file for the starting choice


#This function chooses the right mode wanted by the user
@app.route("/choice", methods=["GET", "POST"])
def choose_mode():
  if request.method=="GET": #Error message if the user get here from the URL
    return "<h1> Error! </h1>"
  
  if request.method=="POST":
    try:
      choice=request.form["choice"] #The scripts gets user's input
      if choice=='help':
        return render_template("help.html") #It prints the manual in HTML format

      #If not help, choose the mode and prints the right HTML file
      elif choice=='1':
        return render_template("inputSat.html", Error=False, ID=None)

      elif choice=='2':
        return render_template("inputConsequence.html", Error=False, ID=None)

      elif choice=='3':
        return render_template("inputDimension.html", Error=False)

      elif choice=='4':
        return render_template("inputDatabase.html", Error=False, ID=None, query=True)

      elif choice=='5':
        return render_template("inputDatabase.html", Error=False, ID=None, query=False)

      elif choice=='6':
        return render_template("inputMcNaughton.html", Error=False, ID=None)
    
    except: #if no option was selected
      return render_template("home page.html") #print the home page again




#Web app in satisfability mode
@app.route("/sat", methods=["GET", "POST"])

def satisfability(): 
  if request.method=="GET":
    return "<p> Error </p>"
  
  if request.method=="POST":  
    s=Solver()
    
    try:
      formula=request.form["formula"] #input formula
      N=int(request.form["N"]) #input number of alternative solutions
    
    except: #Print a error message if no number was given
      return render_template("inputSat.html", Error=True, ID="KeyError")
    

    formula=formula.replace(' ', '') #delete useless spaces

    try:
      if len(formula)==0: #Raise an error if the users gives an empty formula
        raise AttributeError

      initial_scansion(formula) #syntax control (it raises an exception if there is a error)
      [formula, new_formula]=debugFormula(formula) #debug and parsing of the formula
      var=create_variables(new_formula, s) #creation of the variabiles list
        
      if len(var)>1: #removes useless brackets
          formula=formula[1:-1]
      
      x=resolving(new_formula, var) #thuth value computation
      s.add(x==1) #add thuth condition for the solver          
      
      if s.check()==sat: #if the formula is satisfable
        if len(var)>0: #if there are some variables, the app can give a model
          model=s.model() 
          alternative=alternatives(model, var, N, s) #for other solutions
          return render_template("outputSat.html", formula=formula, alternative=alternative, output=str(model)[1:-1], sodd=True)
                
        else: #if there are only logical constants, the app can't give a model
          return render_template("outputSat.html", formula=formula, alternative=None, output=None, sodd=True)
          
      else: #if the formula is not satisfable
        return render_template("outputSat.html", formula=formula, alternative=None, output=None, sodd=False)

    #Error treatment    
    except NotImplementedError:
      return render_template("inputSat.html", Error=True, ID='IOError')
    except IndentationError:
      return render_template("inputSat.html", Error=True, ID='IndentationError')
    except SyntaxError:
      return render_template("inputSat.html", Error=True, ID='SyntaxError')
    except ImportError:
      return render_template("inputSat.html", Error=True, ID='ImportError')      
    except:
      return render_template("inputSat.html", Error=True, ID='NoFormula')


#Web app in logic consequence mode
@app.route("/Consequence", methods=["GET", "POST"])
def consequence():

  if request.method=="GET":
    return "<p> Error </p>"
  
  if request.method=="POST":  
    try: #if there isn't an error
      s=Solver()
      set=request.form["set"].split("\n") #split the input string every time it founds a newline
      for i in range(len(set)): 
        set[i]=set[i].replace('\r', '')
        set[i]=set[i].replace(' ', '')
        #delete useless characters

      while '' in set:
        set.remove('')
      #delete all empty formulas in the set
      
      new_set=[] 
      for i in range(len(set)): #parsing of all formulas in the set
        new_set.append('')
        initial_scansion(set[i])
        [set[i], new_set[i]]=debugFormula(set[i])
        argument=variable_name(new_set[i], 0)[0]
        if argument!=new_set[i]:
          set[i]=set[i][1:-1]

      formula=request.form["formula"] #input formula
      formula=formula.replace(' ', '')
      if len(formula)==0:
        raise AttributeError

      initial_scansion(formula)
      [formula, new_formula]=debugFormula(formula)
      argument=variable_name(new_formula, 0)[0]
      if argument!=new_formula:
        formula=formula[1:-1]

      conj=''
      if len(set)!=0: #if the set is not empty
        for i in range(len(set)): #unify the set as a big conjunction
          if i==0:
            conj='('+new_set[0]+')'
          else:
            conj=merge('&', conj, '('+new_set[i]+')')

        #truth values computations
        var=create_variables(conj, s)
        varN=create_variables(new_formula, s) 
        x=resolving(conj, var)
        y=resolving(new_formula, varN)

        s.add(And(x==1, y<1)) #create the condition "if set is satisfable but the formula not"

        interpretation=[]

        for formulaG in set:
          interpretation.append(formulaG)
          
        if s.check()==unsat: #if the condition is not satisfable (see as the formula is logic consequence)
          result="The formula is logic consequence"
          return render_template("outputConsequence.html", interpetration=interpretation, formula=formula ,result=result, counterexample=None)
            
        else: #if the formula isn't logic consequence
          if (len(var)+len(varN))>0: #if there is at least one variable, the app can provide a counterexample
            result="The formula isn't logic consequence. "
            counterexample= "A possible counterexample: "+str(s.model())[1:-1]
            return render_template("outputConsequence.html", interpetration=interpretation, formula=formula, result=result, counterexample=counterexample)
          else:
            result="the formula isn't logic consequence."
            return render_template("outputConsequence.html", interpetration=interpretation, formula=formula, result=result, counterexample=None)

      else: #if the set is empty
        var=create_variables(new_formula, s)
        x=resolving(new_formula, var)
        s.add(x<1) 

        interpretation=["Empty set."]

        if s.check()==unsat: #if the condition is not satisfable
          result="The formula is logic consequence"
          return render_template("outputConsequence.html", interpetration=interpretation, formula=formula, result=result, counterexample=None)
            
        else: 
          if (len(var))>0: #if there is at least one variable, the app can provide a counterexample
            result="The formula is not logic consequence."
            counterexample= "A possible counterexample: "+str(s.model())[1:-1]
            return render_template("outputConsequence.html", interpetration=interpretation, formula=formula, result=result, counterexample=counterexample)
            
          else:
            result="The formula is not logic consequence."
            return render_template("outputConsequence.html", interpetration=interpretation, formula=formula, result=result, counterexample=None)          

    #errors treatment
    except NotImplementedError:
      return render_template("inputConsequence.html", Error=True, ID='IOError')
    except IndentationError:
      return render_template("inputConsequence.html", Error=True, ID='IndentationError')
    except SyntaxError:
      return render_template("inputConsequence.html", Error=True, ID='SyntaxError')
    except ImportError:
      return render_template("inputConsequence.html", Error=True, ID='ImportError')      
    except:
      return render_template("inputConsequence.html", Error=True, ID="NoFormula")
      

#Web app in reasoning mode (from user's input): get table dimensions
@app.route("/Reasoning", methods=["GET", "POST"])
def dimensions():
  if request.method=="GET":
    return "<p> Error </p>"
  
  if request.method=="POST":
    try:
      r=int(request.form["row"])
      col=int(request.form["col"])
      row=r+1
      return render_template("inputtable.html", Error=False, row=row, col=col)
    
    except: #if at least one form is empty, give an error message
      return render_template("inputDimension.html", Error=True)



#Web app in reasoning mode (from user's input)
@app.route("/table", methods=["GET", "POST"])
def reasoning():

  if request.method=="GET":
    return "<p> Error </p>"
  
  if request.method=="POST":
    tab=list(request.form) #returns all box names
    
    List=[]
    property=[]
    objects=[]
    comparison=[]
    table=[]
    col=0
    row=0

    try:
      for i in range(len(tab)): #split the input 
        x=request.form[tab[i]] 

        if "propriety" in tab[i]:
          col+=1
          property.append(x)

        elif "name" in tab[i]:
          row+=1
          objects.append(x)
          
        elif "entry" in tab[i]:
          List.append(x)
          
        elif "choice" in tab[i]:
          comparison.append(x)

        elif "condition" in tab[i]:
          query=x

        elif "den" in tab[i]:
          den=x
        
        elif "mode" in tab[i]:
          mode=x

      for i in range(row): #put numerical values in the table and 
        table.append(List[i*col: (i+1)*col])
        for j in range(col):
          table[i][j]=int(table[i][j])        

      [formulas, query, output]=Rea(row, col, property, objects, table, comparison, query, den, mode)

      return render_template("outputReasoning.html", formulas=formulas, Decision=query, output=output)
    
    except NameError:
      return render_template("inputtable.html", Error=True, ID="NameError", row=row+1, col=col)
    except PermissionError:
      return render_template("inputtable.html", Error=True, ID="PermissionError", row=row+1, col=col)
    except ArgumentError:
      return render_template("inputtable.html", Error=True, ID="ArgumentError", row=row+1, col=col)
    except TypeError:
      return render_template("inputtable.html", Error=True, ID="TypeError", row=row+1, col=col)
    except NotImplementedError:
      return render_template("inputtable.html", Error=True, ID='IOError', row=row+1, col=col)
    except IndentationError:
      return render_template("inputtable.html", Error=True, ID='IndentationError', row=row+1, col=col)
    except SyntaxError:
      return render_template("inputtable.html", Error=True, ID='SyntaxError', row=row+1, col=col)
    except ImportError:
      return render_template("inputtable.html", Error=True, ID='ImportError', row=row+1, col=col)      
    except: #almeno uno dei campi è vuoto
      return render_template("inputtable.html", Error=True, ID="KeyError", row=row+1, col=col)


#Web app in database mode
@app.route("/database", methods=["POST", "GET"])
def database():

  if request.method=="GET":
      return "<p> Error </p>"
    
  if request.method=="POST":
    if "condition" in list(request.form): #if it's in reasoning from databale mode
      query=True
    else:
      query=False

    try:
      with open(request.form["database"]) as f: #opening database
        objects=[]
        table=[]
        comparison=[]

        #estracting data
        data=f.readlines()
        row=len(data)-1

        for i in range(len(data)):
          riga=data[i].split(',')


          riga[len(riga)-1]=riga[len(riga)-1].replace('\n', '')
          if i==0:
            property=riga[1:]
            col=len(riga)-1

          else:
            objects.append(riga[0])
            table.append(riga[1:])
        
        for j in range(col):
          comparison.append("max")

        for i in range(row):
          for j in range(col):
            table[i][j]=int(table[i][j])

        den=request.form["den"]

        
        if query: #if the app is in reasoning mode
          decision=request.form["condition"]
          mode=request.form["mode"]
          #calling main Reasoning fuction
          [formulas, Decision, output]=Rea(row, col, property, objects, table, comparison, decision, den, mode)

        else: #if the app is in table coding mode
          var_name=[]
          par_control(property, objects, row, col)
          
          for i in range(row):
            var_name.append([])
            for j in range(col):
              var_name[i].append(property[j]+str(i+1))

          formulas=formulas_construction(table, var_name, comparison, row, col, den)
          Decision=output=None

        return render_template("outputReasoning.html", formulas=formulas, Decision=Decision, output=output)
        
    except NameError:
      return render_template("inputDatabase.html", Error=True, ID="NameError", query=query)
    except PermissionError:
      return render_template("inputDatabase.html", Error=True, ID="PermissionError", query=query)
    except ArgumentError:
      return render_template("inputDatabase.html", Error=True, ID="ArgumentError", query=query)
    except TypeError:
      return render_template("inputDatabase.html", Error=True, ID="TypeError", query=query)
    except NotImplementedError:
      return render_template("inputDatabase.html", Error=True, ID='IOError', query=query)
    except IndentationError:
      return render_template("inputDatabase.html", Error=True, ID='IndentationError', query=query)
    except SyntaxError:
      return render_template("inputDatabase.html", Error=True, ID='SyntaxError', query=query)
    except ImportError:
      return render_template("inputDatabase.html", Error=True, ID='ImportError', query=query)      
    except:
      return render_template("inputDatabase.html", Error=True, ID="KeyError", query=query)


#Web app in McNaughton function computing mode
@app.route("/McNaughton", methods=["GET", "POST"])
def McN():
  if request.method=="GET":
    return "<p> Error </p>"
  
  if request.method=="POST":  
    try:
      formula=request.form["formula"] #input formula
      formula=formula.replace(' ', '') #delete useless spaces
      if len(formula)==0: #If an empty formula is found, give an error message
        raise AttributeError

      initial_scansion(formula) #syntax control
      [formula, new_formula]=debugFormula(formula) #debugging and parsing formula      
      function=McNaughton(new_formula) #McNaughton function computing 
      #output treatment
      [output, domains]=pol_print(function) 
      return render_template("outputMcNaughton.html", formula=formula, output=output, domains=domains, N=len(output))
        
    except NotImplementedError:
      return render_template("inputMcNaughton.html", Error=True, ID='IOError')
    except IndentationError:
      return render_template("inputMcNaughton.html", Error=True, ID='IndentationError')
    except SyntaxError:
      return render_template("inputMcNaughton.html", Error=True, ID='SyntaxError')
    except ImportError:
      return render_template("inputMcNaughton.html", Error=True, ID='ImportError')      
    except:
      return render_template("inputMcNaughton.html", Error=True, ID='NoFormula')
