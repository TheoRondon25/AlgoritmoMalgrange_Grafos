#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.app import app

if __name__ == '__main__':
    print("🚀 Iniciando servidor da API...")
    print("📡 Servidor rodando em: http://localhost:8000")
    print("📊 Endpoint de análise: POST http://localhost:8000/api/analyze")
    print("🏥 Health check: GET http://localhost:8000/api/health")
    print("\nPressione Ctrl+C para parar o servidor")
    
    app.run(host='0.0.0.0', port=8000, debug=True)