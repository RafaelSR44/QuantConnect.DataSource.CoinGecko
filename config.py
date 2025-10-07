"""
Configurações para o QuantConnect.DataSource.CoinGecko

Este módulo contém as configurações centralizadas para o projeto,
incluindo URLs da API, símbolos de criptomoedas e parâmetros de processamento.
"""

# Configurações da API CoinGecko
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
COINGECKO_OHLC_ENDPOINT = "/coins/{coin_id}/ohlc"

# Lista das principais criptomoedas para processamento
# Baseada nas 10 maiores por capitalização de mercado
CRYPTO_SYMBOLS = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH', 
    'tether': 'USDT',
    'binancecoin': 'BNB',
    'solana': 'SOL',
    'usd-coin': 'USDC',
    'xrp': 'XRP',
    'dogecoin': 'DOGE',
    'toncoin': 'TON',
    'cardano': 'ADA'
}

# Configurações de processamento
DEFAULT_VS_CURRENCY = "usd"
DEFAULT_DAYS = "max"  # Obter dados históricos completos
REQUEST_DELAY = 1.0   # Delay entre requests para evitar rate limiting

# Configurações de arquivo
CSV_DATE_FORMAT = "%Y-%m-%d"
OUTPUT_DATE_FORMAT = "%Y%m%d %H:%M"

# Diretórios
DATA_DIR = "data"
PROCESSED_DATA_DIR = "data/crypto"
