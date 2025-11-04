#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    print("🚀 Iniciando servidor da API...")
    print(f"📡 Servidor rodando em: http://localhost:{port}")
    print(f"📊 Endpoint de análise: POST http://localhost:{port}/api/analyze")
    print(f"🏥 Health check: GET http://localhost:{port}/api/health")
    print("\nPressione Ctrl+C para parar o servidor")
    app.run(host='0.0.0.0', port=port, debug=debug)