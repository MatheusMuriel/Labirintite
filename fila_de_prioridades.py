"""
6. Utilizando a função de avaliação, implemente mais dois agentes, 
um utilizando a buscas gulosa com retrocesso e o outro a busca A*. 
Para ambas, a borda do algoritmo de busca deve ser uma fila de prioridades
portanto pesquise sobre a biblioteca `heapq`.
"""
import heapq

class FilaDePrioridades():

    def __init__(self):
        self.fila = []
        self.i = 0

    def inserir(self, objeto, prioridade):
        heapq.heappush(self.fila, (prioridade, self.i, objeto))
        self.i += 1

    def pop(self):
        return heapq.heappop(self.fila)[-1]