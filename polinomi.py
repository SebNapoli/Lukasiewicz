#file con la classi per lavorare con i polinomi delle funzioni di McNaughton

#per i singoli coefficienti
class coefficienti:
    def __init__(self, stringa, numero):
        self.nome=stringa #nome della variabile
        self.coefficiente=numero #coefficiente associato alla variabile

class vincoli:
    def __init__(self, coefficienti, t, numero, segno):
        self.pol=coefficienti
        self.tNoto=t
        self.sec=numero
        self.verso=segno

#classe per i singoli posinomi
class polinomio:
    def __init__(self, numero):
        self.coef=[] #lista di tutti i coefficienti (nel formato della classe precedente)
        self.dominio=[] #lista delle condizioni su cui il polinomio è valido
        self.tNoto=numero #termine noto del polinomio lineare

    def nuovo_coefficiente(self, stringa, numero): #aggiunta di un nuova variabile nel polinomio
        self.coef.append(coefficienti(stringa, numero))

    def aggiungi_cond(self, coefficienti, t, lim, segno):
        self.dominio.append(vincoli(coefficienti, t, lim, segno))