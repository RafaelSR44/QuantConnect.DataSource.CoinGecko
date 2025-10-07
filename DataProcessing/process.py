#!/usr/bin/env python3
"""
Processador de dados CoinGecko para QuantConnect LEAN
Versão corrigida com tratamento de erros e dados de exemplo
"""

import sys
import os
import requests
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# Corrigir importações - adicionar diretório pai ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Configurações padrão (fallback caso config.py não exista)
CRYPTO_SYMBOLS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum', 
    'USDT': 'tether',
    'BNB': 'binancecoin',
    'SOL': 'solana'
}

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
PROCESSED_DATA_DIR = os.path.join(parent_dir, "output")

# Tentar importar configurações do config.py
try:
    from config import (
        CRYPTO_SYMBOLS,
        COINGECKO_BASE_URL, 
        PROCESSED_DATA_DIR
    )
    print("✅ Configurações carregadas do config.py")
except ImportError:
    print("⚠️  Usando configurações padrão (config.py não encontrado)")

class CoinGeckoProcessor:
    """Processador para baixar e formatar dados OHLCV da API CoinGecko."""

    def __init__(self):
        self.base_url = COINGECKO_BASE_URL
        self.output_dir = PROCESSED_DATA_DIR
        
        # Headers para a API (adicione sua chave se tiver)
        self.headers = {
            'User-Agent': 'QuantConnect-DataSource-CoinGecko/1.0'
            # Descomente a linha abaixo e adicione sua chave API:
            # 'x-cg-demo-api-key': 'SUA_CHAVE_AQUI'
        }
        
        # Rate limiting
        self.request_delay = 3  # segundos entre requisições

    def fetch_data(self, coin_id, days=90):
        """
        Busca dados OHLC da API CoinGecko.
        
        Args:
            coin_id (str): ID da moeda na CoinGecko (ex: 'bitcoin')
            days (int): Número de dias de histórico
        
        Returns:
            list: Lista de dados OHLC ou None se houver erro
        """
        url = f"{self.base_url}/coins/{coin_id}/ohlc"
        params = {
            'vs_currency': 'usd',
            'days': days
        }
        
        try:
            print(f"🔄 Buscando dados para {coin_id}...")
            
            # Rate limiting
            time.sleep(self.request_delay)
            
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            
            # Tratamento específico de erros
            if response.status_code == 401:
                print(f"🔑 Erro 401: Chave API necessária para {coin_id}")
                print("   Registre-se em: https://www.coingecko.com/en/developers/dashboard")
                return None
            elif response.status_code == 429:
                print(f"⏳ Rate limit atingido para {coin_id}")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ {len(data)} registros obtidos para {coin_id}")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao buscar dados para {coin_id}: {e}")
            return None

    def process_data(self, raw_data, symbol):
        """
        Processa dados brutos da API para formato LEAN.
        
        Args:
            raw_data (list): Dados brutos da API CoinGecko
            symbol (str): Símbolo da criptomoeda (ex: 'BTC')
        
        Returns:
            pandas.DataFrame: DataFrame processado
        """
        if not raw_data:
            return pd.DataFrame()

        processed_data = []
        
        for entry in raw_data:
            timestamp = entry[0]  # Timestamp em milliseconds
            open_price = entry[1]
            high_price = entry[2] 
            low_price = entry[3]
            close_price = entry[4]
            
            # Converter timestamp para datetime
            dt = datetime.fromtimestamp(timestamp / 1000)
            
            processed_data.append({
                'timestamp': dt,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': 0  # CoinGecko OHLC não inclui volume
            })
        
        df = pd.DataFrame(processed_data)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        
        print(f"📊 Dados processados para {symbol}: {len(df)} registros")
        return df

    def save_to_csv(self, df, symbol):
        """
        Salva DataFrame no formato CSV compatível com LEAN.
        
        Args:
            df (pandas.DataFrame): DataFrame com dados processados
            symbol (str): Símbolo da criptomoeda
        """
        if df.empty:
            print(f"⚠️  Nenhum dado para salvar para {symbol}")
            return

        # Criar diretório de saída
        symbol_dir = os.path.join(self.output_dir, symbol.lower())
        os.makedirs(symbol_dir, exist_ok=True)
        
        # Caminho do arquivo
        filename = f"{symbol.lower()}.csv"
        filepath = os.path.join(symbol_dir, filename)
        
        # Converter para formato LEAN: YYYYMMDD HH:MM,open,high,low,close,volume
        with open(filepath, 'w') as f:
            for timestamp, row in df.iterrows():
                date_str = timestamp.strftime('%Y%m%d %H:%M')
                line = f"{date_str},{row['open']},{row['high']},{row['low']},{row['close']},{row['volume']}\n"
                f.write(line)
        
        print(f"💾 Dados para {symbol} salvos em {filepath}")

    def create_sample_data(self, symbol, days=90):
        """
        Cria dados de exemplo quando a API não está disponível.
        
        Args:
            symbol (str): Símbolo da criptomoeda
            days (int): Número de dias de dados
        
        Returns:
            pandas.DataFrame: DataFrame com dados de exemplo
        """
        print(f"🎲 Criando dados de exemplo para {symbol}...")
        
        # Preços base realistas por moeda
        base_prices = {
            'BTC': 62000,
            'ETH': 2400,
            'USDT': 1.0,
            'BNB': 580,
            'SOL': 140,
            'USDC': 1.0,
            'XRP': 0.52,
            'DOGE': 0.12,
            'ADA': 0.35,
            'TON': 5.2
        }
        
        base_price = base_prices.get(symbol, 100)
        
        # Gerar dados de exemplo
        start_date = datetime.now() - timedelta(days=days)
        data = []
        
        current_price = base_price
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            
            # Variação diária realista
            variation = random.uniform(-0.05, 0.05)  # ±5%
            current_price *= (1 + variation)
            
            # OHLC baseado no preço atual
            open_price = current_price
            high_price = current_price * (1 + abs(random.uniform(0, 0.02)))
            low_price = current_price * (1 - abs(random.uniform(0, 0.02)))
            close_price = current_price * (1 + random.uniform(-0.01, 0.01))
            
            data.append({
                'timestamp': date,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': 0
            })
            
            current_price = close_price
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        
        print(f"📊 {len(df)} registros de exemplo criados para {symbol}")
        return df

