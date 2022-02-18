#-*-coding:utf-8 -*-'''
'''
Created on 29/11/2016

@author: Carolina 
'''
from cmd import Cmd
from RetangulosWindow import RetangulosWindow
from RetangulosEngine import RetangulosEngine

    
class RetangulosShell(Cmd):
    intro = 'Interpretador de comandos de Retangulos.   Escrever help ou ? para listar os comandos disponiveis.\n'
    prompt = 'Retangulos> '
  
                            
    def do_dim(self, arg):
        " - Define uma área rectangular que come�a nas coordenadas (1, 1) até ás coordenadas (tamx, tamy): DIM tamx tamy \n"
        try:
            lista_arg = arg.split()
            largura = int(lista_arg[0])
            altura = int(lista_arg[1])
            global eng  # pois pretendo atribuir um valor a um identificador global
            if eng is not None:  # pretendo criar uma nova �rea retangular, por isso � que apago a anterior, se existir.
                del eng  # invoca o metodo destruidor de instancia __del__()
            eng = RetangulosEngine(largura, altura)
            print('SIM')
        except BaseException as e:
            print("Erro: ao criar/mostrar a area rectangular:" , str(e))
    
    def do_rect(self, arg):
        " - Define um rectângulo com um dado nome, dimensões (tamx, tamy) e se este pode ser rodado ou não (usando s ou n): RECT nome largura altura rodar \n"
        try:
            lista_arg = arg.split()
            #if len(lista_arg)!= 4 or type(lista_arg[0])!= str or type(lista_arg[1])!= int or type(lista_arg[2])!= int:
                #print('Não existe')
            nome = lista_arg[0]
            largura = int(lista_arg[1])
            altura = int(lista_arg[2])
            rodar = lista_arg[3]
            res = eng.novo_rect(nome, largura, altura, rodar)
            print(res)
        except:
            print("NÃO")
        pass
    def do_col(self, arg):    
        " - Serve para colocar o rectângulo com um dado nome nas coordenadas (x, y) i.e., o canto superior esquerdo do rectângulo fica nessas coordenadas: COL nome x y \n"
        try:
            lista_arg = arg.split() 
            nome = lista_arg[0]
            x = int(lista_arg[1])
            y = int(lista_arg[2])
            res = eng.coloca(nome, x, y)
            print(res)
        except:
            print("NÃO")
        pass

    def do_colr(self, arg):    
        " - Coloca o rectângulo mas roda-o antes (i.e., faz uma rotação de 90 graus): COLR nome x y \n"
        try:
            lista_arg = arg.split()
            nome = lista_arg[0]
            x = int(lista_arg[1])
            y = int(lista_arg[2])
            res = eng.coloca_rodar(nome, x, y)
            print(res)
        except:
            print("NÃO") 
        pass

    
    def do_dir(self, arg):    
        " - Define a restrição que o rectângulo nomeA está á direita do rectângulo nomeB: DIR nomeA nomeB  \n"
        try:
            lista_arg = arg.split()
            nomeA = lista_arg[0]
            nomeB = lista_arg[1]
            res = eng.rest_dir(nomeA, nomeB)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o DIR:", str(e))
        
        pass
    def do_esq(self, arg):    
        " - O rectângulo nomeA está á esquerda do rectângulo nomeB: ESQ nomeA nomeB  \n"
        try:
            lista_arg = arg.split()
            nomeA = lista_arg[0]
            nomeB = lista_arg[1]
            res = eng.rest_esq(nomeA, nomeB)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o ESQ:", str(e))
        pass
    def do_cim(self, arg):    
        " -  O rectângulo nomeA está por cima do rectângulo nomeB: CIM nomeA nomeB \n"
        try:
            lista_arg = arg.split()
            nomeA = lista_arg[0]
            nomeB = lista_arg[1]
            res = eng.rest_cim(nomeA, nomeB)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o CIM:", str(e))
        
    def do_bx(self, arg):    
        " - O rectângulo nomeA está por baixo do rectângulo nomeB: BX nomeA nomeB \n"
        try:
            lista_arg = arg.split()
            nomeA = lista_arg[0]
            nomeB = lista_arg[1]
            res = eng.rest_bx(nomeA, nomeB)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o BX:", str(e))
            
    def do_cld(self, arg):    
        " - Os rectângulos nomeA e nomeB tem um lado colado: CLD nomeA nomeB \n"
        try:
            lista_arg = arg.split()
            nomeA = lista_arg[0]
            nomeB = lista_arg[1]
            res = eng.rest_cld(nomeA, nomeB)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o CLD:", str(e))
     
    def do_sep(self, arg):    
        " - Os rectângulos nomeA e nomeB não podem ter um lado colado: SEP nomeA nomeB \n"
        try:
            lista_arg = arg.split()
            nomeA = lista_arg[0]
            nomeB = lista_arg[1]
            res = eng.rest_sep(nomeA, nomeB)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o SEP:", str(e))
        
    def do_area(self, arg):    
        " - Define uma área rectangular que começa no ponto com coordenadas (x, y) e acaba no ponto com coordenadas (x + tamx -1, y + tamy -1): AREA nome x y tamx tamy \n"
        try:
            lista_arg = arg.split()
            nome = lista_arg[0]
            x = int(lista_arg[1])
            y = int(lista_arg[2])
            tamx = int(lista_arg[3])
            tamy = int(lista_arg[4])
            res = eng.nova_area(nome, x, y, tamx, tamy)
            print(res)
        except:
            print("NÃO")
    
        pass
    def do_dentro(self, arg):    
        " - Restringe o rectângulo com nome nomeRect a estar completamente dentro da área com nome nomeArea: DENTRO nomeRect nomeArea \n"
        try:
            lista_arg = arg.split()
            nomeRect = lista_arg[0]
            nomeArea = lista_arg[1]
            res = eng.rest_dentro(nomeRect, nomeArea)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o DENTRO:", str(e))
    def do_fora(self, arg):    
        " - Restringe o rectângulo com nome nomeRect a estar completamente fora da área com nome nomeArea: FORA nomeRect nomeArea \n"
        try:
            lista_arg = arg.split()
            nomeRect = lista_arg[0]
            nomeArea = lista_arg[1]
            res = eng.rest_fora(nomeRect, nomeArea)
            print(res)
        except BaseException as e:
            print("Erro: ao mostrar impor o FORA:", str(e))
            
    def do_estado(self, arg):    
        " - Imprime usando a linguagem de saída dada a seguir as posições de todos os rectângulos por ordem alfabética: ESTADO \n"
        try:
            print("########## listagem de figuras colocadas ##############")
            for fig in eng.getfiguras_colocadas().values():
                print("nome: %s largura: %d altura: %d rodar: %s posx: %d posy: %d" % (fig.nome, fig.largura, fig.altura, fig.rodar, fig.posx, fig.posy))      
                print(fig.nome, fig.posx, fig.posy, fig.posx + fig.largura - 1, fig.posy + fig.altura -1)
            print("########## listagem de figuras não colocadas ##############")
            for fig in eng.getfiguras_nao_colocadas().values():
                print("nome: %s largura: %d altura: %d rodar: %s posx: %d posy: %d" % (fig.nome, fig.largura, fig.altura, fig.rodar, fig.posx, fig.posy))
                print(fig.nome, fig.posx, fig.posy, fig.posx + fig.largura - 1, fig.posy + fig.altura - 1)
        except BaseException as e:
            print("Erro: ao mostrar o estado da area rectangular:", str(e))
        pass
    def do_estado_g(self, arg):    
        " - Imprime usando a linguagem de saída dada a seguir as posições de todos os rectângulos por ordem alfabética: ESTADO \n"
        try:
            global janela  # pois pretendo atribuir um valor a um identificador global
            if janela is not None:  # pretendo criar uma nova janels para a área retangular, por isso é que apago a anterior, se existir.
                del janela  # invoca o metodo destruidor de instancia __del__()
            janela = RetangulosWindow(eng.getlargura(), eng.getaltura())
            janela.mostraJanela(eng)
            
        except BaseException as e:
            print("Erro: ao mostrar a janela com o estado da area rectangular:", str(e))
        pass
    def do_undo(self, arg):    
        " - Anula o comando anterior, desfazendo o que este fez: UNDO \n"
        try:
            global eng
            res = eng.rest_undo()
            if res == 'DIM':
                del eng   
                eng=None
                print("SIM - undo dimensão")
            else:
                print (res)
        except BaseException as e:
            print("Erro: ao mostrar/impor o UNDO:", str(e))
        pass
    
    def do_rsv(self, arg):    
        " - Resolver o problema colocando os rectângulos que ainda faltam colocar: RSV \n"
        try:
            res=eng.resolve()
            print (res)
        except BaseException as e:
            print("Erro ao resolver:", str(e))
        pass

    def do_quit(self, arg):
        "Sair do Illuminati: quit"
        print('Obrigado por ter utilizado o Rectangulos, espero que tenha sido útil!')
        return True


if __name__ == '__main__':
    eng = None
    janela = None
    sh = RetangulosShell()
    sh.cmdloop()
    


