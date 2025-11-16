# ============================================================================
# IMPORTAÇÕES DE BIBLIOTECAS
# ============================================================================
# Flask: Framework web para criar a API REST
from flask import Flask, request, jsonify
# CORS: Permite que o frontend (React) faça requisições de diferentes origens
from flask_cors import CORS
# Pandas: Biblioteca para processar arquivos CSV e Excel
import pandas as pd
# io: Para trabalhar com dados em memória (BytesIO)
import io
# defaultdict: Dicionário com valores padrão para contagem
from collections import defaultdict
import json
# os: Para acessar variáveis de ambiente (porta do servidor)
import os

# Cria a instância da aplicação Flask
# Habilita CORS (Cross-Origin Resource Sharing) para todas as rotas
app = Flask(__name__)
CORS(app)

# ============================================================================
# ARMAZENAMENTO DE DADOS
# ============================================================================
# Dicionário global que armazena os dados das pessoas e seus interesses
# Estrutura: {nome_pessoa: [lista_de_interesses]}
pessoas_data_storage = {}

# ============================================================================
# ALGORITMO DE MALGRANGE - FUNÇÕES AUXILIARES
# ============================================================================
# O algoritmo de Malgrange identifica componentes fortemente conexas em grafos
# direcionados. Uma componente fortemente conexa é um conjunto de vértices onde
# cada vértice pode alcançar todos os outros vértices do conjunto.

def fecho_transitivo_direto(grafo, v, visitado=None):
    """
    Calcula o fecho transitivo direto de um vértice v.
    
    O fecho transitivo direto contém todos os vértices que podem ser alcançados
    a partir de v seguindo as arestas do grafo na direção correta.
    
    Args:
        grafo: Dicionário representando o grafo {vértice: [vizinhos]}
        v: Vértice inicial
        visitado: Conjunto de vértices já visitados (usado na recursão)
    
    Returns:
        set: Conjunto de todos os vértices alcançáveis a partir de v
    """
    # Inicializa o conjunto de visitados se for a primeira chamada
    if visitado is None:
        visitado = set()
    # Marca o vértice atual como visitado
    visitado.add(v)
    # Se o vértice tem vizinhos no grafo
    if v in grafo:
        # Para cada vizinho do vértice v
        for viz in grafo[v]:
            # Se o vizinho ainda não foi visitado, visita recursivamente
            if viz not in visitado:
                fecho_transitivo_direto(grafo, viz, visitado)
    return visitado

def fecho_transitivo_inverso(grafo, v, visitado=None):
    """
    Calcula o fecho transitivo inverso de um vértice v.
    
    O fecho transitivo inverso contém todos os vértices que podem alcançar v,
    ou seja, vértices de onde é possível chegar em v seguindo as arestas.
    
    Args:
        grafo: Dicionário representando o grafo {vértice: [vizinhos]}
        v: Vértice de destino
        visitado: Conjunto de vértices já visitados (usado na recursão)
    
    Returns:
        set: Conjunto de todos os vértices que podem alcançar v
    """
    # Inicializa o conjunto de visitados se for a primeira chamada
    if visitado is None:
        visitado = set()
    # Marca o vértice atual como visitado
    visitado.add(v)
    # Percorre todos os vértices do grafo
    for u in grafo:
        # Se v é vizinho de u (u pode alcançar v) e u ainda não foi visitado
        if v in grafo[u] and u not in visitado:
            # Visita recursivamente u
            fecho_transitivo_inverso(grafo, u, visitado)
    return visitado

