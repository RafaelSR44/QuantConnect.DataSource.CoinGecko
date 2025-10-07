from QuantConnect.Data import SubscriptionDataSource, BaseData
from QuantConnect.Python import PythonData
from datetime import datetime, timedelta
import os

class CoinGeckoData(PythonData):
    """Classe de dados customizada para CoinGecko, herda de PythonData."""

    def GetSource(self, config, date, isLiveMode):
        """Define a fonte de dados (arquivo CSV) para uma data específica."""
        source = os.path.join("data", "crypto", config.Symbol.Value.lower(), f"{config.Symbol.Value.lower()}.csv")
        return SubscriptionDataSource(source, 0) # 0 for local file

    def Reader(self, config, line, date, isLiveMode):
        """Lê uma linha do arquivo de dados e a transforma em um objeto CoinGeckoData."""
        if not (line.strip() and line[0].isdigit()):
            return None

        # Cria uma nova instância da classe CoinGeckoData
        data = CoinGeckoData()
        data.Symbol = config.Symbol

        try:
            # Formato do CSV: YYYYMMDD HH:MM,open,high,low,close,volume
            parts = line.split(',')
            data.Time = datetime.strptime(parts[0], "%Y%m%d %H:%M")
            data.EndTime = data.Time + timedelta(days=1)
            data.Value = float(parts[4])  # Preço de fechamento como valor principal

            data["Open"] = float(parts[1])
            data["High"] = float(parts[2])
            data["Low"] = float(parts[3])
            data["Close"] = float(parts[4])
            data["Volume"] = float(parts[5])

        except Exception as e:
            print(f"Erro ao processar linha: {line} - {e}")
            return None

        return data

