'''
Projeto AG

Tam população = 100
Tot pais = 10
Seleção dos pais = elitismo
Tx mutação = 30
Tx crossover = 60

'''

'''
    Projeto Simulated Annealing: Nadine Vasconcellos e Sophia Ferreira
    Problema de Roteamento de Robô
'''

import random
import matplotlib.pyplot as plt

#Ambiente
random.seed(3)  #para gerar as mesmas instâncias a partir da mesma semente
N = 30
Obs = N*10
inicio = [0, 0]
objetivo = [N-1, N-1]
obstaculos = set() #gera os obstáculos sem repetição de coordenadas
while len(obstaculos) < Obs:
    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    if (x, y) != inicio and (x, y) != objetivo:
        obstaculos.add((x, y))
obstaculos = list(obstaculos) #transformação em lista para facilitar o uso de métodos
obstaculos.sort()

#Coordenadas dos movimentos possíveis: 1=Cima, 2=Direita, 3=Baixo, 4=Esquerda
movimentos = {
    1: (0, 1),   # Cima
    2: (1, 0),   # Direita
    3: (0, -1),  # Baixo
    4: (-1, 0)   # Esquerda
}

pesoMovimentos = {
    1: 10,   # Cima
    2: 10,   # Direita
    3: 5,    # Baixo
    4: 5     # Esquerda
}

random.seed();

def imprimeGrafico(melhorRota):
    x=[]
    y=[]
    for i in range(len(obstaculos)):
        x.append(obstaculos[i][0]);
        y.append(obstaculos[i][1]);
    plt.scatter(x, y, color='#f15bb5');
    
    x=[];
    y=[];
    z=[];
    w=[];
    for coordenada in melhorRota:
        x.append(coordenada[0]);
        y.append(coordenada[1]);
        if tuple(coordenada) in obstaculos:
           z.append(coordenada[0]);
           w.append(coordenada[1]);
    plt.scatter(x, y, color='#00f5d4');
    plt.scatter(z, w, color='#d00000', marker='x');
    plt.show();
    
def calculaCusto(rota):
    custo = 0;
    visitadas = set();

    for i in range(len(rota) - 1):
        posicaoAtual = rota[i];
        proxima = rota[i + 1];

        if tuple(posicaoAtual) in obstaculos:
            custo += 50;
        else:
            custo += 1;

        if tuple(posicaoAtual) in visitadas:
            custo += 10;

        dx = proxima[0] - posicaoAtual[0];
        dy = proxima[1] - posicaoAtual[1];
        if dx < 0 or dy < 0:
            custo += 10;

        visitadas.add(tuple(posicaoAtual));

    return custo

def encontraObjetivo(posicao, objetivo):
    coordenadaDestino = posicao[:];
    
    if(posicao[1] < objetivo[1]):
        movX, movY = movimentos[1];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    elif(posicao[1] > objetivo[1]):
            movX, movY = movimentos[3];
            coordenadaDestino[0] = movX + posicao[0];
            coordenadaDestino[1] = movY + posicao[1];
    if(tuple(coordenadaDestino) in obstaculos):
        posicao = geraMovimentoAleatorio(posicao);
    else:
        posicao = coordenadaDestino[:];
    rota.append(posicao);
    
    if(posicao == objetivo):
        return rota, posicao;
    
    if(posicao[0] < objetivo[0]):
        movX, movY = movimentos[2];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    elif(posicao[0] > objetivo[0]):
        movX, movY = movimentos[4];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    if(tuple(coordenadaDestino) in obstaculos):
        posicao = geraMovimentoAleatorio(posicao);
    else:
        posicao = coordenadaDestino[:];
    rota.append(posicao);
    return rota, posicao;   

def geraMovimentoAleatorio(posicao):
    coordenadaDestino = [-1,-1];
    while(coordenadaDestino[0] < 0  or coordenadaDestino[0] >= N or coordenadaDestino[1] < 0 or coordenadaDestino[1] >= N):
        movimento = random.randint(1,4);
        movX, movY = movimentos[movimento];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    return coordenadaDestino;    

def removeCiclos(rota, inicioCorte, fimCorte):
    if(len(rota) < 2):
        return rota;
    
    if(rota[inicioCorte] in rota[fimCorte:]):
        return removeCiclos(rota, inicioCorte, fimCorte + 1);
        
    elif(inicioCorte != fimCorte):
        rota = rota[:inicioCorte + 1] + rota[fimCorte:];
        inicioCorte = 0;
        fimCorte = 0;
        return rota;

