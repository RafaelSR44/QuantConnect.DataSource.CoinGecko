import os
import time
import requests
import pandas as pd
from datetime import datetime
from config import (
    COINGECKO_BASE_URL,
    COINGECKO_OHLC_ENDPOINT,
    CRYPTO_SYMBOLS,
    DEFAULT_VS_CURRENCY,
    DEFAULT_DAYS,
    REQUEST_DELAY,
    PROCESSED_DATA_DIR,
    OUTPUT_DATE_FORMAT
)

class CoinGeckoProcessor:
    """Processador para baixar e formatar dados OHLCV da API CoinGecko."""

    def __init__(self, base_url=COINGECKO_BASE_URL, endpoint=COINGECKO_OHLC_ENDPOINT):
        self.base_url = base_url
        self.endpoint = endpoint

    def fetch_data(self, coin_id, vs_currency=DEFAULT_VS_CURRENCY, days=DEFAULT_DAYS):
        """Busca dados OHLC da API CoinGecko para uma moeda específica."""
        url = f"{self.base_url}{self.endpoint.format(coin_id=coin_id)}?vs_currency={vs_currency}&days={days}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lança exceção para códigos de erro HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados para {coin_id}: {e}")
            return None

    def process_data(self, raw_data, symbol):
        """Processa os dados brutos da API em um DataFrame formatado."""
        if not raw_data:
            return pd.DataFrame()

        df = pd.DataFrame(raw_data, columns=['time', 'open', 'high', 'low', 'close'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['volume'] = 0  # API não fornece volume, então preenchemos com 0
        df = df[['time', 'open', 'high', 'low', 'close', 'volume']]
        df.set_index('time', inplace=True)
        return df

    def save_to_csv(self, df, symbol):
        """Salva o DataFrame em um arquivo CSV no formato esperado pelo LEAN."""
        if df.empty:
            return

        # Garante que o diretório de saída exista
        output_dir = os.path.join(PROCESSED_DATA_DIR, symbol.lower())
        os.makedirs(output_dir, exist_ok=True)

        # Formata o nome do arquivo e o conteúdo
        filename = os.path.join(output_dir, f"{symbol.lower()}.csv")
        df.to_csv(filename, header=False, date_format=OUTPUT_DATE_FORMAT)
        print(f"Dados para {symbol} salvos em {filename}")

def main():
    """Função principal para executar o processamento de dados."""
    processor = CoinGeckoProcessor()
    for coin_id, symbol in CRYPTO_SYMBOLS.items():
        print(f"Processando {symbol}...")
        raw_data = processor.fetch_data(coin_id)
        if raw_data:
            df = processor.process_data(raw_data, symbol)
            processor.save_to_csv(df, symbol)
        time.sleep(REQUEST_DELAY)  # Pausa para evitar rate limiting

if __name__ == "__main__":
    main()