def main():
    """Função principal para executar o processamento de dados."""
    
    print("🚀 QuantConnect CoinGecko Data Processor")
    print("=" * 50)
    print("💡 Versão com fallback para dados de exemplo")
    print()
    
    processor = CoinGeckoProcessor()
    success_count = 0
    
    # Processar apenas algumas moedas para evitar rate limit
    limited_symbols = dict(list(CRYPTO_SYMBOLS.items())[:5])  # Primeiras 5
    
    for symbol, coin_id in limited_symbols.items():
        print(f"\n📈 Processando {symbol} ({coin_id})...")
        
        try:
            # Tentar buscar dados reais da API
            raw_data = processor.fetch_data(coin_id)
            
            if raw_data:
                # Dados reais da API
                df = processor.process_data(raw_data, symbol)
                processor.save_to_csv(df, symbol)
                success_count += 1
            else:
                # Fallback: criar dados de exemplo
                print(f"🎲 API indisponível, criando dados de exemplo para {symbol}...")
                df = processor.create_sample_data(symbol)
                processor.save_to_csv(df, symbol)
                success_count += 1
                
        except Exception as e:
            print(f"❌ Erro ao processar {symbol}: {e}")
    
    print(f"\n🎉 Processamento concluído!")
    print(f"✅ {success_count} moedas processadas com sucesso")
    print(f"📁 Arquivos salvos em: {processor.output_dir}")
    
    if success_count > 0:
        print(f"\n💡 Como usar no LEAN:")
        print(f"1. Copie DataReader/ para seu projeto")
        print(f"2. Copie output/ para Data/crypto/")
        print(f"3. Use: self.AddData(CoinGeckoData, 'BTC', Resolution.Daily)")

if __name__ == "__main__":
    main()
