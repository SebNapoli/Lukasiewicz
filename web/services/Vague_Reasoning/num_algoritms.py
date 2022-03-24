#file content: Numerical algoritms

#MCD computing
def MCD(a, b):
    if b==1:
        return 1
    if b==0:
        return a
    else:
        return MCD(b, a%b)


#for all properties, return max and min value
def MaxMin(table, row, col):
  maxs=[]
  mins=[]

  for j in range(col):
    for i in range(row):
      if i==0:
        x=y=table[i][j]
        
      else:
        x=min(x, table[i][j])
        y=max(y, table[i][j]) 
    
    mins.append(x)
    maxs.append(y) 
  
  return maxs, mins

#return the thuth value of a variable from the model
def value(var_name, model): 
  for d in model.decls():
    if var_name==d.name():
      fraction=str(model[d])
      
      if '/' in fraction:
        ind=fraction.index('/')
        num=int(fraction[:ind])
        den=int(fraction[ind+1:])
      else:
        num=int(fraction)
        den=1

      val=float(num/den)

      return val
