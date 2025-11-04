import pandas as pd
import os

# Criar dados de exemplo para teste
dados_exemplo = {
    'Nome': [
        'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Mendes',
        'Julia Ferreira', 'Lucas Gomes', 'Patricia Lima', 'Roberto Alves', 'Fernanda Ribeiro',
        'Gustavo Souza', 'Amanda Martins', 'Rafael Barbosa', 'Camila Cardoso', 'Diego Fernandes',
        'Natália Correia', 'Felipe Araújo', 'Larissa Dias', 'Bruno Nascimento', 'Renata Cavalcanti'
    ],
    'Interesses': [
        'Esportes, Tecnologia, Música', 'Artes, Tecnologia, Cinema', 'Esportes, Games, Música',
        'Artes, Música, Cinema', 'Tecnologia, Games, Livros', 'Artes, Cinema, Gastronomia',
        'Esportes, Games, Tecnologia', 'Música, Cinema, Gastronomia', 'Esportes, Música, Livros',
        'Artes, Gastronomia, Viagem', 'Games, Tecnologia, Esportes', 'Cinema, Música, Artes',
        'Esportes, Música, Gastronomia', 'Artes, Viagem, Gastronomia', 'Tecnologia, Games, Cinema',
        'Música, Artes, Viagem', 'Esportes, Tecnologia, Games', 'Cinema, Gastronomia, Música',
        'Games, Esportes, Tecnologia', 'Viagem, Artes, Gastronomia'
    ]
}

# Criar DataFrame
df = pd.DataFrame(dados_exemplo)

# Salvar arquivo Excel
caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dados_exemplo.xlsx')
df.to_excel(caminho_arquivo, index=False)

print(f"✅ Arquivo de exemplo criado: {caminho_arquivo}")
print(f"📊 Total de pessoas: {len(df)}")
print("\n📝 Estrutura do arquivo:")
print(df.head())