def algoritmo_malgrange(grafo):
    """
    Implementação do algoritmo de Malgrange para encontrar componentes fortemente conexas.
    
    Uma componente fortemente conexa é um conjunto maximal de vértices onde cada
    vértice pode alcançar todos os outros vértices do conjunto através de caminhos
    direcionados no grafo.
    
    O algoritmo funciona da seguinte forma:
    1. Para cada vértice não processado, calcula seu fecho transitivo direto e inverso
    2. A interseção desses dois fechos forma uma componente fortemente conexa
    3. Marca todos os vértices dessa componente como processados
    4. Repete até processar todos os vértices
    
    Args:
        grafo: Dicionário representando o grafo direcionado {vértice: [vizinhos]}
    
    Returns:
        list: Lista de conjuntos, onde cada conjunto é uma componente fortemente conexa
    """
    # Coleta todos os vértices do grafo (chaves do dicionário)
    vertices = set(grafo.keys())
    # Adiciona também os vértices que aparecem apenas como vizinhos (sem chave própria)
    for adjacencias in grafo.values():
        vertices.update(adjacencias)

    # Lista que armazenará as componentes fortemente conexas encontradas
    componentes = []
    # Conjunto de vértices que já foram processados e atribuídos a uma componente
    vertices_processados = set()

    # Enquanto houver vértices não processados
    while vertices - vertices_processados:
        # Seleciona um vértice ainda não processado
        v = next(iter(vertices - vertices_processados))
        # Calcula todos os vértices alcançáveis a partir de v (fecho direto)
        diretos = fecho_transitivo_direto(grafo, v, set())
        # Calcula todos os vértices que podem alcançar v (fecho inverso)
        inversos = fecho_transitivo_inverso(grafo, v, set())
        # A interseção dos fechos direto e inverso forma a componente fortemente conexa
        # Isso garante que todos os vértices podem alcançar uns aos outros
        componente = diretos & inversos
        # Adiciona a componente encontrada à lista
        componentes.append(componente)
        # Marca todos os vértices da componente como processados
        vertices_processados.update(componente)

    return componentes

# ============================================================================
# FUNÇÕES DE PROCESSAMENTO DE DADOS
# ============================================================================

def criar_grafo_por_categorias(pessoas_data):
    """
    Cria um grafo não direcionado onde pessoas são conectadas por interesses compartilhados.
    
    Duas pessoas são conectadas no grafo se elas compartilham pelo menos uma categoria
    de interesse. O grafo é representado como um dicionário de adjacências.
    
    Args:
        pessoas_data: Dicionário {nome_pessoa: [lista_de_interesses]}
    
    Returns:
        dict: Grafo representado como {pessoa: [lista_de_vizinhos]}
    """
    # Inicializa o grafo com todas as pessoas como vértices (sem vizinhos ainda)
    grafo = {pessoa: [] for pessoa in pessoas_data}
    # Converte as chaves do dicionário em lista para iterar
    pessoas_lista = list(pessoas_data.keys())

    # Compara cada par de pessoas para verificar se compartilham interesses
    for i, pessoa1 in enumerate(pessoas_lista):
        # Compara pessoa1 com todas as pessoas que vêm depois dela (evita duplicatas)
        for pessoa2 in pessoas_lista[i+1:]:
            # Converte as listas de categorias em conjuntos para facilitar a comparação
            categorias1 = set(pessoas_data[pessoa1])
            categorias2 = set(pessoas_data[pessoa2])
            # Verifica se há interseção entre os conjuntos (interesses em comum)
            if categorias1 & categorias2:
                # Se compartilham interesses, cria aresta bidirecional no grafo
                # Adiciona pessoa2 como vizinho de pessoa1
                if pessoa2 not in grafo[pessoa1]:
                    grafo[pessoa1].append(pessoa2)
                # Adiciona pessoa1 como vizinho de pessoa2
                if pessoa1 not in grafo[pessoa2]:
                    grafo[pessoa2].append(pessoa1)
    return grafo

def analisar_categorias_comunidade(pessoas_data, comunidade):
    """
    Analisa quais categorias de interesse são mais comuns em uma comunidade.
    
    Para cada categoria, calcula quantas pessoas da comunidade possuem essa categoria
    e qual a porcentagem que isso representa.
    
    Args:
        pessoas_data: Dicionário com dados de todas as pessoas
        comunidade: Conjunto de nomes de pessoas que formam a comunidade
    
    Returns:
        list: Lista de dicionários ordenada por frequência (mais comum primeiro)
              Cada dicionário contém: {'category': str, 'people': int, 'percentage': float}
    """
    # Dicionário para contar quantas pessoas têm cada categoria
    categorias_contador = defaultdict(int)
    # Total de pessoas na comunidade
    total_pessoas = len(comunidade)

    # Para cada pessoa na comunidade
    for pessoa in comunidade:
        # Se a pessoa existe nos dados
        if pessoa in pessoas_data:
            # Conta cada categoria de interesse dessa pessoa
            for categoria in pessoas_data[pessoa]:
                categorias_contador[categoria] += 1

    # Prepara a lista de análise com estatísticas
    categorias_analise = []
    for categoria, count in categorias_contador.items():
        # Calcula a porcentagem de pessoas da comunidade que têm essa categoria
        porcentagem = (count / total_pessoas) * 100
        # Adiciona os dados da categoria à lista
        categorias_analise.append({
            'category': categoria,      # Nome da categoria
            'people': count,           # Quantidade de pessoas com essa categoria
            'percentage': porcentagem  # Porcentagem (0-100)
        })

    # Ordena as categorias por frequência (mais comum primeiro)
    categorias_analise.sort(key=lambda x: x['people'], reverse=True)
    return categorias_analise

