#-*-coding:utf-8 -*-'''
'''
Created on 29/11/2016

@author: Carolina Gon�alves
'''
from graphics import *
from tkinter.constants import CENTER

class RetangulosWindow:
    
    '''
    Classe que cria uma janela para vizualização grafica do estado de um tabuleiro
    '''
    def __init__(self, largura, altura):
        '''
        Cria nova instancia de RetangulosWindow
        :param largura: largura da janela em pixeis
        :param altura: altura da janela em pixeis
        '''
        self.largura = largura
        self.altura = altura
        self.janela = GraphWin("Superficie", self.largura, self.altura)

    
    def __del__(self):
        self.janela.close()  # fechar a janela

    
    
    def desenhaRetangulo(self, coluna, linha, largura, altura):
        '''
        Desenha um retangulo 
        :param linha: indice da linha 
        :param coluna: indice da coluna
        :param largura: largura do retangulo
        :param altura: altura do retangulo
        '''    
        try:  
            p1 = Point(coluna, linha)
            p2 = Point(p1.getX() + largura, p1.getY() + altura)
            r = Rectangle(p1, p2)
            r.setFill("yellow")
            r.draw(self.janela)
            print("o retangulo devia ter sido desenhada")
        except:
            print("erro ao desenha o retangulo")
        return r
        
    
    def mostraJanela(self, eng):
        '''
        Percorre todo o puzzle, linha a linha e dentro de cada linha coluna a coluna, desenhando cada casa correspondente no puzzle
        '''
        try:
            self.janela.delete("all")
            for fig in eng.getfiguras_colocadas().values():    
                self.desenhaRetangulo(fig.getposx(), fig.getposy(), fig.largura, fig.altura)
                print("Retangulo:", fig.nome, fig.posx, fig.posy, fig.posx + fig.largura, fig.posy + fig.altura)
        except BaseException as e:
            print("erro ao desenhar:", e)
            return "NÃO"
        return "SIM"
                    
