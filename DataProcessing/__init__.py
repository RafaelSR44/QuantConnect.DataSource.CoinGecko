"""
Módulo de Processamento de Dados

Este módulo contém as funcionalidades para baixar, processar e formatar
dados da API CoinGecko para uso no QuantConnect LEAN.
"""

from .process import CoinGeckoProcessor

__all__ = ['CoinGeckoProcessor']
