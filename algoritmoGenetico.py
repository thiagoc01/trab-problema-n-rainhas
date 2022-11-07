import random

'''
    Um tabuleiro é representado como uma lista de N espaços, onde cada espaço representa a dama em uma das N colunas, respectivamente.
    E cada espaço contém um inteiro de 0 a N - 1, representando a linha em que ela está.
'''

def tabuleiro(N, Q):
    tabuleiros = []

    for i in range(0, Q):
        tabuleiro = []

        tabuleiro = [random.randint(0, N - 1) for j in range(0, N)]

        tabuleiros.append(tabuleiro)

    return tabuleiros

def todosVizinhos(T):
    nDamas = len(T)     # Obtém a quantidade de damas no tabuleiro

    tabuleirosNovos = []

    for i in range(0, nDamas):
        posicoes = {j for j in range(0, nDamas)}    # Utiliza-se conjunto para remoção possui complexidade de tempo O(1)

        posicoes.remove(T[i]) # Remove a posição dessa dama, já que seria igual ao tabuleiro recebido

        for j in posicoes: # Movimenta a dama dessa coluna por todas as posições exceto a atual dela
            aux = T[:]
            aux[i] = j
            tabuleirosNovos.append(aux)

    
    return tabuleirosNovos

def umVizinho(T): # Basta gerar todos os tabuleiros possíveis e escolher um deles

    tabuleirosVizinhos = todosVizinhos(T)

    posicaoAleatoria = random.randint(0, len(tabuleirosVizinhos) - 1)

    return tabuleirosVizinhos[posicaoAleatoria]

def numeroAtaques(T):

    qtdAtaques = 0

    tamTabuleiro = len(T)

    for i in range(0, tamTabuleiro - 1):            # A contagem vai até a (N - 1)-ésima dama, já que ela será analisada pelas outras
        for j in range(i + 1, tamTabuleiro):        # Para não repetir a contagem, basta não olhar para trás dessa dama

            if T[i] == T[j]:            # Ataque na linha
                qtdAtaques += 1

            elif abs(i - j) == abs(T[i] - T[j]):      # Ataque na diagonal
                qtdAtaques += 1

    return qtdAtaques



'''
    Algoritmo genético
'''

def geraPopulacaoInicial(N, qtdIndividuos):
    return tabuleiro(N, qtdIndividuos)

def avaliaTabuleiro(T):

    '''
        O algoritmo genético realiza uma maximização. Logo, se obtivermos a quantidade de ataques no tabuleiro, basta invertermos o valor,
        já que queremos o menor número de ataques, até não existir nenhum.

        Com isso, quanto menos ataques, mais próximo será o valor de 1.
        A função de avaliação será 1 / numeroAtaques(T), onde essa é a função definida acima.
        Contudo, como podemos não ter ataques no tabuleiro, teremos uma divisão por 0. Para corrigir isso, basta somar 1.
        Portanto, a função final é 1 / numeroAtaques(T) + 1

        Quanto mais ataques, mais próximo o número é de 0. Quanto menos ataques, mais próximo de 1.
    '''

    return 1 / (numeroAtaques(T) + 1)


def constroiRoletaViciada(P):   # Segue o padrão do algoritmo

    roleta = []

    for individuo in P:

        avaliacao = avaliaTabuleiro(individuo)

        roleta.append(avaliacao)

    soma = sum(roleta)

    return roleta, soma

def constroiIntervalosSelecao(roleta):  # Apenas cria uma lista de intervalos, parecidos com construção de frequências em Estatística

    # Guarda o limite da última iteração

    limiteInferior = roleta[0]
    limiteSuperior = roleta[0]

    intervalos = []

    # Coloca o primeiro intervalo, que é 0 e o primeiro valor em roleta

    intervalos.append([0, roleta[0]])

    # Os demais são o teto do último intervalo e esse valor acrescido do atual a ser verificado da roleta

    for avaliacao in roleta[1 : ]:
        limiteSuperior = limiteInferior + avaliacao

        intervalos.append([limiteInferior, limiteSuperior])

        limiteInferior = limiteSuperior

    return intervalos

