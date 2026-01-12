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
import math

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
temperaturaInicial = 2162;
temperaturaFinal = 25;

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
        objCoordenadaDestino = geraMovimentoAleatorio(posicao);
        posicao = objCoordenadaDestino[1][:];
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
        objCoordenadaDestino = geraMovimentoAleatorio(posicao);
        posicao = objCoordenadaDestino[1][:];
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
    return [0, coordenadaDestino];    

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


def aptidao(Sol):
    tot=0
    passo=inicio[:]
    for i in Sol:
        cx, cy = movimentos[i]
        passo[0]+=cx
        passo[1]+=cy
        if tuple(passo) in obstaculos:
            tot+=1
    custo=len(Sol)+tot*50
    return(custo)
     

def imprimeGrafico(Sol):
    x=[]
    y=[]
    for i in range(len(obstaculos)):
        x.append(obstaculos[i][0])
        y.append(obstaculos[i][1])
    plt.scatter(x, y, color='y')
    
    x=[]
    y=[]
    z=[]
    w=[]
    passo=inicio[:]
    for i in Sol:
        cx, cy = movimentos[i]
        passo[0]+=cx
        passo[1]+=cy
        x.append(passo[0])
        y.append(passo[1])
        if tuple(passo) in obstaculos:
           z.append(passo[0])
           w.append(passo[1]) 
    plt.scatter(x, y, color='b')
    plt.scatter(z, w, color='r')
    plt.show()


def mutacao(pai1):
    obst=[]
    passo=inicio[:]
    for i in pai1:
        cx, cy = movimentos[i]
        passo[0]+=cx
        passo[1]+=cy
        if tuple(passo) in obstaculos:
           obst.append([i, passo[:]])        
    sai= random.randint(0, len(obst)-1) #retira o movimento que cai num obstáculo
    entra= random.randint(1,4)          #sorteia outro para substituir o movimento que vai sair
    while (entra==obst[sai][0]):
        entra= random.randint(1,4)
    pai1[sai]=entra
    filho=[]
    passo=inicio[:]
    for i in pai1:
        npasso=passo[:]
        cx, cy = movimentos[i]
        npasso[0]+=cx
        npasso[1]+=cy
        if (npasso[0]<=objetivo[0] and npasso[1]<=objetivo[1] and npasso[0]>=0 and npasso[1]>=0):
            filho.append(i)
            passo=npasso[:]
        if (passo[0]==objetivo[0] and passo[1]==objetivo[1] and npasso[0]>=0 and npasso[1]>=0):
            return(filho)
    while (passo!=objetivo):
        mv=random.randint(0,len(mov)-1) 
        npasso=passo[:]
        npasso[0]=passo[0]+movimentos[mov[mv]][0]
        npasso[1]=passo[1]+movimentos[mov[mv]][1]
        if (npasso[0]<=objetivo[0] and npasso[1]<=objetivo[1]):
            filho.append(mov[mv])
            passo=npasso[:]
        if (passo[0]==objetivo[0] and passo[1]==objetivo[1]):
            return(filho)
        

def crossover(pai1, pai2, mov):
    totMax=min(len(pai1), len(pai2))
    corte= random.randint(5,totMax-5)
    filho=pai1[0:corte]
    passo=inicio[:]
    for i in filho:
        cx, cy = movimentos[i]
        passo[0]+=cx
        passo[1]+=cy
    for i in range(corte, len(pai2)):
        npasso=passo[:]
        cx, cy = movimentos[pai2[i]]
        npasso[0]+=cx
        npasso[1]+=cy
        if (npasso[0]<=objetivo[0] and npasso[1]<=objetivo[1]):
            filho.append(pai2[i])
            passo=npasso[:]
        if (passo[0]==objetivo[0] and passo[1]==objetivo[1]):
            return(filho)
    while (passo!=objetivo):
        mv=random.randint(0,len(mov)-1) 
        npasso=passo[:]
        npasso[0]=passo[0]+movimentos[mov[mv]][0]
        npasso[1]=passo[1]+movimentos[mov[mv]][1]
        if (npasso[0]<=objetivo[0] and npasso[1]<=objetivo[1]):
            filho.append(mov[mv])
            passo=npasso[:]
        if (passo[0]==objetivo[0] and passo[1]==objetivo[1]):
            return(filho)
            

# Geração da População inicial

# Geração da População inicial

xi=inicio[0]
yi=inicio[1]
xo=objetivo[0]
yo=objetivo[1]

mov=[]
if (xi<xo):
    mov.append(2)
else:
    mov.append(4)

if (yi<yo):
    mov.append(1)
else:
    mov.append(3)

mv=random.randint(0,len(mov)-1)

cont=0
tamPop=100
populacao=[]
custoBest=999999
totPais=10
while (cont<tamPop):
    cont+=1
    passo=inicio[:]
    Sol=[]
    while (passo!=objetivo):
        npasso=passo[:]
        npasso[0]=passo[0]+movimentos[mov[mv]][0]
        npasso[1]=passo[1]+movimentos[mov[mv]][1]
        if (npasso[0]<=objetivo[0] and npasso[1]<=objetivo[1]):
            Sol.append(mov[mv])
            passo=npasso[:]
        mv=random.randint(0,len(mov)-1)      
    
    custo=aptidao(Sol)
    populacao.append([custo, Sol])
    if custo<custoBest:
        Best=Sol[:]
        custoBest=custo

contPop=0
parada=1000
while(contPop<parada):
    contPop+=1
    
    #Geração da nova população
    populacao.sort()
    populacao=populacao[0:totPais]
    
    # Crossover
    cont=0
    txCros=60
    while (cont<txCros):
        cont+=1
        pai1=random.randint(0,totPais-1)
        pai2=random.randint(0,totPais-1)
        while (pai1==pai2):
            pai1=random.randint(0,totPais-1)
        pai1=populacao[pai1][1]
        pai2=populacao[pai2][1]
        filho=crossover(pai1,pai2,mov)
        custo=aptidao(filho)
        populacao.append([custo, filho])
        if custo<custoBest:
            Best=filho[:]
            custoBest=custo
            contPop=0
            print('cros', custoBest)
    
    # Mutação
    cont=0
    txMut=30
    while(cont<txMut):
        cont+=1
        pai1=random.randint(0,totPais-1)
        pai1=populacao[pai1][1]
        filho=mutacao(pai1)
        custo=aptidao(filho)
        populacao.append([custo, filho])
        if custo<custoBest:
            Best=filho[:]
            custoBest=custo
            contPop=0
            print('mut', custoBest)

print(custoBest)
imprimeGrafico(Best)