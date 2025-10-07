
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import requests
from DataProcessing.process import CoinGeckoProcessor

@pytest.fixture
def processor():
    return CoinGeckoProcessor()

@pytest.fixture
def mock_coingecko_response():
    return [
        [1672531200000, 16500, 16800, 16400, 16750],
        [1672617600000, 16750, 17000, 16600, 16900]
    ]

@patch('requests.get')
def test_fetch_data_success(mock_get, processor, mock_coingecko_response):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = mock_coingecko_response
    mock_get.return_value = mock_response

    data = processor.fetch_data('bitcoin')
    assert data is not None
    assert len(data) == 2
    mock_get.assert_called_once()

@patch('requests.get')
def test_fetch_data_error(mock_get, processor):
    mock_get.side_effect = requests.exceptions.RequestException("Test Error")
    data = processor.fetch_data('bitcoin')
    assert data is None

def test_process_data(processor, mock_coingecko_response):
    df = processor.process_data(mock_coingecko_response, 'BTC')
    assert not df.empty
    assert list(df.columns) == ['open', 'high', 'low', 'close', 'volume']
    assert df.shape == (2, 5)
    assert df['volume'].iloc[0] == 0

def test_save_to_csv(processor, tmp_path):
    with patch('DataProcessing.process.PROCESSED_DATA_DIR', str(tmp_path)):
        df = pd.DataFrame({
            'open': [16500.0], 'high': [16800.0], 'low': [16400.0], 'close': [16750.0], 'volume': [0.0]
        }, index=[pd.to_datetime('2023-01-01')])

        processor.save_to_csv(df, 'BTC')

        # O caminho de saída agora é relativo ao tmp_path
        expected_file = tmp_path / "btc" / "btc.csv"
        assert expected_file.exists()

        with open(expected_file, 'r') as f:
            line = f.readline().strip()
            assert line == "20230101 00:00,16500.0,16800.0,16400.0,16750.0,0.0"

