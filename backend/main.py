# ANÁLISE DE COMUNIDADES POR INTERESSES COM ALGORITMO DE MALGRANGE

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from collections import defaultdict
import pandas as pd
import io

# ALGORITMO DE MALGRANGE

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


# CATEGORIAS PREDEFINIDAS (sem emojis, apenas texto)
CATEGORIAS_DISPONIVEIS = {
    'Esportes': ('', ''),
    'Tecnologia': ('', ''),
    'Artes': ('', ''),
    'Entretenimento': ('', ''),
    'Cultura': ('', ''),
    'Estilo de Vida': ('', ''),
    'Saúde': ('', ''),
    'Games': ('', ''),
    'Gastronomia': ('', ''),
    'Música': ('', ''),
    "Cinema": ('', ''),
    "Livros": ('',''),
    "Filmes": ('',''),
    "Séries": ('',''),
}

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
        emoji, cor = CATEGORIAS_DISPONIVEIS.get(categoria, ('', ''))
        categorias_analise.append({
            'categoria': categoria,
            'pessoas': count,
            'porcentagem': porcentagem,
            'emoji': emoji,
            'cor': cor
        })

    categorias_analise.sort(key=lambda x: x['pessoas'], reverse=True)
    return categorias_analise


def processar_planilha(uploaded_file_content, file_name, pessoas_data, CATEGORIAS_DISPONIVEIS):
    """
    Processa um arquivo CSV ou Excel para popular o dicionário pessoas_data
    e atualizar CATEGORIAS_DISPONIVEIS.
    """
    pessoas_data.clear() # Clear existing data
    df = None
    try:
        # Determine file type and read content
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(uploaded_file_content))
        elif file_name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(uploaded_file_content))
        else:
            return False, "Formato de arquivo não suportado. Por favor, use CSV ou Excel (.xls, .xlsx)."

        # Identify Name Column
        name_col = None
        for col in df.columns:
            if 'nome' in col.lower() or 'pessoa' in col.lower():
                name_col = col
                break
        if not name_col:
            return False, "Coluna de nome não encontrada. Por favor, certifique-se de ter uma coluna como 'Nome' ou 'Pessoa'."

        # Identify Interests Column
        interests_col = None
        for col in df.columns:
            if 'interesse' in col.lower() or 'categoria' in col.lower():
                interests_col = col
                break
        if not interests_col:
            return False, "Coluna de interesses/categorias não encontrada. Por favor, certifique-se de ter uma coluna como 'Interesses' ou 'Categorias'."

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
                    if normalized_cat not in CATEGORIAS_DISPONIVEIS:
                        CATEGORIAS_DISPONIVEIS[normalized_cat] = ('', '') # Add new category dynamically
            pessoas_data[nome] = final_categorias

        if not pessoas_data:
            return False, "Nenhuma pessoa válida foi encontrada no arquivo após o processamento."

        return True, "Dados carregados com sucesso!"

    except Exception as e:
        return False, f"Erro ao ler o arquivo: {str(e)}. Verifique se o arquivo está no formato correto e se as colunas estão presentes."


# INTERFACE GRÁFICA

