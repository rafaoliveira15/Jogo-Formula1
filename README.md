# Formula 1 Grand Prix — Jogo de Corrida

<div align="center">

![STATUS](https://img.shields.io/badge/STATUS-%20CONCLUÍDO-0F766E?style=for-the-badge) 
![VERSÃO](https://img.shields.io/badge/VERSÃO-1.0-0F766E?style=for-the-badge) 
![PYTHON](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![FLET](https://img.shields.io/badge/FLET-0F766E?style=for-the-badge) 
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)

</div>

---

# Índice

<div align="center">

[![SOBRE](https://img.shields.io/badge/SOBRE%20O%20PROJETO-0F766E?style=for-the-badge)](#sobre-o-projeto)
[![OBJETIVO](https://img.shields.io/badge/OBJETIVO-0F766E?style=for-the-badge)](#objetivo)
[![FUNCIONALIDADES](https://img.shields.io/badge/FUNCIONALIDADES-0F766E?style=for-the-badge)](#funcionalidades)
[![SELEÇÃO](https://img.shields.io/badge/SELEÇÃO%20DE%20EQUIPE-0F766E?style=for-the-badge)](#seleção-de-piloto-e-equipe)
[![CORRIDA](https://img.shields.io/badge/CORRIDA-0F766E?style=for-the-badge)](#corrida)
[![CONTROLES](https://img.shields.io/badge/CONTROLES-0F766E?style=for-the-badge)](#controles)
[![PONTUAÇÃO](https://img.shields.io/badge/PONTUAÇÃO-0F766E?style=for-the-badge)](#sistema-de-pontuação)
[![PÓDIO](https://img.shields.io/badge/PÓDIO-0F766E?style=for-the-badge)](#sistema-de-pódio)
[![PAUSA](https://img.shields.io/badge/PAUSA-0F766E?style=for-the-badge)](#sistema-de-pausa)
[![GAME OVER](https://img.shields.io/badge/GAME%20OVER-0F766E?style=for-the-badge)](#game-over)
[![TECNOLOGIAS](https://img.shields.io/badge/TECNOLOGIAS-0F766E?style=for-the-badge)](#tecnologias-utilizadas)
[![CONCEITOS](https://img.shields.io/badge/CONCEITOS-0F766E?style=for-the-badge)](#conceitos-de-programação)
[![ESTRUTURA](https://img.shields.io/badge/ESTRUTURA-0F766E?style=for-the-badge)](#estrutura-do-projeto)
[![INSTALAÇÃO](https://img.shields.io/badge/INSTALAÇÃO-0F766E?style=for-the-badge)](#instalação-e-execução)
[![DESEMPENHO](https://img.shields.io/badge/DESEMPENHO-0F766E?style=for-the-badge)](#otimização-de-desempenho)
[![MELHORIAS](https://img.shields.io/badge/MELHORIAS-0F766E?style=for-the-badge)](#melhorias-futuras)
[![STATUS](https://img.shields.io/badge/STATUS-0F766E?style=for-the-badge)](#status-do-projeto)

</div>

---

# Sobre o Projeto

O **Formula 1 Grand Prix** é um jogo de corrida desenvolvido em **Python utilizando Flet**, criado com o objetivo de aplicar conceitos de programação, interface gráfica, lógica de jogos, manipulação de estados, persistência de dados e otimização de desempenho.

O jogador assume o controle de um carro de Fórmula 1 e deve desviar dos carros rivais enquanto permanece na pista pelo maior tempo possível.

Durante a partida, o sistema apresenta informações em tempo real, como:

- Pontuação;
- Velocidade;
- Traçado da pista;
- Posição do jogador;
- Carros rivais;
- Estado da corrida;
- Ranking dos melhores jogadores.

O jogo possui uma interface inspirada em uma transmissão de corrida, com pista de três faixas, carros coloridos, HUD de informações, controles de direção, sistema de pausa e tela de Game Over.

---

# Objetivo

O principal objetivo do jogo é **sobreviver o maior tempo possível na pista e alcançar a maior pontuação**.

Para isso, o jogador precisa:

- Escolher seu nome de piloto;
- Selecionar uma equipe;
- Iniciar a corrida;
- Controlar o carro;
- Desviar dos rivais;
- Acompanhar a velocidade;
- Adaptar-se às curvas da pista;
- Evitar colisões;
- Acumular pontos;
- Tentar alcançar uma posição no pódio.

A aplicação foi desenvolvida também como uma atividade prática para exercitar conceitos de desenvolvimento de software e criação de interfaces interativas.

---

# Funcionalidades

O jogo possui diferentes sistemas que trabalham em conjunto para criar a experiência de corrida.

## Principais funcionalidades

- Cadastro do nome do piloto;
- Seleção de equipe;
- Seleção visual das equipes;
- Corrida em três faixas;
- Carro controlado pelo jogador;
- Carros rivais gerados automaticamente;
- Sistema de colisão;
- Sistema de pontuação;
- Velocidade dinâmica;
- Curvas na pista;
- Indicador de traçado;
- Controles por teclado;
- Controles por botões;
- Sistema de pausa;
- Tela de Game Over;
- Opção de jogar novamente;
- Troca de piloto/equipe;
- Pódio geral;
- Ranking persistente;
- Salvamento das pontuações em JSON;
- Interface adaptada para execução em diferentes ambientes;
- Otimização das atualizações da interface.

---

# Seleção de Piloto e Equipe

Antes de iniciar a corrida, o jogador deve informar seu nome e escolher uma equipe.

A tela inicial apresenta o título:

```text
FORMULA 1
GRAND PRIX
```

Também existe um campo para informar:

- **Nome do piloto** — limite de até 16 caracteres.

## Equipes Disponíveis

O jogo disponibiliza seis equipes:

| Equipe | Cor Principal |
|---|---|
| Ferrari | Vermelho |
| Red Bull Racing | Azul |
| Mercedes | Cinza |
| McLaren | Laranja |
| Aston Martin | Verde |
| Alpine | Azul |

As equipes são configuradas diretamente no código e possuem cores diferentes para o carro e para o capacete do piloto.

## Seleção Visual

Cada equipe é apresentada em um card individual contendo:

- Representação do carro;
- Nome da equipe;
- Identidade visual própria.

Quando uma equipe é selecionada, o card recebe uma borda destacada utilizando a cor da equipe.

O botão de início somente fica disponível quando:

- O nome do piloto foi preenchido;
- Uma equipe foi selecionada.

---

# Corrida

Após escolher o piloto e a equipe, o jogador pode iniciar a corrida.

A pista possui:

- Largura de 340 pixels;
- Altura de 460 pixels;
- Três faixas;
- Bordas laterais;
- Marcas de divisão das faixas;
- Carro do jogador;
- Carros rivais.

## Estrutura da Pista

A pista é composta por três faixas de circulação.

```text
┌──────────────────────────────┐
│        │        │            │
│   🏎️   │        │     🏎️     │
│        │   🏎️   │            │
│        │        │            │
│   🏎️   │        │            │
│        │        │     🏎️     │
│        │   🏎️   │            │
└──────────────────────────────┘
```

O jogador permanece próximo à parte inferior da pista enquanto os carros rivais aparecem na parte superior e avançam em sua direção.

## Carro do Jogador

O carro do jogador é criado dinamicamente de acordo com a equipe escolhida.

A representação visual utiliza componentes do Flet para montar:

- Asa dianteira;
- Carroceria;
- Rodas;
- Cockpit;
- Capacete;
- Detalhes traseiros.

O carro do jogador possui também elementos visuais diferentes dos carros rivais para facilitar sua identificação durante a partida.

## Carros Rivais

Os carros rivais são criados dinamicamente durante a corrida.

Cada rival possui:

- Faixa da pista;
- Posição vertical;
- Equipe;
- Cor da carroceria;
- Cor do capacete.

A posição inicial é definida automaticamente e os rivais são inseridos na pista durante a execução do jogo.

## Sistema de Rivais

Os adversários aparecem em intervalos definidos pela velocidade atual da corrida.

A faixa de surgimento é escolhida aleatoriamente:

```python
lane = random.randint(0, LANE_COUNT - 1)
```

A equipe dos rivais também é selecionada aleatoriamente, evitando utilizar a mesma equipe do jogador quando existem outras opções disponíveis.

## Sistema de Colisão

O jogo possui um sistema de detecção de colisão.

A colisão acontece quando:

- O rival está na mesma faixa do jogador;
- A posição vertical do rival entra na área ocupada pelo carro do jogador.

A verificação é realizada pela função:

```python
def check_collision(rival: Rival) -> bool:
```

A lógica verifica a faixa e a sobreposição vertical dos carros.

Quando uma colisão é detectada, a corrida é encerrada e o sistema apresenta a tela de Game Over.

---

# Controles

O jogador pode controlar o carro utilizando os botões da interface ou o teclado.

## Teclado

| Tecla | Ação |
|---|---|
| ← | Mover para a esquerda |
| → | Mover para a direita |
| A | Mover para a esquerda |
| D | Mover para a direita |
| P | Pausar/continuar |
| ESC | Pausar/continuar |
| Espaço | Reiniciar após a corrida |

## Controles na Interface

A interface possui dois botões principais:

- **◄ ESQUERDA**
- **DIREITA ►**

Esses controles permitem movimentar o carro entre as três faixas disponíveis.

---

# Sistema de Pontuação

A pontuação é atualizada continuamente durante a corrida.

A cada ciclo do jogo, a pontuação aumenta de acordo com a velocidade atual:

```python
state["score"] += state["speed"] * 0.1
```

Dessa forma, quanto mais tempo o jogador permanecer na pista, maior será sua pontuação.

## Sistema de Velocidade

A velocidade aumenta gradualmente durante a corrida.

O sistema possui um limite de velocidade interna:

```python
state["speed"] = min(18.0, state["speed"] + 0.003)
```

A velocidade exibida no HUD é convertida para uma representação em KM/H.

Isso faz com que a dificuldade aumente progressivamente durante a partida.

## Sistema de Curvas

A pista não permanece completamente reta durante toda a corrida.

O sistema utiliza uma função matemática para criar um movimento de curva:

```python
curve_factor = math.sin(state["ticks"] * 0.025)
```

O resultado é utilizado para movimentar lateralmente:

- Bordas da pista;
- Divisões das faixas;
- Carro do jogador;
- Carros rivais.

## Indicador de Traçado

O HUD apresenta o estado atual da pista.

Durante a corrida podem aparecer:

- `RETA`
- `◄ CURVA ESQ`
- `CURVA DIR ►`

Isso permite que o jogador identifique visualmente quando a pista está mudando de direção.

## HUD da Corrida

Durante o jogo, o jogador possui acesso a um painel de informações.

O HUD apresenta:

- Pontos;
- Traçado;
- Velocidade.

Exemplo:

```text
┌─────────────────────────────────┐
│     PONTOS    TRAÇADO VELOCIDADE│
│       125       RETA     210    │
│                            KM/H  │
└─────────────────────────────────┘
```

Essas informações são atualizadas durante a corrida.

---

# Sistema de Pausa

O jogo possui um sistema completo de pausa.

O jogador pode pausar a corrida utilizando:

- Botão PAUSA;
- Tecla P;
- Tecla ESC.

Quando a partida é pausada, um overlay é apresentado sobre a pista:

```text
JOGO PAUSADO

Tome um ar e volte para a pista!

[ CONTINUAR ]
```

Enquanto o jogo estiver pausado, os elementos da corrida deixam de ser movimentados.

---

# Game Over

Quando o carro do jogador colide com um rival, a corrida termina.

A tela de Game Over apresenta informações como:

```text
DNF - BATEU!

Nome do piloto • Pontos

PÓDIO
```

Além disso, o jogador recebe duas opções:

- **JOGAR NOVAMENTE**
- **TROCAR PILOTO / EQUIPE**

---

# Sistema de Pódio

O jogo possui um sistema de ranking para registrar as melhores pontuações.

Após o término da corrida, a pontuação do jogador é salva automaticamente.

O sistema mantém os 20 melhores resultados.

## Pódio Geral

O ranking pode ser acessado por meio do botão:

**🏆 Ver pódio geral**

O sistema apresenta:

- 🥇 Primeiro colocado
- 🥈 Segundo colocado
- 🥉 Terceiro colocado

Além das medalhas, os demais participantes recebem sua posição numérica no ranking.

## Persistência de Dados

As pontuações são armazenadas no arquivo `leaderboard.json`.

A aplicação utiliza a biblioteca padrão `json` do Python para carregar e salvar os dados.

A estrutura armazenada contém informações como:

```json
{
  "name": "Piloto",
  "team": "Ferrari",
  "score": 150
}
```

O sistema ordena os resultados da maior para a menor pontuação e mantém somente os 20 melhores resultados.

---

# Tecnologias Utilizadas

## Python

A linguagem principal utilizada no projeto é o Python.

Foi utilizada para desenvolver:

- Lógica do jogo;
- Controle da corrida;
- Sistema de pontuação;
- Colisões;
- Geração de rivais;
- Manipulação de dados;
- Persistência do ranking;
- Controle de estados.

## Flet

O projeto utiliza Flet para construção da interface gráfica.

O framework é responsável pela criação dos:

- Botões;
- Cards;
- Campos;
- Textos;
- Pista;
- Carros;
- HUD;
- Overlays;
- Diálogos;
- Componentes interativos.

A aplicação inicializa uma janela com tamanho configurado de 400 × 760 pixels.

## JSON

O formato JSON é utilizado para persistir o ranking do jogo, no arquivo `leaderboard.json`.

Ele permite que as pontuações continuem disponíveis mesmo depois de fechar e executar novamente a aplicação.

## Bibliotecas Utilizadas

O projeto utiliza as seguintes bibliotecas:

```python
import asyncio
import json
import math
import os
import random
import flet as ft
```

Função de cada biblioteca:

| Biblioteca | Utilização |
|---|---|
| asyncio | Loop assíncrono da corrida |
| json | Persistência do ranking |
| math | Cálculo das curvas |
| os | Localização do arquivo de ranking |
| random | Geração aleatória de rivais |
| flet | Interface gráfica |

---

# Conceitos de Programação

O projeto permite aplicar diversos conceitos importantes de programação.

## Variáveis

Utilizadas para controlar:

- Velocidade;
- Pontuação;
- Faixa do jogador;
- Posição dos rivais;
- Estado da corrida;
- Estado de pausa.

## Estruturas Condicionais

Utilizadas para controlar situações como:

- Colisão;
- Pausa;
- Game Over;
- Seleção de equipe;
- Validação do nome;
- Movimentação;
- Atualização da pista.

## Funções

O código foi dividido em funções específicas para facilitar a organização. Entre elas:

- `load_leaderboard()`
- `save_score()`
- `get_top()`
- `lane_x()`
- `create_f1_car()`
- `create_car_preview()`
- `spawn_rival()`
- `check_collision()`
- `start_race()`
- `reset_game()`
- `end_game()`
- `game_tick()`
- `move_player()`
- `toggle_pause()`

## Classes

O projeto possui uma classe responsável pela representação dos carros rivais:

```python
class Rival:
```

Cada objeto `Rival` armazena informações como:

- Faixa;
- Posição;
- Equipe;
- Componente visual.

## Gerenciamento de Estado

O estado principal da partida é armazenado em um dicionário:

```python
state = {
    "player_lane": 1,
    "player_x_offset": 0.0,
    "rivals": [],
    "speed": 6.0,
    "score": 0,
    "running": False,
    "paused": False,
    "spawn_timer": 0,
    "track_offset": 0,
    "ticks": 0,
    "curve": 0.0,
    "player_name": "",
    "team": None,
    "team_index": None,
}
```

Esse objeto centraliza as principais informações necessárias para controlar a partida.

## Loop da Corrida

O jogo utiliza um loop assíncrono para atualizar continuamente a partida.

```python
async def loop():
    while True:
        game_tick()
        await asyncio.sleep(FRAME_MS / 1000)
```

O intervalo utilizado é baseado em:

```python
FRAME_MS = 35
```

resultando em aproximadamente 30 atualizações por segundo.

---

# Otimização de Desempenho

Um dos principais pontos trabalhados no projeto foi a otimização do desempenho.

Inicialmente, a aplicação realizava `page.update()` a cada atualização da corrida.

Esse comportamento poderia fazer com que toda a árvore da interface fosse atualizada aproximadamente 30 vezes por segundo, aumentando o processamento principalmente em dispositivos móveis.

Para solucionar o problema, foram utilizadas atualizações mais específicas:

```python
track_elements.update()
hud_card.update()
```

Assim, somente as áreas que realmente mudam durante a corrida são atualizadas.

---

# Estrutura do Projeto

```text
Formula-1-Grand-Prix/
│
├── jogo.py
│
├── leaderboard.json
│
└── README.md
```

## jogo.py

Arquivo principal da aplicação. Contém:

- Interface;
- Configuração da pista;
- Carros;
- Equipes;
- Lógica da corrida;
- Controles;
- Pontuação;
- Colisão;
- Pausa;
- Game Over;
- Ranking;
- Loop do jogo.

## leaderboard.json

Arquivo responsável por armazenar as melhores pontuações dos jogadores.

## README.md

Documentação do projeto, contendo:

- Descrição;
- Objetivo;
- Funcionalidades;
- Tecnologias;
- Estrutura;
- Instalação;
- Controles;
- Regras;
- Informações sobre o desenvolvimento.

---

# Instalação e Execução

## Pré-requisitos

Antes de executar o projeto, é necessário possuir:

- Python 3;
- pip;
- Flet;
- Editor de código, como VS Code.

## Instalação do Flet

Abra o terminal na pasta do projeto e execute:

```bash
pip install flet
```

## Executando o projeto

Depois de instalar as dependências, execute:

```bash
python jogo.py
```

A aplicação será iniciada e apresentará a tela de seleção do piloto e da equipe.

---

# Como Jogar

**1. Informe seu nome**

Digite o nome que será utilizado durante a corrida. Exemplo: `Rafaela`

**2. Escolha uma equipe**

Selecione uma das equipes disponíveis:

- Ferrari
- Red Bull Racing
- Mercedes
- McLaren
- Aston Martin
- Alpine

**3. Inicie a corrida**

Depois de preencher o nome e escolher a equipe, o botão **🏁 COMEÇAR CORRIDA** será habilitado.

**4. Controle o carro**

Utilize `←` `→` ou `A` `D` para mudar de faixa.

**5. Desvie dos rivais**

Os carros adversários surgem aleatoriamente na pista. Evite permanecer na mesma faixa que um rival para não colidir.

**6. Alcance a maior pontuação**

Quanto mais tempo você permanecer na pista, maior será sua pontuação.

**7. Consulte o pódio**

Depois de uma corrida, consulte o ranking geral para verificar sua posição entre os melhores pilotos.

---

# Regras do Jogo

As principais regras são:

- O jogador deve escolher um nome.
- O jogador deve escolher uma equipe.
- A corrida inicia após os dois requisitos serem preenchidos.
- O jogador deve permanecer dentro da pista.
- O jogador deve desviar dos rivais.
- Uma colisão encerra a corrida.
- A pontuação aumenta durante a corrida.
- A velocidade aumenta progressivamente.
- As curvas alteram o deslocamento visual da pista.
- A pontuação final é registrada no ranking.

---

# Interface

A interface utiliza um estilo visual inspirado em jogos de corrida modernos.

Os principais elementos são:

- Fundo escuro;
- Pista de corrida;
- Bordas coloridas;
- Carros de diferentes equipes;
- HUD;
- Indicadores de velocidade;
- Pontuação;
- Indicador de curvas;
- Botões de controle;
- Sistema de pausa;
- Tela de Game Over;
- Ranking.

## Identidade Visual

As equipes possuem cores próprias.

| Equipe | Carro |
|---|---|
| Ferrari | Vermelho |
| Red Bull Racing | Azul |
| Mercedes | Cinza |
| McLaren | Laranja |
| Aston Martin | Verde |
| Alpine | Azul |

O código também utiliza cores neon para alguns elementos da interface, criando uma identidade visual mais próxima de jogos de corrida.

## Fluxo do Sistema

```text
┌─────────────────────────┐
│     TELA INICIAL        │
│                         │
│   Nome do Piloto        │
│   Escolha da Equipe     │
│   Ver Pódio             │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    INICIAR CORRIDA      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│        CORRIDA          │
│                         │
│  Pontos                 │
│  Velocidade             │
│  Traçado                │
│  Rivais                 │
└────────────┬────────────┘
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
    Colisão      Continua
       │           │
       ▼           │
┌─────────────┐    │
│  GAME OVER  │    │
└──────┬──────┘    │
       │           │
       ▼           │
┌─────────────┐    │
│ Salvar Score│    │
└──────┬──────┘    │
       │           │
       ▼           │
┌─────────────┐    │
│    PÓDIO    │    │
└─────────────┘    │
                    │
                    └──────► Continua a corrida
```

## Arquitetura Simplificada

```text
                    jogo.py
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    Interface       Estado        Persistência
        │              │              │
        │              │              ▼
        │              │        leaderboard.json
        │              │
        ▼              ▼
      Flet        Lógica do jogo
                       │
        ┌──────────────┼───────────────┐
        │              │               │
        ▼              ▼               ▼
     Rivais         Colisão        Pontuação
        │              │               │
        └──────────────┼───────────────┘
                       │
                       ▼
                    Game Over
```

---

# Checklist de Desenvolvimento

- [x] Tela de seleção do piloto
- [x] Campo para nome
- [x] Seleção de equipe
- [x] Seis equipes disponíveis
- [x] Representação visual dos carros
- [x] Pista com três faixas
- [x] Carro do jogador
- [x] Carros rivais
- [x] Geração aleatória de rivais
- [x] Sistema de colisão
- [x] Sistema de pontuação
- [x] Sistema de velocidade
- [x] Curvas na pista
- [x] Indicador de traçado
- [x] Controles por teclado
- [x] Controles por botões
- [x] Sistema de pausa
- [x] Tela de Game Over
- [x] Opção de jogar novamente
- [x] Troca de piloto/equipe
- [x] Ranking
- [x] Persistência em JSON
- [x] Pódio geral
- [x] Otimização de atualização da interface

---

# Melhorias Futuras

Algumas funcionalidades podem ser adicionadas em versões futuras.

## Sistema de níveis

Adicionar diferentes níveis de dificuldade:

- Fácil
- Médio
- Difícil
- Extremo

## Diferentes pistas

Adicionar circuitos inspirados em diferentes características:

- Pista urbana;
- Circuito internacional;
- Pista noturna;
- Circuito com curvas mais fechadas;
- Circuito de alta velocidade.

## Sistema de combustível

Adicionar gerenciamento de combustível, obrigando o jogador a realizar estratégias durante a corrida.

## Sistema de nitro

Adicionar uma mecânica de aceleração temporária.

## Mais equipes

Adicionar novas equipes e personalizações para os carros.

## Sistema de recordes

Criar diferentes categorias de recordes:

- Maior pontuação;
- Maior velocidade;
- Maior tempo de sobrevivência;
- Maior sequência sem colisões.

## Sons

Adicionar:

- Som do motor;
- Som de colisão;
- Música de fundo;
- Efeitos de interface;
- Som de aceleração.

---

# Status do Projeto

**DESENVOLVIMENTO**

```text
████████████████████░░ 90%
```

O projeto possui atualmente os principais sistemas necessários para uma experiência funcional de corrida:

- Seleção de piloto;
- Seleção de equipe;
- Corrida;
- Rivais;
- Colisão;
- Pontuação;
- Velocidade;
- Curvas;
- Controles;
- Pausa;
- Game Over;
- Ranking;
- Persistência de dados;
- Otimização de desempenho.

---

# Considerações Finais

O Formula 1 Grand Prix demonstra a aplicação prática de conceitos de programação através da criação de um jogo interativo.

O desenvolvimento permitiu trabalhar com:

- Python;
- Flet;
- Programação orientada a objetos;
- Funções;
- Estruturas condicionais;
- Estruturas de repetição;
- Manipulação de listas e dicionários;
- Geração de dados aleatórios;
- Persistência de informações;
- Arquivos JSON;
- Programação assíncrona;
- Interfaces gráficas;
- Gerenciamento de estados;
- Detecção de colisões;
- Animação;
- Otimização de desempenho.

Além da criação da lógica de corrida, o projeto também buscou melhorar a experiência do usuário por meio de uma interface visual organizada e de atualizações específicas dos componentes da pista e do HUD, evitando atualizações desnecessárias de toda a interface a cada frame.

## Autoria

**Rafaela Oliveira**

Estudante de Desenvolvimento de Sistemas.

Projeto desenvolvido para fins educacionais e acadêmicos.

## Licença

Este projeto possui finalidade educacional e acadêmica.

O código pode ser utilizado como referência para estudos, adaptações e desenvolvimento de novos projetos, respeitando sua autoria e finalidade.

---

<div align="center">

**Formula 1 Grand Prix**

Python | Flet | JSON

Projeto educacional de desenvolvimento de jogos.

</div>
