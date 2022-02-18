#-*-coding:utf-8 -*-'''
'''
Created on 29/11/2016

@author: Carolina 
'''

class Figura():
            
    def __init__(self, nome, l, a, r):
        self.nome = nome
        self.largura = l
        self.altura = a
        self.rodar = r
        self.posx = -1
        self.posy = -1
        
    def move(self, px, py):
        self.posx = px
        self.posy = py
    
    def getnome(self):
        return self.nome  

    def setnome(self, nome):
        self.nome = nome    
    
    def getposx(self):
        return self.posx
    
    def getposx2(self):  # Correspondente ao canto inferior direito
        if self.posx == -1: 
            return -1
        else: 
            return self.posx + self.largura - 1
    
    def setposx(self, px):
        self.posx = px  
        
    def getposy(self):
        return self.posy
    
    def getposy2(self):  # Correspondente ao canto inferior direito
        if self.posy == -1: 
            return -1
        else: 
            return self.posy + self.altura - 1

    def setposy(self, py):
        self.posy = py
    
    def getwidth(self):
        return self.largura

    def setwidth(self, w):
        self.largura = w
    
    def getheight(self):
        return self.altura
    
    def setheight(self, h):
        self.altura = h

    def getArea(self):
        return self.largura * self.altura
    
    def getrodar (self):
        return self.rodar
    
    
