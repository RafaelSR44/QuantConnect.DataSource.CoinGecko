
import pytest
from datetime import datetime
from DataReader.CoinGeckoDataReader import CoinGeckoData

@pytest.fixture
def data_reader_instance():
    """Fixture que fornece uma instância do leitor de dados."""
    return CoinGeckoData()

def test_get_source(data_reader_instance, mock_config):
    """Testa o método GetSource."""
    source_obj = data_reader_instance.GetSource(mock_config, datetime.now(), isLiveMode=False)
    assert source_obj.Source == "data/crypto/btc/btc.csv"

def test_reader_success(data_reader_instance, mock_config):
    """Testa o método Reader com uma linha de dados válida."""
    line = "20230101 00:00,16500,16800,16400,16750,0"
    data = data_reader_instance.Reader(mock_config, line, datetime.now(), isLiveMode=False)

    assert data is not None
    assert data.Symbol == mock_config.Symbol
    assert data.Time == datetime(2023, 1, 1)
    assert data.Value == 16750
    assert data["Open"] == 16500
    assert data["High"] == 16800
    assert data["Low"] == 16400
    assert data["Close"] == 16750
    assert data["Volume"] == 0

def test_reader_invalid_line(data_reader_instance, mock_config):
    """Testa o método Reader com uma linha que não começa com um dígito."""
    line = "invalid line"
    data = data_reader_instance.Reader(mock_config, line, datetime.now(), isLiveMode=False)
    assert data is None

def test_reader_empty_line(data_reader_instance, mock_config):
    """Testa o método Reader com uma linha vazia."""
    line = ""
    data = data_reader_instance.Reader(mock_config, line, datetime.now(), isLiveMode=False)
    assert data is None

def test_reader_malformed_line(data_reader_instance, mock_config):
    """Testa o método Reader com uma linha CSV malformada."""
    line = "20230101 00:00,16500,16800,16400"  # Colunas faltando
    data = data_reader_instance.Reader(mock_config, line, datetime.now(), isLiveMode=False)
    assert data is None

