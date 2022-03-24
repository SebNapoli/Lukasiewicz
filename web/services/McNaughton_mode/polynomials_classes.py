#file for working with linear polynomials in McNaughton functions

#class of all coefficients
class coefficients:
    def __init__(self, string, number):
        self.name=string #variable name
        self.coef_value=number #variable coefficient

#class of all constrains
class constrains:
    def __init__(self, coefficients, t, number, sign):
        self.pol=coefficients
        self.cons_term=t
        self.second_member=number
        self.verse=sign

#class of all linear polynomials
class linear_polynomials:
    def __init__(self, number):
        self.coef=[] #coefficient list
        self.domain=[] #condition list where the polynomial is valid
        self.al_domain=[] #list of other domains where the polynomial is valid
        self.cons_term=number #constant term

    def new_coef(self, string, number): #add a new coefficient
        temp=coefficients(string, number) #creation of the new coefficient
        if len(self.coef)==0: #add it if there aren't other oefficient
            self.coef.append(temp)
        
        else:
            for i in range(len(self.coef)): #insert it in alphabetical order
                if temp.name<self.coef[i].name:
                    self.coef.insert(i, temp)
                    break

            if i+1==len(self.coef):
                self.coef.append(temp)

    def new_cond(self, coefficients, t, lim, sign): #add a new condition in the domain
        self.domain.append(constrains(coefficients, t, lim, sign))