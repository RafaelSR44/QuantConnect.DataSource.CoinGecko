# QuantConnect.DataSource.CoinGecko

**Submission for the Data Engineer Position at QuantConnect**

This project is a custom data source implementation for the QuantConnect LEAN engine, designed to demonstrate key data engineering skills. It provides a complete, end-to-end pipeline for fetching, processing, and integrating cryptocurrency market data from the **CoinGecko API** into a LEAN-compatible format.

---

## Visão Geral

O objetivo deste projeto é criar uma fonte de dados robusta e de fácil utilização que permita aos pesquisadores e traders do QuantConnect acessar dados históricos de preços (OHLCV) para as principais criptomoedas. A implementação segue as melhores práticas de desenvolvimento em Python, com foco em modularidade, testabilidade e documentação clara.

## Funcionalidades

- **Downloader de Dados**: Um script (`process.py`) que se conecta à API pública da CoinGecko para baixar dados OHLCV diários.
- **Processamento e Formatação**: Converte os dados JSON da API para o formato CSV exigido pelo LEAN, garantindo a compatibilidade.
- **Estrutura de Diretórios LEAN**: Salva os arquivos de dados processados na estrutura de diretórios `output/crypto/<market>/` esperada pelo motor LEAN.
- **Classe de Dados Customizada**: Uma classe `CoinGeckoData` que herda de `PythonData` para permitir a leitura e o consumo dos dados em algoritmos.
- **Cobertura de Testes**: Testes unitários abrangentes para validar a busca de dados, o processamento e a lógica de leitura.
- **Fácil Instalação**: O projeto é empacotado com dependências claras em `requirements.txt` para uma instalação simplificada.

## Estrutura do Projeto

```
QuantConnect.DataSource.CoinGecko/
├── DataProcessing/         # Módulo para download e processamento de dados
│   ├── __init__.py
│   └── process.py
├── DataReader/             # Módulo para a classe de dados customizada do LEAN
│   ├── __init__.py
│   └── CoinGeckoDataReader.py
├── tests/                  # Testes unitários
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_process.py
│   └── test_reader.py
├── config.py               # Configurações centralizadas (símbolos, URLs)
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## Como Usar

### 1. Instalação

Clone o repositório e instale as dependências necessárias.

```bash
git clone https://github.com/RafaelSR44/QuantConnect.DataSource.CoinGecko.git
cd QuantConnect.DataSource.CoinGecko
pip3 install -r requirements.txt
```

### 2. Download dos Dados

Execute o script de processamento para baixar os dados da CoinGecko. O script buscará os dados para as 10 principais criptomoedas (configuradas em `config.py`) e os salvará no diretório `output/crypto/`.

```bash
python3 DataProcessing/process.py
```

Após a execução, a estrutura de dados será semelhante a esta:

```
output/
└── crypto/
    ├── btc/
    │   └── btc.csv
    ├── eth/
    │   └── eth.csv
    └── ...
```

### 3. Integração com o LEAN

Para usar esta fonte de dados em um algoritmo do QuantConnect, siga estes passos:

1.  **Copie os Módulos**: Copie os diretórios `DataReader` e `config.py` para o diretório do seu algoritmo LEAN.
2.  **Copie os Dados**: Copie o diretório `output/crypto` gerado para o diretório `data/` da sua instalação local do LEAN.
3.  **Use no Algoritmo**: Importe e adicione os dados em seu algoritmo, como no exemplo abaixo.

#### Exemplo de Algoritmo

```python
from DataReader.CoinGeckoDataReader import CoinGeckoData

class MyCryptoAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        # Adiciona os dados customizados da CoinGecko para Bitcoin
        self.btc = self.AddData(CoinGeckoData, "BTC", Resolution.Daily)

    def OnData(self, data):
        if not self.btc.IsReady:
            return

        # Exemplo de acesso aos dados
        close_price = data["BTC"].Close
        self.Log(f"Preço de fechamento do BTC: {close_price}")

        if not self.Portfolio.Invested:
            self.SetHoldings("BTC", 1)
```

## Executando os Testes

Para garantir a qualidade e a corretude do código, execute os testes unitários usando `pytest`.

```bash
pytest tests/
```

## Principais Criptomoedas Suportadas

O projeto está configurado para processar dados das seguintes criptomoedas:

| Símbolo | Nome Completo | ID CoinGecko |
|---------|---------------|--------------|
| BTC     | Bitcoin       | bitcoin      |
| ETH     | Ethereum      | ethereum     |
| USDT    | Tether        | tether       |
| BNB     | Binance Coin  | binancecoin  |
| SOL     | Solana        | solana       |
| USDC    | USD Coin      | usd-coin     |
| XRP     | Ripple        | xrp          |
| DOGE    | Dogecoin      | dogecoin     |
| TON     | Toncoin       | toncoin      |
| ADA     | Cardano       | cardano      |

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal do projeto
- **Requests**: Para comunicação com a API CoinGecko
- **Pandas**: Para manipulação e processamento de dados
- **Pytest**: Framework de testes unitários
- **Git**: Controle de versão

## Contribuições

Este projeto foi desenvolvido como uma demonstração de habilidades de Data Engineering para a posição na QuantConnect. Ele segue as melhores práticas de desenvolvimento e está pronto para integração com o ecossistema LEAN.

---

**Desenvolvido por**: Rafael Silva Rodrigues  
**Para**: Vaga de Data Engineer na QuantConnect  
**Data**: Outubro 2025