class RetangulosEngine:
    
    def __init__(self, l, a):
        self.largura = l
        self.altura = a
        self.figuras_colocadas = {}
        self.figuras_nao_colocadas = {}
        self.areas = {}
        self.rest_DIR = []
        self.rest_ESQ = []
        self.rest_CIM = []
        self.rest_BX = []
        self.rest_CLD = []
        self.rest_SEP = []
        self.rest_DENTRO = []
        self.rest_FORA = []
        self.desfrsv=[]
        self.figuras_anteriores={}
        self.s = Stack()
        t= ('first', 'DIM', 'no name')
        self.s.push(t)
    
    def novo_rect(self, nome, largura, altura, rodar):
        if nome in self.figuras_nao_colocadas or nome in self.figuras_colocadas:
            return "NÃO"
        else:
            f = Figura(nome, largura, altura, rodar)
            self.figuras_nao_colocadas[nome] = f
            
            return "SIM"

    def coloca(self, nome, px, py):  
        if nome in self.figuras_nao_colocadas:
            f = self.figuras_nao_colocadas[nome]
            if self.__valida_coloca(f, px, py) == False: 
                return "NÃO"
            else:
                f.setposx(px)
                f.setposy(py)
                self.figuras_colocadas[nome] = f
                del self.figuras_nao_colocadas[nome]
                t=(f, 'COL', nome)
                self.s.push(t)
        elif nome in self.figuras_colocadas:  # aqui vamos mudar o rectangulo de posição
            f = self.figuras_colocadas[nome]
            if self.__valida_coloca(f, px, py) == False: 
                return "NÃO"
            else:
                g=self.figuras_colocadas[nome]
                if nome in self.figuras_anteriores:        #criamos um dicionario para guardar as posições anteriores de cada figura, de modo a conseguirmos restaurar a sua posição no undo
                    self.figuras_anteriores[nome]+=[(g.getposx(), g.getposy())]  #se não for a primeira vez que estamos a mudar a figura de posição, apenas adicionamos, antes de a mudarmos de posição, as suas coordenadas ao dicionario como valores da chave correspondente ao nome da figura
                else:                                                            # assim, o ultimo tuplo da lista correspondente ao nome da figura(chave) corresponde a última posição que esta ocupou antes de ser alterada
                    self.figuras_anteriores[nome]=[(g.getposx(), g.getposy())]
                f.setposx(px)
                f.setposy(py)
                t=(f, 'COL',nome)
                self.s.push(t)
        elif nome not in self.figuras_nao_colocadas and nome not in self.figuras_colocadas:
            return 'NÃO'         
        return "SIM"
    
    def __valida_coloca(self, fig, posx, posy):
            if not self.__valida_rest_dentro_sup(fig, posx, posy):
                return False
            if not self.__nao_sobrepoe(fig, posx, posy):
                return False #vai sobrepor a nenhum outro rectangulo e cai dentro da dimensao
            if not self.__valida_rest_dir(fig, posx, posy): 
                return False  # valida a restrição do comando DIR
            if not self.__valida_rest_esq(fig, posx, posy): 
                return False  # valida a restrição do comando ESQ
            if not self.__valida_rest_cim(fig, posx, posy): 
                return False  # valida a restrição do comando CIM
            if not self.__valida_rest_bx(fig, posx, posy): 
                return False  # valida a restrição do comando BX
            if not self.__valida_rest_CLD(fig, posx, posy): 
                return False  # valida a restrição do comando CLD
            if not self.__valida_rest_SEP(fig, posx, posy): 
                return False  # valida a restrição do comando SEP
            if not self.__valida_rest_dentro(fig, posx, posy): 
                return False  # valida a restrição do comando DENTRO
            if not self.__valida_rest_fora(fig, posx, posy): 
                return False  # valida a restrição do comando FORA         
            return True
        
    def __valida_rest_dentro_sup(self, f, x, y):
        if x >= 1 and y >= 1 and x + f.getwidth() - 1 <= self.largura and y + f.getheight() - 1 <= self.altura:
            return True
        else:
            return False
        
    def __valida_rest_dir(self, fig, x, y):
        valido = True
        for (fA, fB) in self.rest_DIR:  # cada elemento desta lista é um tuplo do genero (figA,figB) em que a figA fica à direita de figB
            if fig.getnome() == fA:  # encontrei a figura na lista de restrições como uma que tinha de estar à direita
                if fB in self.figuras_colocadas:  # pois se fB não estiver colocada não vai haver qualquer problema em colocar fA
                    figuraB = self.figuras_colocadas[fB]
                    # testar que a instancia fig está à direita da instancia figuraB
                    if x <= figuraB.getposx2(): 
                        valido = False
                        break
            elif fig.getnome() == fB:  # encontrei a figura na lista de restrições como uma que tinha de estar à esquerda
                if fA in self.figuras_colocadas:
                    figuraA = self.figuras_colocadas[fA]
                    # testar que a instancia fig está à esquerda da instancia figuraA
                    if figuraA.getposx() <= x + fig.getwidth() - 1:  
                        valido = False
                        break
        return valido
    
        
    def __valida_rest_esq(self, fig, x, y):
        valido = True
        for (fA, fB) in self.rest_ESQ:  # cada elemento desta lista é um tuplo do genero (figA,figB) em que a figA fica à esquerda de figB
            if fig.getnome() == fA:  # encontrei a figura na lista de restrições como uma que tinha de estar à esq
                if fB in self.figuras_colocadas:  # pois se fB não estiver colocada não vai haver qualquer problema em colocar fA
                    figuraB = self.figuras_colocadas[fB]
                    # testar que a instancia fig está à esquerda da instancia figuraB
                    if figuraB.getposx() <= x + fig.getwidth() - 1: 
                        valido = False
                        break
            elif fig.getnome() == fB:  # encontrei a figura na lista de restrições como uma que tinha de estar à direita
                if fA in self.figuras_colocadas:
                    figuraA = self.figuras_colocadas[fA]
                    # testar que a instancia fig está à direita da instancia figuraA
                    if x <= figuraA.getposx2():   
                        valido = False
                        break
        return valido
    
    def __valida_rest_cim(self, fig, x, y):
        valido = True
        for (fA, fB) in self.rest_CIM:  # cada elemento desta lista é um tuplo do genero (figA,figB) em que a figA fica acima de figB
            if fig.getnome() == fA:  # encontrei a figura na lista de restrições como uma que tinha de estar acima de outra
                if fB in self.figuras_colocadas:  # pois se fB não estiver colocada não vai haver qualquer problema em colocar fA
                    
                    figuraB = self.figuras_colocadas[fB]
                    # testar que a instancia fig está acima da instancia figuraB
                    if y + fig.getheight() - 1 >= figuraB.getposy(): 
                        valido = False
                        break
            elif fig.getnome() == fB:  # encontrei a figura na lista de restrições como uma que tinha de estar abaixo
                if fA in self.figuras_colocadas:
                    figuraA = self.figuras_colocadas[fA]
                    # testar que a instancia fig está abaixo da instancia figuraA
                    if y <= figuraA.getposy2():   
                        valido = False
                        break
        return valido
        
    def __valida_rest_bx(self, fig, x, y):
        valido = True
        for (fA, fB) in self.rest_BX:  # cada elemento desta lista é um tuplo do genero (figA,figB) em que a figA fica abaixo de figB
            if fig.getnome() == fA:  # encontrei a figura na lista de restrições como uma que tinha de estar abaixo
                if fB in self.figuras_colocadas:  # pois se fB não estiver colocada não vai haver qualquer problema em colocar fA
                    figuraB = self.figuras_colocadas[fB]
                    # testar que a instancia fig está abaixo da instancia figuraB
                    if y <= figuraB.getposy2(): 
                        valido = False
                        break
            elif fig.getnome() == fB:  # encontrei a figura na lista de restrições como uma que tinha de estar acima
                if fA in self.figuras_colocadas:
                    figuraA = self.figuras_colocadas[fA]
                    # testar que a instancia fig está acima da instancia figuraA
                    if y +fig.getheight() -1 >= figuraA.getposy():   
                        valido = False
                        break
        return valido
    
    def __valida_rest_CLD(self, fig, x, y):      #verificador da restrição em colado
        valido = False
        if len(self.rest_CLD)==0:    #se nao existir nenhuma restriçao guardada na lista
            return True
        for (fA, fB) in self.rest_CLD: # cada elemento desta lista é um tuplo do genero (figA,figB) em que a um lado da figA fica colado a um lado da figB
            if fig.getnome() == fA:    # encontrei a figura na lista de restrições como uma que tinha de estar colada a figB
                if fB in self.figuras_colocadas:    # verifica se fB já foi colocada
                    if fA in self.figuras_colocadas:   #se estivermos a mudar a posição de uma figura ja colocada
                        figuraB = self.figuras_colocadas[fB]
                        figuraA = self.figuras_colocadas[fA]
                        if x == figuraB.getposx() + figuraB.getwidth() or x + figuraA.getwidth()-2 == figuraB.getposx():  #verifica um dos lados verticais em posições seguidas
                            if y<=figuraB.getposy()<=y+figuraA.getheight()-1 or y<=figuraB.getposy()+figuraB.getheight()-1<=y+figuraA.getheight()-1 or figuraB.getposy()<=y<=figuraB.getposy() + figuraB.getheight()-1 or figuraB.getposy()<=figuraA.getheight()+y - 1<=figuraB.getposy() + figuraB.getheight()-1:  #verifica se esses lados estão mesmo colados 
                                return True
                                break
                        if y  == figuraB.getposy() + figuraB.getheight() or y + figuraA.getheight()-1 == figuraB.getposy()-1:  #mesmo raciocínio para os lados horizontais
                            if x<=figuraB.getposx()<=x+figuraA.getwidth()-1 or x<=figuraB.getposx()+figuraB.getwidth()-1<=x+figuraA.getwidth()-1 or figuraB.getposx()<=x<=figuraB.getposx() + figuraB.getwith()-1 or figuraB.getposx()<=figuraA.getwidth()+x-1<=figuraB.getposx() + figuraB.getwith()-1: 
                                return True
                                break
                    elif fA in self.figuras_nao_colocadas:
                        figuraB = self.figuras_colocadas[fB]
                        figuraA = self.figuras_nao_colocadas[fA]
                        if x == figuraB.getposx() + figuraB.getwidth() or x + figuraA.getwidth()-2 == figuraB.getposx():
                            if y<=figuraB.getposy()<=y+figuraA.getheight()-1 or y<=figuraB.getposy()+figuraB.getheight()-1<=y+figuraA.getheight()-1 or figuraB.getposy()<=y<=figuraB.getposy() + figuraB.getheight()-1 or figuraB.getposy()<=figuraA.getheight()+y - 1<=figuraB.getposy() + figuraB.getheight()-1: 
                                return True
                                break
                        if y  == figuraB.getposy() + figuraB.getheight() or y + figuraA.getheight()-1 == figuraB.getposy()-1:
                            if x<=figuraB.getposx()<=x+figuraA.getwidth()-1 or x<=figuraB.getposx()+figuraB.getwidth()-1<=x+figuraA.getwidth()-1 or figuraB.getposx()<=x<=figuraB.getposx() + figuraB.getwith()-1 or figuraB.getposx()<=figuraA.getwidth()+x-1<=figuraB.getposx() + figuraB.getwith()-1: 
                                return True
                                break
                elif fB in self.figuras_nao_colocadas:  # verifica se fB ainda não foi colocada
                    return True
            elif fig.getnome() == fB:      # encontrei a figura na lista de restrições como uma que tinha de estar colada
                if fA in self.figuras_colocadas:    # verifica se fA já foi colocada
                    if fB in self.figuras_colocadas:
                        figuraA = self.figuras_colocadas[fA]
                        figuraB = self.figuras_colocadas[fB]
                        if x == figuraA.getposx() + figuraA.getwidth() or x + figuraB.getwidth()-2 == figuraA.getposx():
                            if y<=figuraA.getposy()<=y+figuraB.getheight()-1 or y<=figuraA.getposy()+figuraA.getheight()-1<=y+figuraB.getheight()-1 or figuraA.getposy()<=y<=figuraA.getposy() + figuraA.getheight()-1 or figuraA.getposy()<=figuraB.getheight()+y - 1<=figuraA.getposy() + figuraA.getheight()-1: 
                                return True
                                break
                        if y  == figuraA.getposy() + figuraA.getheight() or y + figuraB.getheight()-1 == figuraA.getposy()-1:
                            if x<=figuraA.getposx()<=x+figuraB.getwidth()-1 or x<=figuraA.getposx()+figuraA.getwidth()-1<=x+figuraB.getwidth()-1 or figuraA.getposx()<=x<=figuraA.getposx() + figuraA.getwith()-1 or figuraA.getposx()<=figuraB.getwidth()+x-1<=figuraA.getposx() + figuraA.getwith()-1: 
                                return True
                                break
                    if fB in self.figuras_nao_colocadas:
                        figuraA = self.figuras_colocadas[fA]
                        figuraB = self.figuras_nao_colocadas[fB]
                        if x == figuraA.getposx() + figuraA.getwidth() or x + figuraB.getwidth()-2 == figuraA.getposx():
                            if y<=figuraA.getposy()<=y+figuraB.getheight()-1 or y<=figuraA.getposy()+figuraA.getheight()-1<=y+figuraB.getheight()-1 or figuraA.getposy()<=y<=figuraA.getposy() + figuraA.getheight()-1 or figuraA.getposy()<=figuraB.getheight()+y - 1<=figuraA.getposy() + figuraA.getheight()-1: 
                                return True
                                break
                        if y  == figuraA.getposy() + figuraA.getheight() or y + figuraB.getheight()-1 == figuraA.getposy()-1:
                            if x<=figuraA.getposx()<=x+figuraB.getwidth()-1 or x<=figuraA.getposx()+figuraA.getwidth()-1<=x+figuraB.getwidth()-1 or figuraA.getposx()<=x<=figuraA.getposx() + figuraA.getwith()-1 or figuraA.getposx()<=figuraB.getwidth()+x-1<=figuraA.getposx() + figuraA.getwith()-1: 
                                return True
                                break
                elif fA in self.figuras_nao_colocadas:      # verifica se fA ainda não foi colocada
                    return True
            elif fig.getnome() != fA and fig.getnome() != fB:   #verifica se fig pertence a alguma das restrições da lista
                return True 
        return valido    #se não estiver de acordo com a restrição, retorna False
    
    def __valida_rest_SEP(self, fig, x, y):      #verificador da restrição separado
        valido = True
        for (fA, fB) in self.rest_SEP: # cada elemento desta lista é um tuplo do genero (figA,figB) em que a um lado da figA fica separada da figB
            if fig.getnome() == fA:    # encontrei a figura na lista de restrições como uma que tinha de estar separada da figB
                if fB in self.figuras_colocadas:    # verifica se fB já foi colocada
                    if fA in self.figuras_colocadas:   #se estivermos a mudar a posição de uma figura ja colocada
                        figuraB = self.figuras_colocadas[fB]
                        figuraA = self.figuras_colocadas[fA]
                        if x == figuraB.getposx() + figuraB.getwidth() or x + figuraA.getwidth()-2 == figuraB.getposx():
                            if y<=figuraB.getposy()<=y+figuraA.getheight()-1 or y<=figuraB.getposy()+figuraB.getheight()-1<=y+figuraA.getheight()-1 or figuraB.getposy()<=y<=figuraB.getposy() + figuraB.getheight()-1 or figuraB.getposy()<=figuraA.getheight()+y - 1<=figuraB.getposy() + figuraB.getheight()-1: 
                                return False
                                break
                        if y  == figuraB.getposy() + figuraB.getheight() or y + figuraA.getheight()-1 == figuraB.getposy()-1:
                            if x<=figuraB.getposx()<=x+figuraA.getwidth()-1 or x<=figuraB.getposx()+figuraB.getwidth()-1<=x+figuraA.getwidth()-1 or figuraB.getposx()<=x<=figuraB.getposx() + figuraB.getwith()-1 or figuraB.getposx()<=figuraA.getwidth()+x-1<=figuraB.getposx() + figuraB.getwith()-1: 
                                return False
                                break
                    elif fA in self.figuras_nao_colocadas:
                        figuraB = self.figuras_colocadas[fB]
                        figuraA = self.figuras_nao_colocadas[fA]
                        if x == figuraB.getposx() + figuraB.getwidth() or x + figuraA.getwidth()-2 == figuraB.getposx():
                            if y<=figuraB.getposy()<=y+figuraA.getheight()-1 or y<=figuraB.getposy()+figuraB.getheight()-1<=y+figuraA.getheight()-1 or figuraB.getposy()<=y<=figuraB.getposy() + figuraB.getheight()-1 or figuraB.getposy()<=figuraA.getheight()+y - 1<=figuraB.getposy() + figuraB.getheight()-1: 
                                return False
                                break
                        if y  == figuraB.getposy() + figuraB.getheight() or y + figuraA.getheight()-1 == figuraB.getposy()-1:
                            if x<=figuraB.getposx()<=x+figuraA.getwidth()-1 or x<=figuraB.getposx()+figuraB.getwidth()-1<=x+figuraA.getwidth()-1 or figuraB.getposx()<=x<=figuraB.getposx() + figuraB.getwith()-1 or figuraB.getposx()<=figuraA.getwidth()+x-1<=figuraB.getposx() + figuraB.getwith()-1: 
                                return False
                                break
                elif fB in self.figuras_nao_colocadas:   # verifica se fB ainda não foi colocada
                    return True
            elif fig.getnome() == fB:     # encontrei a figura na lista de restrições como uma que tinha de estar separada
                if fA in self.figuras_colocadas:    # verifica se fA já foi colocada
                    if fB in self.figuras_colocadas:
                        figuraA = self.figuras_colocadas[fA]
                        figuraB = self.figuras_colocadas[fB]
                        if x == figuraA.getposx() + figuraA.getwidth() or x + figuraB.getwidth()-2 == figuraA.getposx():
                            if y<=figuraA.getposy()<=y+figuraB.getheight()-1 or y<=figuraA.getposy()+figuraA.getheight()-1<=y+figuraB.getheight()-1 or figuraA.getposy()<=y<=figuraA.getposy() + figuraA.getheight()-1 or figuraA.getposy()<=figuraB.getheight()+y - 1<=figuraA.getposy() + figuraA.getheight()-1: 
                                return False
                                break
                        if y  == figuraA.getposy() + figuraA.getheight() or y + figuraB.getheight()-1 == figuraA.getposy()-1:
                            if x<=figuraA.getposx()<=x+figuraB.getwidth()-1 or x<=figuraA.getposx()+figuraA.getwidth()-1<=x+figuraB.getwidth()-1 or figuraA.getposx()<=x<=figuraA.getposx() + figuraA.getwith()-1 or figuraA.getposx()<=figuraB.getwidth()+x-1<=figuraA.getposx() + figuraA.getwith()-1: 
                                return False
                                break
                    if fB in self.figuras_nao_colocadas:
                        figuraA = self.figuras_colocadas[fA]
                        figuraB = self.figuras_nao_colocadas[fB]
                        if x == figuraA.getposx() + figuraA.getwidth() or x + figuraB.getwidth()-2 == figuraA.getposx():
                            if y<=figuraA.getposy()<=y+figuraB.getheight()-1 or y<=figuraA.getposy()+figuraA.getheight()-1<=y+figuraB.getheight()-1 or figuraA.getposy()<=y<=figuraA.getposy() + figuraA.getheight()-1 or figuraA.getposy()<=figuraB.getheight()+y - 1<=figuraA.getposy() + figuraA.getheight()-1: 
                                return False
                                break
                        if y  == figuraA.getposy() + figuraA.getheight() or y + figuraB.getheight()-1 == figuraA.getposy()-1:
                            if x<=figuraA.getposx()<=x+figuraB.getwidth()-1 or x<=figuraA.getposx()+figuraA.getwidth()-1<=x+figuraB.getwidth()-1 or figuraA.getposx()<=x<=figuraA.getposx() + figuraA.getwith()-1 or figuraA.getposx()<=figuraB.getwidth()+x-1<=figuraA.getposx() + figuraA.getwith()-1: 
                                return False
                                break
                elif fA in self.figuras_nao_colocadas:      # verifica se fA ainda não foi colocada
                    return True
        return valido    #se estiver de acordo com a restrição retorna True


    def __valida_rest_dentro(self, fig, x, y):
        valido = True
        for (f, a) in self.rest_DENTRO:  # cada elemento desta lista é um tuplo do genero (f,a) em que a f tem de estar dentro de a
            if fig.getnome() == f:
                if a in self.areas:  # pois se a não estiver definida não vai haver qualquer problema em colocar fig
                    if f in self.figuras_colocadas:  
                        a = self.areas[a]
                        fA=self.figuras_colocadas[f]
                        # testar que a instancia fig tem de estar dentro de a
                        if x >= a.getx() and y >= a.gety() and x + fA.getwidth() -1 <= a.getx() + a.gettamx() - 1 and y + fA.getheight() - 1 <= a.gety() + a.gettamy() - 1:
                            valido = True
                            break
                        else:
                            valido = False
                            break
                    if f in self.figuras_nao_colocadas:  
                        a = self.areas[a]
                        fA=self.figuras_nao_colocadas[f]
                       
                        if x >= a.getx() and y >= a.gety() and x + fA.getwidth() -1 <= a.getx() + a.gettamx() - 1 and y + fA.getheight() - 1 <= a.gety() + a.gettamy() - 1:
                            valido = True
                            break
                        else:
                            valido = False
                            break
        return valido
    
    def __valida_rest_fora(self, fig, x, y):
        valido = True
        for (f, a) in self.rest_FORA:  # cada elemento desta lista é um tuplo do genero (f,a) em que a f tem de estar fora de a
            if fig.getnome() == f:  
                if a in self.areas:  # pois se a não estiver definida não vai haver qualquer problema em colocar f
                    if f in self.figuras_colocadas:  
                        a = self.areas[a]
                        fA=self.figuras_colocadas[f]
                        
                        if  (x >= a.getx() and x <= a.getx() + a.gettamx() -1) or (y >= a.gety() and y<=a.gety() + a.gettamy()-1) or (x + fA.getwidth() -1 >= a.getx() and x + fA.getwidth() -1 <= a.getx() + a.gettamx() - 1) or (y + fA.getheight() -1 >= a.gety() and y + fA.getheight() - 1 <= a.gety() + a.gettamy() - 1):
                            valido = False
                            break
                        else:
                            valido=True
                            break
                    elif f in self.figuras_nao_colocadas: 
                        
                        a = self.areas[a]
                        fA=self.figuras_nao_colocadas[f]
                        
                        if  (x >= a.getx() and x <= a.getx() + a.gettamx() -1) or (y >= a.gety() and y<=a.gety() + a.gettamy()-1) or (x + fA.getwidth() -1 >= a.getx() and x + fA.getwidth() -1 <= a.getx() + a.gettamx() - 1) or (y + fA.getheight() -1 >= a.gety() and y + fA.getheight() - 1 <= a.gety() + a.gettamy() - 1):
                            valido = False
                            break
                        else:
                            valido=True
                            break
        return valido
    
    def rest_dir(self, nomeA, nomeB):  
        tup = (nomeA, nomeB)
        if tup in self.rest_ESQ:   #verificar se não há contradições entre restrições
            return 'NÃO'
        if nomeA in self.figuras_colocadas:      #caso as figuras ja estejam colocadas
            if nomeB in self.figuras_colocadas:
                fA=self.figuras_colocadas[nomeA]  #encontrei a figura ja colocada que teria de estar à direita de fB
                fB=self.figuras_colocadas[nomeB]
                if fA.getposx() <= fB.getposx2():   #se fA nao estiver a direita de fB
                    return 'NÃO'
                else:
                    self.rest_DIR.append(tup)      
                    return 'SIM'
        self.rest_DIR.append(tup)   #se alguma das figuras ainda nao estiver colocada, podemos adiciona-la a respetiva lista das restricoes, sem qualque problema
        return "SIM"                # o mesmo raciocinio e usado nas funcoes seguintes
    
    def rest_esq(self, nomeA, nomeB):  
        tup = (nomeA, nomeB)
        if tup in self.rest_DIR:
            return 'NÃO'
        if nomeA in self.figuras_colocadas:       #caso as figuras ja estejam colocadas
            if nomeB in self.figuras_colocadas:
                fA=self.figuras_colocadas[nomeA]    #encontrei a figura ja colocada que teria de estar à esquerda de fB
                fB=self.figuras_colocadas[nomeB]
                if fB.getposx() <= fA.getposx2():  #se fA nao estiver a esquerda de fB
                    return 'NÃO'
                else:
                    self.rest_ESQ.append(tup) 
                    return 'SIM'
        self.rest_ESQ.append(tup)
        return "SIM"
    
    def rest_cim(self, nomeA, nomeB):  
        tup = (nomeA, nomeB)
        if tup in self.rest_BX:
            return 'NÃO'
        if nomeA in self.figuras_colocadas:
            if nomeB in self.figuras_colocadas:
                fA=self.figuras_colocadas[nomeA]
                fB=self.figuras_colocadas[nomeB]
                if fA.getposy2() >= fB.getposy():
                    return 'NÃO'
                else:
                    self.rest_CIM.append(tup) 
                    return 'SIM'
        self.rest_CIM.append(tup)
        return "SIM"
    
    def rest_bx(self, nomeA, nomeB):  
        tup = (nomeA, nomeB)
        if tup in self.rest_CIM:
            return 'NÃO'
        if nomeA in self.figuras_colocadas:
            if nomeB in self.figuras_colocadas:
                fA=self.figuras_colocadas[nomeA]
                fB=self.figuras_colocadas[nomeB]
                if fA.getposy() <= fB.getposy2():
                    return 'NÃO'
                else:
                    self.rest_BX.append(tup) 
                    return 'SIM'
        self.rest_BX.append(tup)
        return "SIM"
    
    def rest_cld(self, nomeA, nomeB):  
        tup = (nomeA, nomeB)
        if tup in self.rest_SEP:
            return 'NÃO'
        if nomeA in self.figuras_colocadas:
            if nomeB in self.figuras_colocadas:
                figuraA=self.figuras_colocadas[nomeA]
                figuraB=self.figuras_colocadas[nomeB]
                x=figuraA.getposx()
                y=figuraA.getposy()
                if x == figuraB.getposx() + figuraB.getwidth() or x + figuraA.getwidth()-2 == figuraB.getposx():  #verifica um dos lados verticais em posições seguidas
                    if y<=figuraB.getposy()<=y+figuraA.getheight()-1 or y<=figuraB.getposy()+figuraB.getheight()-1<=y+figuraA.getheight()-1 or figuraB.getposy()<=y<=figuraB.getposy() + figuraB.getheight()-1 or figuraB.getposy()<=figuraA.getheight()+y - 1<=figuraB.getposy() + figuraB.getheight()-1:  #verifica se esses lados estão mesmo colados 
                        self.rest_CLD.append(tup)
                        return 'SIM'
                                
                if y  == figuraB.getposy() + figuraB.getheight() or y + figuraA.getheight()-1 == figuraB.getposy()-1:  #mesmo raciocínio para os lados horizontais
                    if x<=figuraB.getposx()<=x+figuraA.getwidth()-1 or x<=figuraB.getposx()+figuraB.getwidth()-1<=x+figuraA.getwidth()-1 or figuraB.getposx()<=x<=figuraB.getposx() + figuraB.getwith()-1 or figuraB.getposx()<=figuraA.getwidth()+x-1<=figuraB.getposx() + figuraB.getwith()-1: 
                        self.rest_CLD.append(tup)
                        return 'SIM'          
                else: 
                    return 'NÃO'
        self.rest_CLD.append(tup)
        return "SIM"
      
    def rest_sep(self, nomeA, nomeB):  
        tup = (nomeA, nomeB)
        if tup in self.rest_CLD:
            return 'NÃO'
        if nomeA in self.figuras_colocadas:
            if nomeB in self.figuras_colocadas:
                figuraA=self.figuras_colocadas[nomeA]
                figuraB=self.figuras_colocadas[nomeB]
                x=figuraA.getposx()
                y=figuraA.getposy()
                if x == figuraB.getposx() + figuraB.getwidth() or x + figuraA.getwidth()-2 == figuraB.getposx():  #verifica um dos lados verticais em posições seguidas
                    if y<=figuraB.getposy()<=y+figuraA.getheight()-1 or y<=figuraB.getposy()+figuraB.getheight()-1<=y+figuraA.getheight()-1 or figuraB.getposy()<=y<=figuraB.getposy() + figuraB.getheight()-1 or figuraB.getposy()<=figuraA.getheight()+y - 1<=figuraB.getposy() + figuraB.getheight()-1:  #verifica se esses lados estão mesmo colados 
                        self.rest_CLD.append(tup)
                        return 'NÃO'
                                
                if y  == figuraB.getposy() + figuraB.getheight() or y + figuraA.getheight()-1 == figuraB.getposy()-1:  #mesmo raciocínio para os lados horizontais
                    if x<=figuraB.getposx()<=x+figuraA.getwidth()-1 or x<=figuraB.getposx()+figuraB.getwidth()-1<=x+figuraA.getwidth()-1 or figuraB.getposx()<=x<=figuraB.getposx() + figuraB.getwith()-1 or figuraB.getposx()<=figuraA.getwidth()+x-1<=figuraB.getposx() + figuraB.getwith()-1: 
                        self.rest_CLD.append(tup)
                        return 'NÃO'          
                else:
                    self.rest_SEP.append(tup) 
                    return 'SIM'
        self.rest_SEP.append(tup)
        return "SIM"
    
    def rest_dentro(self, nomeRect, nomeArea):  
        tup = (nomeRect, nomeArea)
        if tup in self.rest_FORA:
            return 'NÃO'
        if nomeRect in self.figuras_colocadas:
            if nomeArea in self.areas:
                fA=self.figuras_colocadas[nomeRect]
                a=self.areas[nomeArea]
                if fA.getposx() >= a.getx() and fA.getposy() >= a.gety() and fA.getposx() + fA.getwidth() -1 <= a.getx() + a.gettamx() - 1 and fA.getposy() + fA.getheight() - 1 <= a.gety() + a.gettamy() - 1:
                    self.rest_DENTRO.append(tup)
                    return 'SIM'
                else: 
                    return 'NÃO'
        self.rest_DENTRO.append(tup)
        return "SIM"
    
    def rest_fora(self, nomeRect, nomeArea):  
        tup = (nomeRect, nomeArea)
        if tup in self.rest_DENTRO:   #verificar se não há contradições entre restrições
            return 'NÃO'
        if nomeRect in self.figuras_colocadas:
            if nomeArea in self.areas:
                fA=self.figuras_colocadas[nomeRect]
                a=self.areas[nomeArea]
                if  (fA.getposx() >= a.getx() and fA.getposx() <= a.getx() + a.gettamx() -1) or (fA.getposy() >= a.gety() and fA.getposy()<=a.gety() + a.gettamy()-1) or (fA.getposx() + fA.getwidth() -1 >= a.getx() and fA.getposx() + fA.getwidth() -1 <= a.getx() + a.gettamx() - 1) or (fA.getposy() + fA.getheight() -1 >= a.gety() and fA.getposy() + fA.getheight() - 1 <= a.gety() + a.gettamy() - 1):
                    return 'NÃO'
                else:
                    self.rest_FORA.append(tup) 
                    return 'SIM'
        self.rest_FORA.append(tup)
        return "SIM"
    
    def coloca_rodar(self, nome, px, py):
        if nome in self.figuras_nao_colocadas:
            f = self.figuras_nao_colocadas[nome]
            if f.rodar=='s':
                if self.__valida_coloca(f, px, py) == False: 
                    return "NÃO"
                else:
                    g= Figura(nome, f.getheight(), f.getwidth(), f.getrodar())
                    g.setposx(px)
                    g.setposy(py)
                    self.figuras_colocadas[nome] = g
                    del self.figuras_nao_colocadas[nome]
                    t=(g, 'COLR', nome)
                    self.s.push(t)
                    return "SIM"
        elif nome in self.figuras_colocadas:  # aqui vamos mudar o rectangulo de posição
            f = self.figuras_colocadas[nome]
            if self.__valida_coloca(f, px, py) == False: 
                return "NÃO"
            else:
                h= f.altura
                f.setheight(f.largura)   #quando queremos voltar a colocar a figura outra vez, mas usando o colr, nao so queremos que ela mude de posição, como queremos que esta rode de novo, voltando a sua forma original
                f.setwidth(h)
                if nome in self.figuras_anteriores:        #criamos um dicionario para guardar as posições anteriores de cada figura, de modo a conseguirmos restaurar a sua posição no undo
                    self.figuras_anteriores[nome]+=[(f.getposx(), f.getposy())]  #se não for a primeira vez que estamos a mudar a figura de posição, apenas adicionamos, antes de a mudarmos de posição, as suas coordenadas ao dicionario como valores da chave correspondente ao nome da figura
                else:                                                            # assim, o ultimo tuplo da lista correspondente ao nome da figura(chave) corresponde a última posição que esta ocupou antes de ser alterada
                    self.figuras_anteriores[nome]=[(f.getposx(), f.getposy())]
                f.setposx(px)
                f.setposy(py)
                t=(f, 'COLR', nome)
                self.s.push(t)
                return "SIM"
        elif nome not in self.figuras_nao_colocadas and nome not in self.figuras_colocadas:
            return 'NÃO' 
         
    def __nao_sobrepoe(self,g, x, y):
        for f in self.figuras_colocadas.values():  #ver se a fig cai em cima de alguma figura f da lista de figuras co,ocadas
            if f.getnome()!= g.getnome():          #para, no caso de estarmos a mudar a posição de uma figura já colocada, a posião atual desta não interferir
                if x>= f.getposx() and x<= f.getposx2() and y>= f.posy and y<= f.getposy2():   #primeiro vertice (x,y)
                    return False
                if x+g.getwidth() - 1>= f.getposx() and x+g.getwidth()-1<= f.getposx2() and y>= f.getposy() and y<= f.getposy2(): #segundo vertice (x2,y)
                    return False
                if x>= f.getposx() and x<= f.getposx2() and y+g.getheight()-1>= f.getposy() and y+g.getheight()-1<= f.getposy2():  # terceiro vertice (x,y2)
                    return False
                if x+g.getwidth()-1>= f.getposx() and x+g.getwidth()-1<= f.getposx2() and y+g.getheight()-1>= f.getposy() and y+g.getheight()-1<= f.getposy2(): #quarto vertice (x2,y2)
                    return False
                #verifica se a figura ja existente fica contida dentro da que queremos colocar
                if f.getposx()>= x and f.getposx()<= x+g.getwidth()-1 and f.getposy()>= y and f.getposy()<= y+g.getheight()-1:   #primeiro vertice (ver rascunho tarefa 9 no caderno)
                    return False
                if f.getposx2()>= x and f.getposx2()<= x+g.getwidth()-1 and f.getposy()>= y and f.getposy()<= y+g.getheight()-1: #segundo vertice
                    return False
                if f.getposx()>= x and f.getposx()<= x+g.getwidth()-1  and f.getposy2()>= y and f.getposy2()<= y+g.getheight()-1:  # terceiro vertice
                    return False
                if f.getposx2()>= x and f.getposx2()<= x+g.getwidth()-1 and f.getposy2()>= y and f.getposy2()<= y+g.getheight()-1: #quarto vertice
                    return False
        return True
    
    def __valida_rest_dentro_sup_areas(self, x, y, tamx, tamy):
        if x >= 1 and y >= 1 and x + tamx - 1 <= self.largura and y + tamy - 1 <= self.altura:
            return True
        else:
            return False
        
    def nova_area(self, nome, x, y, tamx, tamy):
        if nome in self.areas:
            return "NÃO"
        if self.__valida_rest_dentro_sup_areas( x, y,tamx, tamy)==True:  #verificar se a area esta dentro da dimensao
            f= Area(nome, x, y, tamx, tamy)
            self.areas[nome]=f
            t=(f, 'AREA', nome)
            self.s.push(t)
            return "SIM"
        else:
            return 'NÃO'
    
    def getlargura(self):
        return self.largura
    
    def getaltura(self):
        return self.altura
    
    def getfiguras_colocadas(self):
        return self.figuras_colocadas

    def getfiguras_nao_colocadas(self):
        return self.figuras_nao_colocadas
    
    def stack_to_list(self, stack):
        s=stack
        L=[]
        stemp=Stack()
        while not s.is_empty():
            t= s.pop()
            L.append(t)
            stemp.push(t)
        while not stemp.is_empty():
            s.push(stemp.pop())
        return L
        
    def rest_undo(self):
        if not self.s.is_empty():    
    
            T=self.s.pop()   
            f= T[0]   #o meu f sera a figura, area ou a dimensao, dependendo do ultimo comando efetuado
            com= T[1]  #o meu com e o ultimo comando efetuado
            nome = T[2]
            L= self.stack_to_list(self.s)
            print(L)
            
            if com == 'COL':
                for el in L:
                 
                    if el[2] == f.getnome(): #a primeira figura que encontrar na lista com um nome igual ao da figura (f) que queremos eliminar corresponde ao ultimo estado(posição, dimensão) de f, antes desta ter mudado de posição
                        nome= el[2]
                        l= len(self.figuras_anteriores[nome])
                        t=self.figuras_anteriores[nome][l-1]
                        
                        x = t[0]    
                        y= t[1]
                        print(x,y)
                        f.setposx(x)
                        f.setposy(y)
                        del self.figuras_anteriores[nome][l-1]
                        if not self.__valida_coloca(f, x, y):
                            return 'E_RESTR'
                            break
                        else:
                            return 'SIM'
                            break
                f.setposx(-1)
                f.setposy(-1)
                self.figuras_nao_colocadas[f.getnome()]=f
                del self.figuras_colocadas[f.getnome()]
                return 'SIM'
                    
            if com == 'COLR':
                for el in L:
                   
                    if el[2] == f.getnome():
                        print('aaaa')
                        nome=el[2]
                        l= len(self.figuras_anteriores[nome])
                        t=self.figuras_anteriores[nome][l-1]
                        
                        x = t[0]    #É AQUI QUE DÁ MAL
                        y= t[1]
                        print(x,y)
                        f.setposx(x)
                        f.setposy(y)
                        h= f.altura
                        f.setheight(f.largura)   #anulamos tambem a sua rotação
                        f.setwidth(h)
                        del self.figuras_anteriores[nome][l-1]
                        if not self.__valida_coloca(f, x, y):
                            return 'E_RESTR'
                            break
                        else:
                            return 'SIM'
                            break
                
                    f.setposx(-1)
                    f.setposy(-1)
                    h= f.altura           #aqui estamos a anular a rotação que a figuar sofreu
                    f.setheight(f.largura)
                    f.setwidth(h)
                    self.figuras_nao_colocadas[f.getnome()]=f
                    del self.figuras_colocadas[f.getnome()]
                    return 'SIM'
                    break
                    
            elif com == 'AREA':
                del self.areas[nome]
                return 'SIM'
            
            elif L==[]:             #como o primeiro elemento da stack corresponde a dimensão, quando fazemos o pop deste, a nossa lista L ficará vazia
                return 'DIM'
        else:
            return 'NÃO'
    
    def __valida_rsv(self, fig, posx, posy):
            if not self.__valida_rest_dentro_sup(fig, posx, posy):
                return False
            if not self.__nao_sobrepoe(fig, posx, posy):
                return False #vai sobrepor a nenhum outro rectangulo e cai dentro da dimensao
        
    def coloca_auto(self, f, px, py):    
        
        if RetangulosEngine.__valida_rsv(self, f, px, py)==True:  
            f = self.figuras_nao_colocadas[f.nome]    
            f.setposx(px)   
            f.setposy(py)   
            self.figuras_colocadas[f.nome] = f
            if not self.__valida_coloca(f, px, py): 
                return 'E_RESTR'
            else:
                return True
        else:
            return False
        
        
    def coloca_rodar_auto(self, f, px, py):   
            f=self.figuras_nao_colocadas[f.nome]       
            if f.rodar=='s':    
                g= Figura(f.nome, f.altura, f.largura, f.rodar)   
                g.setposx(px)    
                g.setposy(py)  
                del self.figuras_nao_colocadas[f.nome]   
                self.figuras_nao_colocadas[f.nome] = g    
                if RetangulosEngine.__valida_rsv(self, g, px, py)==True:  
                    self.figuras_colocadas[f.nome] = g
                    if not self.__valida_coloca(f, px, py): 
                        return 'E_RESTR'
                    else:
                        return True     
                else:
                    del self.figuras_nao_colocadas[f.nome]     
                    self.figuras_nao_colocadas[f.nome] = f     
                    return False
    
    
    def resolve(self):  
        for f in self.figuras_nao_colocadas.values():   #percorrer a lista de figuras não colocadas
            g=self.figuras_nao_colocadas[f.nome]   
            if f.nome in self.figuras_colocadas:   
                break  
            else:
                for i in range (1, (self.largura-g.largura+1)):  
                    j=1 
                    if f.nome in self.figuras_colocadas:   
                        break 
                    else:
                        while(1<=j< (self.altura-g.altura+1)): 
                            if RetangulosEngine.coloca_auto(self, g, i, j)==True:  
                                break
                            else:
                                j+=1   
        for f in self.figuras_colocadas.values():    #depois de a figura ser colocada
            if f.nome in self.figuras_nao_colocadas:   #temos de eliminá-la da lista das não colocadas
                self.desfrsv.append(f.nome)  
                del self.figuras_nao_colocadas[f.nome]
                  
        for f in self.figuras_nao_colocadas.values():    #vamos tentar colocar as restantes, rodando-as tambem
            g=self.figuras_nao_colocadas[f.nome]    
            if f.nome in self.figuras_colocadas:   
                break   
            else:
                for i in range (1, (self.largura-g.altura+1)):  
                    j=1     
                    if f.nome in self.figuras_colocadas:    
                        break   
                    else:
                        while(1<=j<(self.altura-g.largura+1)):  
                            if RetangulosEngine.coloca_rodar_auto(self, g, i, j)==True:    
                                break   
                            else:
                                j+=1
        for f in self.figuras_colocadas.values():   
            if f.nome in self.figuras_nao_colocadas:   
                self.desfrsv.append(f.nome)    
                del self.figuras_nao_colocadas[f.nome]  
        
        if len(self.figuras_nao_colocadas)>0:  
            return "NÃO HÁ SOLUÇÃO"   
        else:
            return "SIM"
                    

class Area():
    def __init__(self, nome, x, y, tamx, tamy):
        self.nome = nome
        self.x = x
        self.y = y
        self.tamx = tamx
        self.tamy = tamy
        
    def getx(self):
        return self.x
    
    def getNome(self):
        return self.nome
    
    def gety(self):
        return self.y
    
    def gety2(self):
        return self.y + self.tamy - 1
    
    def getx2(self):
        return self.x + self.tamx - 1
    
    def gettamx(self):
        return self.tamx
    
    def gettamy(self):
        return self.tamy
    
class Stack:
    def __init__(self):
        self.items = []
        
    def is_empty(self):
        return self.items == []
    
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        return self.items.pop()
    
    def top(self):
        return self.items[len(self.items)-1]
    
    def size(self):
        return len(self.items)
    