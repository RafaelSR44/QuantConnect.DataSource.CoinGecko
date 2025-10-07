#!/usr/bin/env python3
"""
Script launcher para executar o processador de dados CoinGecko
Execute este arquivo da raiz do projeto para evitar problemas de importação
"""

import sys
import os

# Adicionar o diretório atual ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Executa o processador de dados."""
    
    print("🚀 Launcher do CoinGecko Data Processor")
    print("=" * 50)
    
    try:
        # Importar e executar o processador
        from DataProcessing.process import main as process_main
        process_main()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("\n💡 Soluções:")
        print("1. Certifique-se de estar no diretório raiz do projeto")
        print("2. Execute: pip install -r requirements.txt")
        print("3. Verifique se todos os arquivos estão presentes")
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")

if __name__ == "__main__":
    main()
