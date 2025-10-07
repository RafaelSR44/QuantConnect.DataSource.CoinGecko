"""
Módulo de Leitura de Dados

Este módulo contém a classe CoinGeckoData que estende PythonData
para permitir que o QuantConnect LEAN leia os dados processados.
"""

from .CoinGeckoDataReader import CoinGeckoData

__all__ = ['CoinGeckoData']
