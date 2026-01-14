# 🤖 Projeto Algoritmo Genético – Roteamento de Robô

**Autoras**: Nadine Vasconcellos e Sophia Ferreira

**Descrição Geral**: O projeto aplica a **meta-heurística** de Algoritmo Genético ao problema de roteamento de um robô em um tabuleiro com obstáculos. O robô deve sair da posição inicial (0, 0) e alcançar o objetivo (N–1, N–1), buscando **minimizar o custo total** da rota.
O processo combina uma fase inicial para geração de uma população inicial com movimentos que se direcionam ao objetivo em ordem aleatória. Em seguida, utiliza parte dessa população para gerar novas soluções por meio de crossover e mutações repetidadmente.

---

## 📝 Metaheurística Utilizada

* **Tipo:** Algoritmo Genético
* **Tamanho da população:** 100
* **Quantidade de pais:** 10
* **Seleção dos pais:** Torneio + melhor indivíduo da geração corrente
* **Taxa de mutação:** 30 (30%)
* **Taxa de crossover:** 60 (60%)
* **Critério de parada:** 100 gerações sem melhora
---
## 🔎 Análise
### 🧭 Resultado Final
O algoritmo genético apresenta reduzido tempo de resposta, aproximadamente 7 segundos, e resultados subótimos (entre 229 e 217 pontos de custo), um tanto distantes do que se tem conhecimento ser o melhor.

<div align="center">
  <img width="371" height="253" alt="plot" src="https://github.com/user-attachments/assets/8ef259ff-f1da-4647-aed3-313acceb647f" />
</div>
Entretanto, após algumas gerações é possivel obter respostas mais próximas ao otimo (131 ponos) como na rota abaixo:
<br>

<div align="center">
  <img width="371" height="253" alt="bestPlot" src="https://github.com/user-attachments/assets/407f60d4-3803-4d6c-90dc-21fd13aee46f" />
</div>

### 👥 Comparação

Em comparação à meta-heurística GRASP, em termos de resposta e custo apresentam respostas próximas. Entretanto, o GRASP possui uma resposta melhor e oriunda de menos iterações. Além de apresentar uma implementação mais simples.

Já em relação à meta-heurística SA, em termos de resposta o algoritmo genético apresentou um tempo de resposta 7x melhor que o SA, e custos melhores ou próximos. Ademais, apresenta uma lógica bem mais simples (ainda que o código tenha sido desenvolvido com base no código da professora).

Desse modo, em termos de desempenho e solução, de longe o GRASP seria o algoritmo que nos traria melhor custo benefício, seguido do Algoritmo Genético e por fim o SA. Pode-se dizer que ainda que não não seja capaz (no estado atual) de convergir para um ótimo, o algoritmo genético apresenta um desempenho bem satisfatório.
