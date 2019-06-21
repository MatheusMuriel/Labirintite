


class HeuristicaLabirinto():

    def __init__(self, origem, destino):
        self.h = None
        self.g = None
        self.valor = None

        """Objetos do tipo espaco_estados"""
        self.origem = origem
        self.destino = destino

    def calculaHeuristica(self):
        """Calculo pela distancia de Manhattan"""
        valor_calculado = 0
        
        vx = self.origem.getValorLetra()
        vx_aux = self.destino.getValorLetra()
        n = self.origem.getNumero()
        n_aux = self.destino.getNumero()

        distancia_horizontal = n - n_aux if n > n_aux else n_aux - n
        distancia_vertical = vx - vx_aux if vx > vx_aux else vx_aux - vx

        valor_calculado = distancia_horizontal + distancia_vertical

        self.valor = valor_calculado

    def getValor(self):
        if self.valor == None:
            self.calculaHeuristica()
        return self.valor

    def is_admissivel(self):
        """
        heurística de avaliacao f(n) = g(n) + h(n), 
        tal que h(n) ≤ h∗(n) é uma heurística admissível.
        """
        return False

    def is_monotonica(self):
        return False
