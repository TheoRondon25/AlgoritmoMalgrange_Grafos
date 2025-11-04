from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
from collections import defaultdict
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Algoritmo de Malgrange (copiado do main.py original)
def fecho_transitivo_direto(grafo, v, visitado=None):
    """Calcula todas as pessoas alcançáveis a partir de v"""
    if visitado is None:
        visitado = set()
    visitado.add(v)
    if v in grafo:
        for viz in grafo[v]:
            if viz not in visitado:
                fecho_transitivo_direto(grafo, viz, visitado)
    return visitado

def fecho_transitivo_inverso(grafo, v, visitado=None):
    """Calcula todas as pessoas que podem alcançar v"""
    if visitado is None:
        visitado = set()
    visitado.add(v)
    for u in grafo:
        if v in grafo[u] and u not in visitado:
            fecho_transitivo_inverso(grafo, u, visitado)
    return visitado

def algoritmo_malgrange(grafo):
    """
    Encontra componentes fortemente conexas (comunidades).
    Uma componente fortemente conexa é um conjunto maximal de vértices
    onde cada vértice pode alcançar todos os outros.
    """
    vertices = set(grafo.keys())
    for adjacencias in grafo.values():
        vertices.update(adjacencias)

    componentes = []
    vertices_processados = set()

    while vertices - vertices_processados:
        v = next(iter(vertices - vertices_processados))
        diretos = fecho_transitivo_direto(grafo, v, set())
        inversos = fecho_transitivo_inverso(grafo, v, set())
        componente = diretos & inversos
        componentes.append(componente)
        vertices_processados.update(componente)

    return componentes

def criar_grafo_por_categorias(pessoas_data):
    """Cria grafo direcionado onde pessoas se conectam por categorias compartilhadas."""
    grafo = {pessoa: [] for pessoa in pessoas_data}
    pessoas_lista = list(pessoas_data.keys())

    for i, pessoa1 in enumerate(pessoas_lista):
        for pessoa2 in pessoas_lista[i+1:]:
            categorias1 = set(pessoas_data[pessoa1])
            categorias2 = set(pessoas_data[pessoa2])
            if categorias1 & categorias2:
                if pessoa2 not in grafo[pessoa1]:
                    grafo[pessoa1].append(pessoa2)
                if pessoa1 not in grafo[pessoa2]:
                    grafo[pessoa2].append(pessoa1)
    return grafo

def analisar_categorias_comunidade(pessoas_data, comunidade):
    """Analisa as categorias compartilhadas em uma comunidade"""
    categorias_contador = defaultdict(int)
    total_pessoas = len(comunidade)

    for pessoa in comunidade:
        if pessoa in pessoas_data:
            for categoria in pessoas_data[pessoa]:
                categorias_contador[categoria] += 1

    categorias_analise = []
    for categoria, count in categorias_contador.items():
        porcentagem = (count / total_pessoas) * 100
        categorias_analise.append({
            'category': categoria,
            'people': count,
            'percentage': porcentagem
        })

    categorias_analise.sort(key=lambda x: x['people'], reverse=True)
    return categorias_analise

def processar_planilha(file_content, file_name):
    """
    Processa um arquivo CSV ou Excel para popular o dicionário pessoas_data
    """
    pessoas_data = {}
    
    try:
        # Determine file type and read content
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            return None, "Formato de arquivo não suportado. Por favor, use CSV ou Excel (.xls, .xlsx)."

        # Identify Name Column
        name_col = None
        for col in df.columns:
            if 'nome' in col.lower() or 'pessoa' in col.lower() or 'name' in col.lower():
                name_col = col
                break
        if not name_col:
            return None, "Coluna de nome não encontrada. Por favor, certifique-se de ter uma coluna como 'Nome' ou 'Pessoa'."

        # Identify Interests Column
        interests_col = None
        for col in df.columns:
            if 'interesse' in col.lower() or 'categoria' in col.lower() or 'interest' in col.lower():
                interests_col = col
                break
        if not interests_col:
            return None, "Coluna de interesses/categorias não encontrada. Por favor, certifique-se de ter uma coluna como 'Interesses' ou 'Categorias'."

        # Process each row
        for index, row in df.iterrows():
            nome = str(row[name_col]).strip()
            if not nome:
                continue # Skip if name is empty

            categorias_str = str(row[interests_col]).strip()
            if not categorias_str:
                pessoas_data[nome] = []
                continue

            # Split categories by comma or semicolon
            if ',' in categorias_str:
                categorias_list = [cat.strip() for cat in categorias_str.split(',') if cat.strip()]
            elif ';' in categorias_str:
                categorias_list = [cat.strip() for cat in categorias_str.split(';') if cat.strip()]
            else:
                categorias_list = [categorias_str]

            # Normalize and add categories
            final_categorias = []
            for cat in categorias_list:
                normalized_cat = cat.strip()
                if normalized_cat:
                    final_categorias.append(normalized_cat)
            pessoas_data[nome] = final_categorias

        if not pessoas_data:
            return None, "Nenhuma pessoa válida foi encontrada no arquivo após o processamento."

        return pessoas_data, None

    except Exception as e:
        return None, f"Erro ao ler o arquivo: {str(e)}. Verifique se o arquivo está no formato correto e se as colunas estão presentes."

@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        # Read file content
        file_content = file.read()
        
        # Process the spreadsheet
        pessoas_data, error = processar_planilha(file_content, file.filename)
        if error:
            return jsonify({'error': error}), 400

        # Create graph and find communities
        grafo = criar_grafo_por_categorias(pessoas_data)
        comunidades = algoritmo_malgrange(grafo)

        # Prepare response
        communities_data = []
        for i, comunidade in enumerate(comunidades):
            members = list(comunidade)
            shared_categories = analisar_categorias_comunidade(pessoas_data, comunidade)
            
            communities_data.append({
                'id': i,
                'members': members,
                'shared_categories': shared_categories
            })

        result = {
            'communities': communities_data,
            'total_people': len(pessoas_data),
            'total_communities': len(comunidades)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)