def criar_interface():
    pessoas_data = {}
    # This dictionary will hold the original CATEGORIAS_DISPONIVEIS to revert to on clear
    original_categorias_disponiveis = dict(CATEGORIAS_DISPONIVEIS)

    display(HTML('''
    <style>
        .widget-label { font-weight: bold; font-size: 14px; }
        .widget-text input { font-size: 13px; }
    </style>
    '''))

    # Seção de adicionar pessoa
    secao_adicionar = widgets.HTML(
        value='<h3 style="color: #667eea; margin-top: 10px;">Carregar Pessoas de Arquivo</h3>'
    )

    # NOVO: Widget FileUpload
    file_upload = widgets.FileUpload(
        accept='.csv, .xls, .xlsx',
        multiple=False,  # Allow only one file to be uploaded
        description='Selecionar Arquivo',
        layout=widgets.Layout(width='450px')
    )

    carregar_planilha_button = widgets.Button(
        description='Carregar Planilha',
        button_style='success',
        layout=widgets.Layout(width='200px', height='40px')
    )

    lista_pessoas = widgets.Output(
        layout=widgets.Layout(
            width='700px',
            max_height='250px',
            border='1px solid #ddd',
            padding='15px',
            overflow_y='auto',
            border_radius='8px'
        )
    )

    def on_carregar_planilha_clicked(b):
        with lista_pessoas:
            clear_output()
            if not file_upload.value:
                print("Erro: Por favor, selecione um arquivo para carregar.")
                return

            uploaded_file = list(file_upload.value.values())[0]
            file_name = uploaded_file['metadata']['name']
            file_content = uploaded_file['content']

            success, message = processar_planilha(file_content, file_name, pessoas_data, CATEGORIAS_DISPONIVEIS)

            if success:
                print(message)
                print("\nPESSOAS CARREGADAS:")
                print("="*70)
                for p, cats in pessoas_data.items():
                    print(f"{p}")
                    print(f" Categorias: {', '.join(cats)}")
                    print()
                print(f"Novas categorias disponíveis: {', '.join([cat for cat in CATEGORIAS_DISPONIVEIS if cat not in original_categorias_disponiveis])}")
            else:
                print(f"Erro ao carregar planilha: {message}")

            # Clear the file upload selection after processing to allow re-uploading the same file
            # or a different one without issues.
            file_upload.value.clear()

    carregar_planilha_button.on_click(on_carregar_planilha_clicked)

    secao_analisar = widgets.HTML(
        value='<h3 style="color: #667eea; margin-top: 30px;">Aplicar Algoritmo de Malgrange</h3>'
    )

    botao_analisar = widgets.Button(
        description='Identificar Comunidades',
        button_style='primary',
        layout=widgets.Layout(width='240px', height='50px')
    )

    botao_limpar = widgets.Button(
        description='Limpar Tudo',
        button_style='danger',
        layout=widgets.Layout(width='150px', height='50px')
    )

    resultado = widgets.Output(
        layout=widgets.Layout(
            width='750px',
            border='2px solid #667eea',
            padding='20px',
            margin='15px 0',
            border_radius='10px'
        )
    )

    def analisar_comunidades(b):
        with resultado:
            clear_output()

            if len(pessoas_data) < 2:
                print("Erro: Adicione pelo menos 2 pessoas para análise!")
                return

            try:
                print("="*75)
                print("ALGORITMO DE MALGRANGE - ANÁLISE DE COMUNIDADES".center(75))
                print("="*75)
                print(f"Total de pessoas: {len(pessoas_data)}")
                print()

                grafo = criar_grafo_por_categorias(pessoas_data)
                print("Grafo criado com conexões entre pessoas com categorias em comum.")
                print()

                componentes = algoritmo_malgrange(grafo)
                print(f"Total de Componentes: {len(componentes)}")
                print()

                for i, comunidade in enumerate(componentes, 1):
                    membros = sorted(list(comunidade))
                    tamanho = len(comunidade)

                    if tamanho > 1:
                        print(f"\nCOMPONENTE {i} - COMUNIDADE")
                        print(f"Membros ({tamanho}): {', '.join(membros)}")

                        categorias = analisar_categorias_comunidade(pessoas_data, comunidade)
                        if categorias:
                            print("Categorias mais compartilhadas:")
                            for cat in categorias:
                                print(f" - {cat['categoria']}: {cat['pessoas']}/{tamanho} pessoas")
                    else:
                        print(f"\nCOMPONENTE {i} - PESSOA ISOLADA: {membros[0]}")

            except Exception as e:
                print(f"Erro ao processar: {str(e)}")

    botao_analisar.on_click(analisar_comunidades)

    def limpar_tudo(b):
        pessoas_data.clear()
        # Restore CATEGORIAS_DISPONIVEIS to its original state
        CATEGORIAS_DISPONIVEIS.clear()
        CATEGORIAS_DISPONIVEIS.update(original_categorias_disponiveis)
        file_upload.value.clear() # Clear file upload selection
        with lista_pessoas:
            clear_output()
            print("Nenhuma pessoa cadastrada ainda.")
        with resultado:
            clear_output()

    botao_limpar.on_click(limpar_tudo)

    interface = widgets.VBox([
        secao_adicionar,
        file_upload,
        carregar_planilha_button,
        widgets.HTML("<p style='font-weight: bold; margin-top: 15px;'>Pessoas Carregadas:</p>"),
        lista_pessoas,
        secao_analisar,
        botao_analisar,
        botao_limpar,
        resultado
    ])

    display(interface)

    with lista_pessoas:
        print("Nenhuma pessoa cadastrada ainda.")


# EXECUTAR
print("Sistema de Análise de Comunidades com Algoritmo de Malgrange")
print("="*70)
print()
print("CATEGORIAS DISPONÍVEIS:")
for cat in CATEGORIAS_DISPONIVEIS.keys():
    print(f"  - {cat}")
print()
print("ALGORITMO:")
print("  Malgrange - Identifica componentes fortemente conexas em grafos dirigidos")
print()
criar_interface()