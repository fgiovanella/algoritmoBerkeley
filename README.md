# Algoritmo de Berkeley em Python

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Implementação didática do Algoritmo de Berkeley para sincronização de relógios em sistemas distribuídos, utilizando comunicação via Sockets TCP em Python.

## Sobre o Algoritmo

O Algoritmo de Berkeley é um método centralizado para sincronização de relógios. Diferente de outros algoritmos que buscam sincronizar com um tempo "universal", o Berkeley sincroniza os nós do sistema com um tempo médio entre eles, sem a necessidade de uma fonte de tempo externa.

O mestre (servidor) é eleito para coordenar o processo, que funciona nos seguintes passos:
1.  **Consulta:** O servidor solicita a hora local de cada cliente.
2.  **Resposta:** Cada cliente responde ao servidor com a diferença de tempo em relação à hora enviada pelo servidor.
3.  **Cálculo:** O servidor calcula a média de todas as diferenças de tempo recebidas (incluindo a sua própria, que é zero).
4.  **Ajuste:** O servidor envia a cada cliente o valor de ajuste necessário para que seu relógio se alinhe à média do sistema.
5.  **Sincronização:** O cliente aplica o ajuste recebido, adiantando ou atrasando seu relógio lógico.

## Funcionalidades desta Implementação

* **Arquitetura Cliente-Servidor:** Um servidor (`servidor.py`) atua como mestre do tempo e múltiplos clientes (`cliente.py`) podem se conectar a ele.
* **Comunicação TCP:** Utiliza a biblioteca `socket` do Python para uma comunicação confiável entre os nós.
* **Multithreading:** O servidor utiliza threads para gerenciar múltiplos clientes de forma concorrente e não bloqueante.
* **Relógios Lógicos:** Os clientes simulam relógios dessincronizados através de um *offset* de tempo, que é ajustado a cada ciclo de sincronização.
* **Ciclos Periódicos:** O servidor inicia um novo ciclo de sincronização a cada 20 segundos (configurável).

## Pré-requisitos

* Python 3.7 ou superior.

## Como Executar

Siga os passos abaixo para rodar a simulação.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/NOME-DO-SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-SEU-REPOSITORIO.git)
    cd NOME-DO-SEU-REPOSITORIO
    ```

2.  **Inicie o Servidor:**
    Em um terminal, execute o script do servidor. Ele ficará aguardando conexões dos clientes.
    ```bash
    python servidor.py
    ```

3.  **Inicie os Clientes:**
    Abra um **novo terminal para cada cliente** que você deseja simular e execute o script do cliente.
    ```bash
    # No Terminal 2
    python cliente.py

    # No Terminal 3
    python cliente.py

    # E assim por diante...
    ```

## Exemplo de Saída

Você observará o processo de sincronização ocorrendo periodicamente nos terminais.

**Saída do Servidor:**
```console
[SERVIDOR] Servidor iniciado em 127.0.0.1:65432. Aguardando conexões...
[NOVA CONEXÃO] ('127.0.0.1', 54310) conectado.
[NOVA CONEXÃO] ('127.0.0.1', 54312) conectado.

==================================================
[2025-09-05 09:15:30.123456] >>> INICIANDO NOVO CICLO DE SINCRONIZAÇÃO <<<
==================================================
[SERVIDOR] Meu tempo de referência: 2025-09-05 09:15:30.123456
[CLIENTE ('127.0.0.1', 54310)] Respondeu com diferença de -5123.45 ms
[CLIENTE ('127.0.0.1', 54312)] Respondeu com diferença de 8765.12 ms

[CÁLCULO] Média das diferenças: 1213.89 ms
[AJUSTE] Enviando para ('127.0.0.1', 54310) o ajuste de 6337.34 ms
[AJUSTE] Enviando para ('127.0.0.1', 54312) o ajuste de -7551.23 ms
```

**Saída de um Cliente:**
```console
[CONEXÃO] Conectado ao servidor em 127.0.0.1:65432
[RELÓGIO LOCAL] Meu offset inicial é de -5.12 segundos.
[RELÓGIO LOCAL] Minha hora inicial: 2025-09-05 09:15:05.003456

--- Ciclo de Sincronização ---
Recebi tempo de referência do servidor: 2025-09-05 09:15:30.123456
Minha hora local no momento era:       2025-09-05 09:15:25.000006
Enviei a minha diferença de -5123.45 ms
Recebi instrução para ajustar meu relógio em 6337.34 ms
Minha nova hora sincronizada é: 2025-09-05 09:15:31.337346
```

## Estrutura do Projeto
```
.
├── cliente.py      # Script do nó cliente
└── servidor.py     # Script do nó servidor (mestre do tempo)
```

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
