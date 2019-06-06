class NoDeBusca():
    def __init__(self, estado, acao=None, gn=0, pai=None):
        self.estado = estado
        self.acao = acao
        self.gn = gn
        self.pai = pai
    
    def __repr__(self):
        return f'NoDeBusca({self.estado!r},{self.acao!r},{self.gn!r},{self.pai!r})'
    
    def calcularAltura(self):
        altura = 0
        no = self
        while no.pai != None:
            altura += 1
            no = no.pai
        return altura
    
    def criarListaDeAcoes(self):
        raiz = not self.pai
        if raiz:
            return [] # acao da raiz é nula!
        else:
            acoes = self.pai.criarListaDeAcoes()
            acoes.append(self.acao)
            return acoes

def construir_no_raiz(estado):
    return NoDeBusca(estado)    

def construir_no_filho(no_pai, acao):
    estado_filho = no_pai.estado.transicaoPor(acao)
    gn_filho = no_pai.gn + no_pai.estado.custo(a, estado_filho)
    return NoDeBusca(estado_filho, acao, gn_filho, no_pai)