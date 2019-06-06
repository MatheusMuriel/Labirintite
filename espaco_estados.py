from abc import ABC

class AbstractEstado(ABC):
    def __init__(self, is_objetivo, custo_transicao=lambda s,a,st: 1):
        self.isObjetivo = is_objetivo
        self.custoTransicao = custo_transicao
    
    @abstractmethod
    def acoesPossiveis(self):
        """ AbstractEstado -> (AbstractAcao)
        Cria um generator de ações válidas para self.
        """
        return
    
    @abstractmethod
    def transicaoPor(self, acao):
        """ AbstractEstado, AbstractAcao -> AbstractEstado
        Computa o estado adjacente a self ao aplicar uma acao válida.
        """
        return
    
    def adjacentes(self):
        """ AbstractEstado -> (AbstractEstado)
        Cria um generator de estados adjacentes a self, o estado atual.
        """
        return (self.transicaoPor(acao) for acao in self.acoesPossiveis())

