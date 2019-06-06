import no_de_busca


def busca_amplitude(inicial):
    return _busca_cega_generica(inicial, lambda q, e: q.insert(0, e))

def busca_profundidade(inicial):
    return _busca_cega_generica(inicial, lambda q, e: q.append(e))


def _busca_cega_generica(inicial, enfileirar):

    borda = [ no_de_busca.construir_no_raiz(inicial) ]
    visitados = set()
    while borda:
        
        folha = borda.pop()
        if folha.estado.isObjetivo():
            return folha
        
        visitados.add(folha.estado)
        for acao in folha.estado.acoesPossiveis():
            expandido = no_de_busca.construir_no_filho(folha, acao)
            if expandido.estado not in visitados:
                enfileirar(borda, expandido)

    raise None


# Implementação simplificada, recursiva, do professor.
def busca_com_retrocesso(inicial):
    
    visitados = set()
    def busca_com_retrocesso_rec(atual):
        if atual.isObjetivo():
            return []
        
        filhos_de_atual = (filho for filho in estado_atual.adjacentes() if filho not in visitados)
        for filho in filhos_de_atual:
            solucao = busca_com_retrocesso_rec(filho)
            if solucao != None:
                return [filho] + solucao
            else:
                visitados.add(filho)
        
        return None
    
    return busca_com_retrocesso_rec(inicial)


# Implementação fiel ao livro, mas com nomes melhorados.
def busca_com_retrocesso_estruturada(inicial):
    caminho, borda, becos, estado_atual = [inicial], [inicial], [], inicial
    while borda:
        if estado_atual.isObjetivo():
            return caminho
        
        filhos_ec = [filho for filho in estado_atual.adjacentes() if filho not in becos]
        if not filhos_ec:
            while caminho and estado_atual == caminho[0]:
                becos.append(estado_atual)
                caminho.pop(0)
                borda.pop(0)
                estado_atual = borda[0]
            caminho.append(estado_atual)
        else:
            borda = filhos_ec + borda
            estado_atual = borda[0]
            caminho.insert(0, estado_atual)
    
    return None