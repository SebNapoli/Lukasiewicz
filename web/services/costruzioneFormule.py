#file content: formula construction for reasoning mode

def Cformula(start, a, b, x): #Mundici algoritm variation

    if a+b==0: #
        return '0'

    elif b==0: 
        if a==1: 
            return x
        else:
            f=str(a)+'*'+x
            return '('+f+')'

    else: 
        f1=Cformula(start, a-1, b, x)
        if f1=='0':
            f1=x
        else:
            f1='(('+f1+')+'+x+')'

        if (a-1)*start>=-b:
            f2=''
        else:
            f2=Cformula(start, a-1, b+1, x)
            f2='&'+f2
        
        return f1+f2


def Cformula2(start, a, b, x): 
  return Cformula(1-start, -a, b+a, '-'+x)