def processar_planilha(file_content, file_name):
    """
    Processa um arquivo CSV ou Excel e extrai dados de pessoas e seus interesses.
    
    O arquivo deve conter pelo menos duas colunas:
    - Uma coluna com nomes (pode se chamar "Nome", "Pessoa", "Name", etc)
    - Uma coluna com interesses/categorias (pode se chamar "Interesses", "Categorias", etc)
    
    Os interesses podem estar separados por vírgula ou ponto e vírgula.
    
    Args:
        file_content: Conteúdo binário do arquivo (bytes)
        file_name: Nome do arquivo (usado para determinar o formato)
    
    Returns:
        tuple: (pessoas_data, error)
            - pessoas_data: Dicionário {nome: [lista_interesses]} ou None em caso de erro
            - error: Mensagem de erro (None se sucesso)
    """
    pessoas_data = {}
    
    try:
        # Determina o tipo de arquivo e lê o conteúdo usando pandas
        if file_name.endswith('.csv'):
            # Lê arquivo CSV a partir do conteúdo em memória
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_name.endswith(('.xls', '.xlsx')):
            # Lê arquivo Excel (.xls ou .xlsx) a partir do conteúdo em memória
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            return None, "Formato de arquivo não suportado. Por favor, use CSV ou Excel (.xls, .xlsx)."

        # Identifica a coluna de nomes procurando por palavras-chave
        name_col = None
        for col in df.columns:
            # Procura por colunas que contenham "nome", "pessoa" ou "name" (case-insensitive)
            if 'nome' in col.lower() or 'pessoa' in col.lower() or 'name' in col.lower():
                name_col = col
                break
        if not name_col:
            return None, "Coluna de nome não encontrada. Por favor, certifique-se de ter uma coluna como 'Nome' ou 'Pessoa'."

        # Identifica a coluna de interesses procurando por palavras-chave
        interests_col = None
        for col in df.columns:
            # Procura por colunas que contenham "interesse", "categoria" ou "interest"
            if 'interesse' in col.lower() or 'categoria' in col.lower() or 'interest' in col.lower():
                interests_col = col
                break
        if not interests_col:
            return None, "Coluna de interesses/categorias não encontrada. Por favor, certifique-se de ter uma coluna como 'Interesses' ou 'Categorias'."

        # Processa cada linha do arquivo
        for index, row in df.iterrows():
            # Extrai e limpa o nome da pessoa
            nome = str(row[name_col]).strip()
            # Pula linhas com nome vazio
            if not nome:
                continue

            # Extrai e limpa a string de categorias/interesses
            categorias_str = str(row[interests_col]).strip()
            # Se não houver categorias, cria lista vazia
            if not categorias_str:
                pessoas_data[nome] = []
                continue

            # Divide as categorias por vírgula ou ponto e vírgula
            if ',' in categorias_str:
                # Separa por vírgula e remove espaços
                categorias_list = [cat.strip() for cat in categorias_str.split(',') if cat.strip()]
            elif ';' in categorias_str:
                # Separa por ponto e vírgula e remove espaços
                categorias_list = [cat.strip() for cat in categorias_str.split(';') if cat.strip()]
            else:
                # Se não houver separador, trata como uma única categoria
                categorias_list = [categorias_str]

            # Normaliza e adiciona as categorias (remove espaços extras)
            final_categorias = []
            for cat in categorias_list:
                normalized_cat = cat.strip()
                # Adiciona apenas categorias não vazias
                if normalized_cat:
                    final_categorias.append(normalized_cat)
            # Armazena os dados da pessoa
            pessoas_data[nome] = final_categorias

        # Valida se pelo menos uma pessoa foi encontrada
        if not pessoas_data:
            return None, "Nenhuma pessoa válida foi encontrada no arquivo após o processamento."

        # Retorna os dados processados sem erros
        return pessoas_data, None

    except Exception as e:
        # Em caso de erro, retorna None e a mensagem de erro
        return None, f"Erro ao ler o arquivo: {str(e)}. Verifique se o arquivo está no formato correto e se as colunas estão presentes."

