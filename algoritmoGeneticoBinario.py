import random
from math import log2
import matplotlib.pyplot as plt


'''
    Um tabuleiro é representado como uma string binária onde há N substrings de tamanho log_2(N).
    Cada i-ésima substring possui a linha da i-ésima dama.
    As colunas já são automaticamente representadas pela posição da substring na string.

    Ex.:

    4 damas:
        Dama 1 na linha 2
        Dama 2 na linha 3
        Dama 3 na linha 4
        Dama 4 na linha 1

        String: 01101100 => 01 10 11 00

        Os índices são reduzidos em 1, já que para a N-ésima linha precisaríamos de mais um bit.
'''
numDamas = 0

def tabuleiro(N, Q):
    tabuleiros = []

    for i in range(0, Q):
        tabuleiro = ''

        for j in range(0, N):
            tabuleiro += str((bin(random.randint(0, N-1))[2:].zfill(int(log2(N)))))

        tabuleiros.append(tabuleiro)

    return tabuleiros

def todosVizinhos(T):
    nDamas = numDamas    # Obtém a quantidade de damas no tabuleiro
    inicio = 0
    fim = int(log2(numDamas))
    tabuleirosNovos = []

    for i in range(0, nDamas):

        posicoes = {j for j in range(0, nDamas)}    # Utiliza-se conjunto para remoção possui complexidade de tempo O(1)

        posicaoDama = T[inicio : fim]

        posicoes.remove(int(posicaoDama, 2)) # Remove a posição dessa dama, já que seria igual ao tabuleiro recebido

        for j in posicoes: # Movimenta a dama dessa coluna por todas as posições exceto a atual dela
            aux1 = T[:inicio]
            aux2 = T[fim:]
            aux = str(bin(j)[2:].zfill(int(log2(nDamas))))
            tabuleirosNovos.append(aux1 + aux + aux2)

        inicio = fim
        fim = fim + int(log2(numDamas))
        
    return tabuleirosNovos

def umVizinho(T): # Basta gerar todos os tabuleiros possíveis e escolher um deles

    tabuleirosVizinhos = todosVizinhos(T)

    posicaoAleatoria = random.randint(0, len(tabuleirosVizinhos) - 1)

    return tabuleirosVizinhos[posicaoAleatoria]

def numeroAtaques(T):

    qtdAtaques = 0

    # Marcadores do intervalo da dama analisada

    inicio = 0

    fim = int(log2(numDamas))

    for i in range(0, numDamas - 1):
        posicaoDama = int(T[inicio : fim], 2)   # Converte para inteiro a posição da dama atual
    
        for j in range(0, len(T) - fim, int(log2(numDamas))):       # Verifica todas as damas à frente da atual

            # Intervalos para a dama que será comparada a atual

            a = fim + j
            b = fim + j + int(log2(numDamas))

            posicaoDamaAnalisada = int(T[a : b], 2)

            if posicaoDama == posicaoDamaAnalisada:     # Ataque na linha
                qtdAtaques += 1

            elif abs(posicaoDamaAnalisada - posicaoDama) == abs( (fim  /log2(numDamas) - 1) - ( ( b / int(log2(numDamas) ) ) - 1) ):        # Ataque na diagonal
                qtdAtaques += 1

        inicio = fim
        fim = fim + int(log2(numDamas))

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
            
            if numeroSorteado >= intervalos[0] and numeroSorteado <= intervalos[1]:
                populacaoIntermediaria.append(P[intervalo])
                break
            
            intervalo += 1

    return populacaoIntermediaria

def realizaCrossover(individuoUm, individuoDois, probabilidade):

    chanceSorteada = random.random()

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

        if len(P) == 1:
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

            aux1 = individuo[0 : posicaoSorteada]
            aux2 = individuo[posicaoSorteada + 1 : ]

            bit = not int(individuo[posicaoSorteada])

            # Gera o indivíduo com a posição invertida

            individuo = aux1 + str(int(bit)) + aux2

        populacaoNova.append(individuo)
    
    return populacaoNova

def retornaMelhorIndividuo(P):

    maior = avaliaTabuleiro(P[0])
    pos = 1
    posMelhor = 0
    melhor = P[0]
    somasIndividuos = maior

    for individuo in P[1 : ]:
    
        avaliacao = avaliaTabuleiro(individuo)
        somasIndividuos += avaliacao

        if avaliacao > maior:
            melhor = P[pos]
            posMelhor = pos
            maior = avaliacao

        pos += 1

    return melhor, maior, posMelhor, somasIndividuos



def aplicaAlgoritmoGenetico(nDamas, tamPopulacao, nGeracoes, probCrossover, probMutacao, usaElitismo):

    geracoesGeradas = 0

    populacaoInicial = geraPopulacaoInicial(nDamas, tamPopulacao)
    melhoresIndividuos = []
    melhoresNotas = []
    mediasIndividuos = []
    melhorNotaAtual = 0

    while geracoesGeradas < nGeracoes:

        novaPopulacao = []
        melhorIndividuoAtual, melhorNotaAtual, pos, somasIndividuos = retornaMelhorIndividuo(populacaoInicial)
        melhoresIndividuos.append(melhorIndividuoAtual)
        melhoresNotas.append(melhorNotaAtual)

        mediasIndividuos.append(somasIndividuos / tamPopulacao)

        if usaElitismo:
            
            novaPopulacao.append(melhorIndividuoAtual)
            populacaoInicial.pop(pos)


        populacaoSelecionada = realizaSelecao(populacaoInicial)

        populacaoCrossover = iniciaCrossover(populacaoSelecionada, probCrossover)

        novaPopulacao += realizaMutacao(populacaoCrossover, probMutacao)

        populacaoInicial = novaPopulacao

        geracoesGeradas += 1        

    return melhoresIndividuos, melhoresNotas, mediasIndividuos

def bestUnitPlot(x,y):
    plt.plot(x,y)
    plt.xlabel('Generations')
    plt.ylabel('Best grades')
    plt.title("Generations x adaptation function of best unit")
    plt.show()

def bestUnitMeanPlot(x,y):
    plt.plot(x,y)
    plt.xlabel('Generations')
    plt.ylabel('Average')
    plt.title("Generations x adaptation function average")
    plt.show()

def main():

    global numDamas
    numDamas = 8

    a, b, c = aplicaAlgoritmoGenetico(8, 50, 2e3, 0.75, 0.03, True)

    print(f"{a[-1]}\n\n{b[-1]}")
    x= list(range(0,len(a)))
    y= b
    bestUnitPlot(x,y)
    x= list(range(0,len(c)))
    y= c
    bestUnitMeanPlot(x, y)

if __name__ == "__main__":
    main()




