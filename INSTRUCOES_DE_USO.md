# 📋 Instruções de Uso - QuantConnect.DataSource.CoinGecko

## 🚀 Como Executar (Passo a Passo)

### 1. Preparação
```bash
# Certifique-se de estar no diretório raiz do projeto
cd QuantConnect.DataSource.CoinGecko

# Instale as dependências
pip install -r requirements.txt
```

### 2. Executar o Processador de Dados

**Opção A: Script Launcher (Recomendado)**
```bash
python run_data_processor.py
```

**Opção B: Módulo Python**
```bash
python -m DataProcessing.process
```

**Opção C: Diretamente**
```bash
python DataProcessing/process.py
```

### 3. Verificar Resultados
```bash
# Ver arquivos gerados
ls -la output/

# Ver dados do Bitcoin
head output/btc/btc.csv
```

## 🔧 Solução de Problemas

### Erro: "No module named 'config'"
**Solução**: Use o script launcher
```bash
python run_data_processor.py
```

### Erro: "401 Unauthorized" ou "429 Too Many Requests"
**Solução**: O script automaticamente criará dados de exemplo

### Para usar API real (Opcional)
1. Registre-se: https://www.coingecko.com/en/developers/dashboard
2. Obtenha chave API gratuita
3. Edite `DataProcessing/process.py` linha 42:
```python
# 'x-cg-demo-api-key': 'SUA_CHAVE_AQUI'  # Descomente e adicione sua chave
```

## 📊 Estrutura de Saída

Após executar, você terá:
```
output/
├── btc/
│   └── btc.csv
├── eth/
│   └── eth.csv
├── usdt/
│   └── usdt.csv
├── bnb/
│   └── bnb.csv
└── sol/
    └── sol.csv
```

## 🤖 Como Usar no LEAN

### 1. Copiar Arquivos
```bash
# Copie o módulo DataReader para seu projeto LEAN
cp -r DataReader/ /caminho/para/seu/projeto/

# Copie os dados para o diretório Data do LEAN
cp -r output/ /caminho/para/lean/Data/crypto/
```

### 2. Código do Algoritmo
```python
from DataReader.CoinGeckoDataReader import CoinGeckoData

class MeuAlgoritmoCripto(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2024, 9, 1)
        self.SetEndDate(2024, 10, 6)
        self.SetCash(100000)
        
        # Adicionar dados customizados
        self.btc = self.AddData(CoinGeckoData, "BTC", Resolution.Daily)
        self.eth = self.AddData(CoinGeckoData, "ETH", Resolution.Daily)
        
    def OnData(self, data):
        if "BTC" in data:
            btc_price = data["BTC"].Close
            self.Log(f"Bitcoin: ${btc_price:,.2f}")
            
            if not self.Portfolio.Invested:
                self.SetHoldings("BTC", 0.8)
```

## ✅ Checklist de Verificação

- [ ] Executei `pip install -r requirements.txt`
- [ ] Executei `python run_data_processor.py`
- [ ] Verifiquei que arquivos foram criados em `output/`
- [ ] Copiei `DataReader/` para meu projeto LEAN
- [ ] Copiei dados para `Data/crypto/` do LEAN
- [ ] Testei o algoritmo de exemplo

## 🎯 Comandos Resumidos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar processador
python run_data_processor.py

# 3. Verificar resultados
ls output/

# 4. Ver dados do Bitcoin
head output/btc/btc.csv
```

## 📞 Suporte

Se ainda tiver problemas:
1. Verifique se está no diretório correto
2. Confirme que Python 3.6+ está instalado
3. Execute `python --version` para verificar
4. Execute `pip list` para ver dependências instaladas