def realizaSelecao(P):
    populacaoIntermediaria = []

    roleta, soma = constroiRoletaViciada(P)

    intervalosSelecao = constroiIntervalosSelecao(roleta)

    for i in range(0, len(P)):      # Gera uma população de mesmo tamanho, onde um valor sorteado é encaixado nos intervalos da roleta

        intervalo = 0       # Utilizada para sabermos qual cromossomo foi escolhido com base no número sorteado

        numeroSorteado = random.uniform(0, soma)

        for intervalos in intervalosSelecao:
            
            if numeroSorteado >= intervalos[0] and numeroSorteado <= intervalos[1]:     # Se verdade, o número está nesse intervalo
                populacaoIntermediaria.append(P[intervalo])     # Coloca o tabuleiro respectivo ao intervalo
                break
            
            intervalo += 1

    return populacaoIntermediaria

def realizaCrossover(individuoUm, individuoDois, probabilidade):        # Crossover do algoritmo

    chanceSorteada = random.random()

    # O pior caso é não haver crossover, então os indivíduos serão os mesmos

    individuoUmCrossover = individuoUm

    individuoDoisCrossover = individuoDois

    if chanceSorteada <= probabilidade:

        posicaoCorte = random.randint(0, len(individuoUm) - 1)
    
        individuoUmCrossover =  individuoUm[0 : posicaoCorte] + individuoDois[posicaoCorte : ]
        individuoDoisCrossover =  individuoDois[0 : posicaoCorte] + individuoUm[posicaoCorte : ]

    return individuoUmCrossover, individuoDoisCrossover


def iniciaCrossover(P : list, probabilidade):

    populacaoNova = []

    while len(P) != 0:

        if len(P) == 1:        # População ímpar, não há como fazer pares totalmente
            populacaoNova.append(P[0])
            P.pop()
        
        else:

            posIndividuoUm = random.randint(0, len(P) - 1)
            individuoUm = P[posIndividuoUm]

            P.pop(posIndividuoUm)

            posIndividuoDois = random.randint(0, len(P) - 1)

            individuoDois = P[posIndividuoDois]

            P.pop(posIndividuoDois)

            individuoUmCrossover, individuoDoisCrossover = realizaCrossover(individuoUm, individuoDois, probabilidade)

            populacaoNova.append(individuoUmCrossover)
            populacaoNova.append(individuoDoisCrossover)


    return populacaoNova

def realizaMutacao(P, chance):

    populacaoNova = []

    for individuo in P:

        chanceSorteada = random.random()

        if chanceSorteada <= chance:

            posicaoSorteada = random.randint(0, len(individuo) - 1)

            individuo[posicaoSorteada] = random.randint(0, len(individuo) - 1)      # Troca essa posição por outra

        populacaoNova.append(individuo)
    
    return populacaoNova

def retornaMelhorIndividuo(P):      # Procura comum de maior valor pelo tabuleiro com menos ataques

    maior = avaliaTabuleiro(P[0])
    pos = 1
    posMelhor = 0
    melhor = P[0]

    for individuo in P[1 : ]:
    
        avaliacao = avaliaTabuleiro(individuo)

        if avaliacao > maior:
            melhor = P[pos]
            posMelhor = pos
            maior = avaliacao

        pos += 1

    return melhor, maior, posMelhor



def aplicaAlgoritmoGenetico(nDamas, tamPopulacao, nGeracoes, probCrossover, probMutacao, usaElitismo):

    geracoesGeradas = 0

    populacaoInicial = geraPopulacaoInicial(nDamas, tamPopulacao)

    # Guardam os melhores indivíduos de cada geração e suas notas

    melhoresIndividuos = []
    melhoresNotas = []
    melhorNotaAtual = 0

    while melhorNotaAtual != 1.0:

        if len(melhoresIndividuos) == 100:      # Reinicia para não consumir memória
            melhoresIndividuos = []
            melhoresNotas = []

        novaPopulacao = []
        melhorIndividuoAtual, melhorNotaAtual, pos = retornaMelhorIndividuo(populacaoInicial)
        melhoresIndividuos.append(melhorIndividuoAtual)
        melhoresNotas.append(melhorNotaAtual)

        if usaElitismo:
            
            novaPopulacao.append(melhorIndividuoAtual)
            populacaoInicial.pop(pos)


        populacaoSelecionada = realizaSelecao(populacaoInicial)

        populacaoCrossover = iniciaCrossover(populacaoSelecionada, probCrossover)

        novaPopulacao += realizaMutacao(populacaoCrossover, probMutacao)

        populacaoInicial = novaPopulacao

        geracoesGeradas += 1

        
    print(geracoesGeradas)
    
    return melhoresIndividuos, melhoresNotas


def main():
    a, b = aplicaAlgoritmoGenetico(32, 50, 100, 0.7, 0.01, True)

    print(f"{a}\n\n{b}")


if __name__ == "__main__":
    main()