def mutacao(pai):
    filho = pai[:];
    for coordenada in enumerate(filho):
        if tuple(coordenada) in obstaculos:
            rotaAntesColisao = filho[:coordenada];
            rotaAposColisao = filho[coordenada + 1:];
            posicao = geraMovimentoAleatorio(rotaAntesColisao[-1]);
            rotaAntesColisao.append(posicao);
            while(posicao != rotaAposColisao[0]):
                rotaAntesColisao, posicao =  encontraObjetivo(posicao, rotaAposColisao[0]);
            filho = rotaAntesColisao[:] + rotaAposColisao[1:];
    i = 0;
    while(i < len(filho)):
        filho = removeCiclos(filho, i, 0)
        i += 1;
    return filho
        

def crossover(pai1, pai2):
    if len(pai1) <= len(pai2):
        tamanhoMenorRota = len(pai1);
    else: 
        tamanhoMenorRota = len(pai2);
    pontoCorte = random.randint(1,tamanhoMenorRota-1);
    rotaPai1 = pai1[:pontoCorte][:];
    rotaPai2 = pai2[pontoCorte:][:];
    coordenadaDestino = rotaPai1[-1][:];
    posicao = rotaPai1[-1][:];
    for j in range(1, 4):
       movX, movY = movimentos[j];
       coordenadaDestino[0] = movX + posicao[0];
       coordenadaDestino[1] = movY + posicao[1];
       if coordenadaDestino == rotaPai2[0]:
           rotaFilho = rotaPai1[:] + rotaPai2[:];
           return rotaFilho;
    while(posicao != rotaPai2[0]):
        rotaPai1, posicao =  encontraObjetivo(posicao, rotaPai2[0]);
    rotaFilho = rotaPai1[:] + rotaPai2[:];  
    return rotaFilho;

#------------------------------------------------------------------------------------------------------------------------------------------ 
melhorCusto = 99999;
melhorRota = [];

tamanhoPopulacao = 100
geracoes = 1000;
filhosCrossover = 60
filhosMutacao = 30
populacao = []
qntPais = 10

           
# Geração da População inicial
movimentoBase = []
if (inicio[0] < objetivo[0]):
    movimentoBase.append(list(movimentos[2]));
else:
    movimentoBase.append(list(movimentos[4]));
    
if (inicio[1] < objetivo[1]):
    movimentoBase.append(list(movimentos[1]));
else:
    movimentoBase.append(list(movimentos[3]));
movimentoRandomico = random.randint(0,len(movimentoBase)-1)


for iPopulacao in range(0, tamanhoPopulacao):
    posicao = inicio[:]
    coordenadaDestino = posicao[:];
    rota = [inicio[:]]
    while (posicao != objetivo):
        coordenadaDestino[0] = posicao[0] + movimentoBase[movimentoRandomico][0]
        coordenadaDestino[1] = posicao[1] + movimentoBase[movimentoRandomico][1]
        if (coordenadaDestino[0] <= objetivo[0] and coordenadaDestino[1] <= objetivo[1]):
            posicao = coordenadaDestino[:];
            rota.append(posicao)
        movimentoRandomico = random.randint(0,len(movimentoBase)-1)      
    custo = calculaCusto(rota)
    populacao.append([custo, rota])
    if custo < melhorCusto:
        melhorRota = rota[:]
        melhorCusto = custo
        
#Geração das novas populações (gerações)
for iGeracao in range(0, geracoes):
    #Escolha dos pais
    random.shuffle(populacao);
    torneio = [];
    for i in range(0, 10):
        etapaTorneio = [];
        etapaTorneio = populacao[:5][:];
        populacao = populacao[5:][:];
        etapaTorneio.sort(key=lambda pai: pai[0]);  
        torneio.append(etapaTorneio[0][:]);
    populacao = torneio[:];
    
    #Crossover
    for i in range(0, filhosCrossover):
        pai1 = random.randint(0, qntPais-1)
        pai2 = random.randint(0, qntPais-1)
        while (pai1 == pai2):
            pai1 = random.randint(0, qntPais-1)
        pai1 = populacao[pai1][1]
        pai2 = populacao[pai2][1]
        filho = crossover(pai1, pai2)
        custo = calculaCusto(filho)
        populacao.append([custo, filho])
        if custo < melhorCusto:
            melhorRota = filho[:]
            melhorCusto = custo
            iGeracao = 0
            print('Melhor custo (Crossover):', melhorCusto)
    
    # Mutação
    for i in range(0, filhosMutacao):
        pai1 = random.randint(0, qntPais-1)
        pai1 = populacao[pai1][1]
        filho = mutacao(pai1)
        custo = calculaCusto(filho)
        populacao.append([custo, filho])
        if custo < melhorCusto:
            melhorRota = filho[:]
            melhorCusto = custo
            iGeracao = 0
            print('Melhor custo (Mutação):', melhorCusto)

imprimeGrafico(melhorRota);
print("\n========== Resultado GA ==========")
print("Melhor custo Final: ", melhorCusto);