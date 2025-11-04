# Analisador de Comunidades - Algoritmo de Malgrange

## Descrição
Esta aplicação analisa comunidades baseadas em interesses compartilhados usando o algoritmo de Malgrange. O sistema identifica grupos de pessoas que compartilham interesses semelhantes e fornece insights sobre as categorias mais comuns em cada comunidade.

## 🚀 Tecnologias Utilizadas

### Backend
- Python 3.x
- Flask (API REST)
- Pandas (processamento de dados)
- OpenPyXL (leitura de arquivos Excel)

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Vite
- Lucide React (ícones)

## 📋 Pré-requisitos

1. Python 3.x instalado
2. Node.js 22.15.0+ instalado
3. npm ou pnpm

## 🔧 Instalação e Configuração

### 1. Instalar dependências do Python
```bash
pip install -r requirements.txt
```

### 2. Instalar dependências do Node.js
```bash
npm install
```

## 🎯 Como Usar

### 1. Iniciar o Backend (API)
```bash
python run_api.py
```
O servidor será iniciado em: http://localhost:8000

### 2. Iniciar o Frontend
```bash
npm run dev
```
O frontend será iniciado em: http://localhost:5173

### 3. Usar a Aplicação
1. Acesse http://localhost:5173 no navegador
2. Clique para selecionar um arquivo Excel (.xlsx, .xls) ou CSV
3. Clique em "Analisar Dados"
4. Visualize as comunidades identificadas e seus interesses compartilhados

## 📊 Formato do Arquivo de Entrada

O arquivo deve conter as seguintes colunas:
- **Nome** (ou "Pessoa", "Name"): Nome da pessoa
- **Interesses** (ou "Categorias", "Interests"): Lista de interesses separados por vírgula ou ponto e vírgula

### Exemplo:
```csv
Nome,Interesses
João Silva,Esportes,Tecnologia,Música
Maria Santos,Artes,Tecnologia,Cinema
```

## 📈 Funcionalidades

- 📤 Upload de arquivos Excel/CSV
- 🔍 Análise automática de comunidades
- 📊 Visualização de estatísticas gerais
- 👥 Lista de membros por comunidade
- 🏷️ Interesses compartilhados com percentuais
- 📱 Interface responsiva e moderna

## 🛠️ Estrutura do Projeto

```
c:\Projetos\AlgoritmoMalgrange_Grafos/
├── api/                    # Backend Flask
│   └── app.py             # API principal
├── src/                   # Frontend React
│   ├── App.tsx           # Componente principal
│   └── main.tsx          # Entry point
├── backend/               # Código Python original
│   └── main.py           # Implementação original do algoritmo
├── dados_exemplo.xlsx     # Arquivo de exemplo
├── run_api.py            # Script para iniciar o backend
├── criar_exemplo.py      # Script para criar dados de exemplo
└── requirements.txt      # Dependências Python
```

## 🔍 API Endpoints

- `POST /api/analyze` - Analisa arquivo e retorna comunidades
- `GET /api/health` - Verifica status do servidor

## 💡 Exemplos de Uso

### Criar arquivo de exemplo
```bash
python criar_exemplo.py
```

### Testar API manualmente
```bash
curl -X GET http://localhost:8000/api/health
```

## 🚨 Solução de Problemas

### Backend não inicia
- Verifique se Python está instalado: `python --version`
- Instale as dependências: `pip install -r requirements.txt`

### Frontend não conecta ao backend
- Verifique se o backend está rodando na porta 8000
- Verifique se não há conflitos de porta
- Verifique o console do navegador para erros de CORS

### Arquivo não é processado
- Verifique se o arquivo tem as colunas corretas (Nome e Interesses)
- Certifique-se de que o arquivo não está corrompido
- Tente usar o arquivo de exemplo gerado

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está disponível para uso educacional e de pesquisa.

## 📞 Suporte

Em caso de dúvidas ou problemas, verifique os logs do console do navegador e do terminal onde os servidores estão rodando.
