'''
    Projeto Algoritmos Genéticos: Nadine Vasconcellos e Sophia Ferreira
    Problema de Roteamento de Robô
     
     Tamanho da população = 100
     Quantidade de pais = 10
     Seleção dos pais = torneio
     Taxa de mutação = 30
     Taxa de crossover = 60

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

MAX_PASSOS = 4 * N * N        # limite de tamanho da rota
MAX_TENTATIVAS_REPARO = 200   # limite para while de "reconectar" no crossover/mutação

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
    
def calculaCusto(rota, melhorAtual = None):
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

        #Penaliza apenas se afastar do objetivo
        distAtual = abs(objetivo[0] - posicaoAtual[0]) + abs(objetivo[1] - posicaoAtual[1])
        distProx  = abs(objetivo[0] - proxima[0]) + abs(objetivo[1] - proxima[1])
        if distProx > distAtual:
            custo += 10;

        visitadas.add(tuple(posicaoAtual));
        
        # Se o cálculo o custo já passou do melhor custo atual, não vale continuar calculando o resto da rota
        if melhorAtual is not None and custo > melhorAtual:
            return custo
        
    #Penaliza se não chegou no objetivo
    if rota[-1] != objetivo:
        custo += 500;
        
    return custo

def encontraObjetivo(posicao, objetivo, rota_atual):
    coordenadaDestino = posicao[:];
    
    if len(rota_atual) > MAX_PASSOS:
        return rota_atual, posicao;
    
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
    rota_atual.append(posicao);
    
    if(posicao == objetivo):
        return rota_atual, posicao;
    
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
    rota_atual.append(posicao);
    return rota_atual, posicao;   

def geraMovimentoAleatorio(posicao):
    coordenadaDestino = [-1,-1];
    while(coordenadaDestino[0] < 0  or coordenadaDestino[0] >= N or coordenadaDestino[1] < 0 or coordenadaDestino[1] >= N):
        movimento = random.randint(1,4);
        movX, movY = movimentos[movimento];
        coordenadaDestino[0] = movX + posicao[0];
        coordenadaDestino[1] = movY + posicao[1];
    return coordenadaDestino;    

def removeCiclos(rota):
    vistos = {}
    nova = []
    for p in rota:
        tp = tuple(p)
        if tp in vistos:
            corte = vistos[tp]
            nova = nova[:corte+1]
            vistos = {tuple(nova[i]): i for i in range(len(nova))}
        else:
            vistos[tp] = len(nova)
            nova.append(p)
    return nova


def mutacao(pai):
    filho = pai[:];
    for i in range(0, len(filho)-1):
        if tuple(filho[i]) in obstaculos:
            rotaAntesColisao = filho[:i];
            rotaAposColisao = filho[i + 1:];
            
            if len(rotaAntesColisao) == 0 or len(rotaAposColisao) == 0:
               continue
            
            posicao = geraMovimentoAleatorio(rotaAntesColisao[-1]);
            rotaAntesColisao.append(posicao);
            
            tentativas = 0
            while(posicao != rotaAposColisao[0] and tentativas < MAX_TENTATIVAS_REPARO):
                rotaAntesColisao, posicao =  encontraObjetivo(posicao, rotaAposColisao[0], rotaAntesColisao);
                tentativas += 1
            filho = rotaAntesColisao[:] + rotaAposColisao[1:]
            
    filho = removeCiclos(filho)
    
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
           rotaFilho = removeCiclos(rotaFilho)
           return rotaFilho;
       
    tentativas = 0    
    while(posicao != rotaPai2[0] and tentativas < MAX_TENTATIVAS_REPARO):
        rotaPai1, posicao =  encontraObjetivo(posicao, rotaPai2[0], rotaPai1);
        tentativas += 1
        
    rotaFilho = rotaPai1[:] + rotaPai2[:];  
    rotaFilho = removeCiclos(rotaFilho)
    
    return rotaFilho;

#------------------------------------------------------------------------------------------------------------------------------------------ 
melhorCusto = 99999;
melhorRota = [];

tamanhoPopulacao = 100
geracoes = 100;
filhosCrossover = 60
filhosMutacao = 30
populacao = []
qntPais = 10
       
#Geração da População inicial
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
    
    passos = 0
    while (posicao != objetivo and passos < MAX_PASSOS):
        coordenadaDestino[0] = posicao[0] + movimentoBase[movimentoRandomico][0]
        coordenadaDestino[1] = posicao[1] + movimentoBase[movimentoRandomico][1]
        if (0 <= coordenadaDestino[0] < N and 0 <= coordenadaDestino[1] < N):
            posicao = coordenadaDestino[:];
            rota.append(posicao)
        movimentoRandomico = random.randint(0,len(movimentoBase)-1)
        passos += 1
        
    custo = calculaCusto(rota, melhorCusto)
    populacao.append([custo, rota])
    if custo < melhorCusto:
        melhorRota = rota[:]
        melhorCusto = custo
        
#Geração das novas populações (gerações)
for iGeracao in range(0, geracoes):
    
    #Guarda o melhor antes de cortar a população
    populacao.sort(key=lambda ind: ind[0])
    elite = populacao[0][:]
    
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
    
    populacao.append(elite)
    
    #Crossover
    for i in range(0, filhosCrossover):
        pai1 = random.randint(0, qntPais-1)
        pai2 = random.randint(0, qntPais-1)
        while (pai1 == pai2):
            pai1 = random.randint(0, qntPais-1)
        pai1 = populacao[pai1][1]
        pai2 = populacao[pai2][1]
        filho = crossover(pai1, pai2)
        custo = calculaCusto(filho, melhorCusto)
        populacao.append([custo, filho])
        if custo < melhorCusto:
            melhorRota = filho[:]
            melhorCusto = custo
            iGeracao = 0
            print('Melhor custo | Crossover:', melhorCusto)
    
    # Mutação
    for i in range(0, filhosMutacao):
        pai1 = random.randint(0, qntPais-1)
        pai1 = populacao[pai1][1]
        filho = mutacao(pai1)
        custo = calculaCusto(filho, melhorCusto)
        populacao.append([custo, filho])
        if custo < melhorCusto:
            melhorRota = filho[:]
            melhorCusto = custo
            iGeracao = 0
            print('Melhor custo | Mutação:', melhorCusto)

imprimeGrafico(melhorRota);
print("\n========== Resultado AG ==========")
print("Melhor custo Final: ", melhorCusto);