# ============================================================================
# ENDPOINTS DA API REST
# ============================================================================

@app.route('/api/analyze', methods=['POST'])
def analyze_file():
    """
    Endpoint principal: Analisa um arquivo e identifica comunidades usando o algoritmo de Malgrange.
    
    Recebe um arquivo CSV ou Excel via upload, processa os dados, cria um grafo
    baseado em interesses compartilhados e identifica comunidades usando o algoritmo
    de Malgrange.
    
    Request:
        - FormData com campo 'file' contendo o arquivo
    
    Response (sucesso):
        - JSON com comunidades identificadas, estatísticas e dados das pessoas
    
    Response (erro):
        - JSON com mensagem de erro e código HTTP apropriado
    """
    try:
        # Verifica se um arquivo foi enviado na requisição
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400
        
        # Obtém o arquivo enviado
        file = request.files['file']
        # Verifica se um arquivo foi realmente selecionado (não está vazio)
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        # Lê o conteúdo binário do arquivo
        file_content = file.read()
        
        # Processa a planilha e extrai dados de pessoas e interesses
        pessoas_data, error = processar_planilha(file_content, file.filename)
        # Se houver erro no processamento, retorna o erro
        if error:
            return jsonify({'error': error}), 400

        # Armazena os dados das pessoas em memória (para uso em outros endpoints)
        global pessoas_data_storage
        pessoas_data_storage = pessoas_data.copy()

        # Cria o grafo onde pessoas são conectadas por interesses compartilhados
        grafo = criar_grafo_por_categorias(pessoas_data)
        # Aplica o algoritmo de Malgrange para encontrar componentes fortemente conexas
        comunidades = algoritmo_malgrange(grafo)

        # Prepara os dados de resposta para cada comunidade encontrada
        communities_data = []
        for i, comunidade in enumerate(comunidades):
            # Converte o conjunto de pessoas em lista
            members = list(comunidade)
            # Analisa quais categorias são mais comuns nesta comunidade
            shared_categories = analisar_categorias_comunidade(pessoas_data, comunidade)
            
            # Adiciona os dados da comunidade à lista
            communities_data.append({
                'id': i,                      # ID numérico da comunidade
                'members': members,           # Lista de nomes das pessoas na comunidade
                'shared_categories': shared_categories  # Categorias compartilhadas com estatísticas
            })

        # Monta o objeto de resposta completo
        result = {
            'communities': communities_data,           # Lista de todas as comunidades
            'total_people': len(pessoas_data),         # Total de pessoas analisadas
            'total_communities': len(comunidades),     # Total de comunidades encontradas
            'people_data': {pessoa: interesses for pessoa, interesses in pessoas_data.items()}  # Dados completos
        }

        # Retorna a resposta em formato JSON
        return jsonify(result)

    except Exception as e:
        # Em caso de erro não esperado, retorna erro genérico do servidor
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificação de saúde do servidor.
    
    Usado para verificar se a API está funcionando corretamente.
    Útil para monitoramento e testes de conectividade.
    
    Response:
        - JSON: {'status': 'healthy'}
    """
    return jsonify({'status': 'healthy'})

@app.route('/api/update-person-interests', methods=['PUT'])
def update_person_interests():
    """
    Endpoint para atualizar os interesses de uma pessoa e regenerar as comunidades.
    
    Permite modificar os interesses de uma pessoa específica e recalcula automaticamente
    as comunidades usando o algoritmo de Malgrange com os dados atualizados.
    
    Request (JSON):
        {
            'person_name': str,      # Nome da pessoa a ser atualizada
            'interests': [str, ...]  # Nova lista de interesses
        }
    
    Response (sucesso):
        - JSON com as comunidades recalculadas (mesmo formato do /api/analyze)
    
    Response (erro):
        - JSON com mensagem de erro e código HTTP apropriado
    """
    try:
        # Obtém os dados JSON enviados na requisição
        data = request.get_json()
        
        # Valida se os dados foram fornecidos
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Extrai o nome da pessoa e a lista de interesses
        person_name = data.get('person_name')
        interests = data.get('interests', [])
        
        # Valida se o nome da pessoa foi fornecido
        if not person_name:
            return jsonify({'error': 'Nome da pessoa não fornecido'}), 400
        
        # Valida se os interesses são uma lista
        if not isinstance(interests, list):
            return jsonify({'error': 'Interesses devem ser uma lista'}), 400
        
        # Acessa o armazenamento global de dados
        global pessoas_data_storage
        
        # Verifica se há dados carregados (se um arquivo foi analisado anteriormente)
        if not pessoas_data_storage:
            return jsonify({'error': 'Nenhum dado carregado. Por favor, analise um arquivo primeiro.'}), 400
        
        # Atualiza os interesses da pessoa (remove espaços e valores vazios)
        pessoas_data_storage[person_name] = [interest.strip() for interest in interests if interest.strip()]
        
        # Regenera o grafo com os dados atualizados
        grafo = criar_grafo_por_categorias(pessoas_data_storage)
        # Recalcula as comunidades usando o algoritmo de Malgrange
        comunidades = algoritmo_malgrange(grafo)
        
        # Prepara os dados de resposta (mesmo formato do endpoint /api/analyze)
        communities_data = []
        for i, comunidade in enumerate(comunidades):
            members = list(comunidade)
            shared_categories = analisar_categorias_comunidade(pessoas_data_storage, comunidade)
            
            communities_data.append({
                'id': i,
                'members': members,
                'shared_categories': shared_categories
            })
        
        # Monta a resposta completa
        result = {
            'communities': communities_data,
            'total_people': len(pessoas_data_storage),
            'total_communities': len(comunidades),
            'people_data': {pessoa: interesses for pessoa, interesses in pessoas_data_storage.items()}
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500

@app.route('/api/get-person-interests', methods=['GET'])
def get_person_interests():
    """
    Endpoint para obter os interesses de uma pessoa específica.
    
    Retorna apenas os interesses de uma pessoa, sem recalcular as comunidades.
    Útil para consultas rápidas ou para popular formulários de edição.
    
    Request (Query Parameters):
        - person_name: str  # Nome da pessoa
    
    Response (sucesso):
        - JSON: {'person_name': str, 'interests': [str, ...]}
    
    Response (erro):
        - JSON com mensagem de erro e código HTTP apropriado
    """
    try:
        # Obtém o nome da pessoa dos parâmetros da URL (query string)
        person_name = request.args.get('person_name')
        
        # Valida se o nome foi fornecido
        if not person_name:
            return jsonify({'error': 'Nome da pessoa não fornecido'}), 400
        
        # Acessa o armazenamento global de dados
        global pessoas_data_storage
        
        # Verifica se há dados carregados
        if not pessoas_data_storage:
            return jsonify({'error': 'Nenhum dado carregado'}), 400
        
        # Verifica se a pessoa existe nos dados
        if person_name not in pessoas_data_storage:
            return jsonify({'error': 'Pessoa não encontrada'}), 404
        
        # Retorna os dados da pessoa
        return jsonify({
            'person_name': person_name,
            'interests': pessoas_data_storage[person_name]
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro no servidor: {str(e)}'}), 500

# ============================================================================
# INICIALIZAÇÃO DO SERVIDOR
# ============================================================================
# Este bloco só é executado quando o arquivo é rodado diretamente (não quando importado)
if __name__ == '__main__':
    # Obtém a porta do servidor da variável de ambiente PORT, ou usa 8000 como padrão
    port = int(os.environ.get('PORT', 8000))
    # Obtém o modo debug da variável de ambiente FLASK_DEBUG
    # Se FLASK_DEBUG='true', ativa o modo debug (recarregamento automático, mensagens detalhadas)
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    # Inicia o servidor Flask
    # host='0.0.0.0' permite que o servidor aceite conexões de qualquer IP
    # Isso é necessário para acessar o servidor de outras máquinas na rede
    app.run(host='0.0.0.0', port=port, debug=debug)