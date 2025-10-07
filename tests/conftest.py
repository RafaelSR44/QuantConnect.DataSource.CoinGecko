
import sys
import os
import pytest
from unittest.mock import MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Mock QuantConnect Dependencies ---

class MockPythonData:
    def __init__(self):
        self.Symbol = None
        self.Time = None
        self.EndTime = None
        self.Value = 0
        self._props = {}

    def __getitem__(self, key):
        return self._props.get(key)

    def __setitem__(self, key, value):
        self._props[key] = value

class MockSubscriptionDataSource:
    def __init__(self, source, transport_medium):
        self.Source = source
        self.TransportMedium = transport_medium

# Create a mock for the entire QuantConnect namespace
qc_mock = MagicMock()
qc_mock.Data.SubscriptionDataSource = MockSubscriptionDataSource
qc_mock.Python.PythonData = MockPythonData

# Inject the mock into sys.modules
sys.modules['QuantConnect'] = qc_mock
sys.modules['QuantConnect.Data'] = qc_mock.Data
sys.modules['QuantConnect.Python'] = qc_mock.Python

# --- Fixtures ---

@pytest.fixture
def mock_config():
    """Fixture for a mock SubscriptionDataConfig."""
    config = MagicMock()
    config.Symbol.Value = "BTC"
    return config

