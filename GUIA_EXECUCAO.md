# 🚀 Guia de Execução - Analisador de Comunidades (Algoritmo de Malgrange)

Este guia fornece instruções passo a passo para executar o projeto completo, incluindo backend e frontend.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. **Python 3.x** (recomendado: Python 3.8 ou superior)

   - Verificar instalação: `python --version` ou `python3 --version`
   - Download: [python.org](https://www.python.org/downloads/)

2. **Node.js** (recomendado: versão 18 ou superior)

   - Verificar instalação: `node --version`
   - Download: [nodejs.org](https://nodejs.org/)

3. **npm** (geralmente vem com Node.js)
   - Verificar instalação: `npm --version`

---

## 🔧 Passo 1: Instalação das Dependências

### 1.1 Instalar Dependências do Backend (Python)

Abra um terminal na raiz do projeto e execute:

```bash
pip install -r requirements.txt
```

**Nota para Windows:**

- Se `pip` não funcionar, tente `pip3` ou `python -m pip`
- Se estiver usando ambiente virtual, ative-o primeiro:

  ```bash
  # Windows
  venv\Scripts\activate

  # Linux/Mac
  source venv/bin/activate
  ```

**Dependências que serão instaladas:**

- Flask (framework web)
- Flask-CORS (permissão de requisições cross-origin)
- Pandas (processamento de dados)
- OpenPyXL (leitura de arquivos Excel)

### 1.2 Instalar Dependências do Frontend (Node.js)

Abra um terminal na raiz do projeto e execute:

```bash
npm install
```

Este comando irá instalar todas as dependências listadas no `package.json`, incluindo:

- React
- TypeScript
- Vite
- Tailwind CSS
- E outras dependências necessárias

**Tempo estimado:** 2-5 minutos (dependendo da conexão)

---

## 🎯 Passo 2: Executar o Backend (API Flask)

### 2.1 Iniciar o Servidor Backend

Abra um terminal na raiz do projeto e execute:

```bash
python run_api.py
```

**Alternativas:**

- Se `python` não funcionar, tente: `python3 run_api.py`
- No Windows, pode ser necessário: `py run_api.py`

### 2.2 Verificar se o Backend Está Rodando

Você deve ver uma mensagem similar a:

```
🚀 Iniciando servidor da API...
📡 Servidor rodando em: http://localhost:8000
📊 Endpoint de análise: POST http://localhost:8000/api/analyze
🏥 Health check: GET http://localhost:8000/api/health

Pressione Ctrl+C para parar o servidor
```

### 2.3 Testar o Backend (Opcional)

Abra outro terminal e teste se a API está respondendo:

```bash
# Windows (PowerShell)
curl http://localhost:8000/api/health

# Ou use um navegador e acesse:
# http://localhost:8000/api/health
```

Você deve receber: `{"status":"healthy"}`

**⚠️ IMPORTANTE:** Mantenha este terminal aberto enquanto estiver usando a aplicação. O backend precisa estar rodando para o frontend funcionar.

---

## 🎨 Passo 3: Executar o Frontend (React)

### 3.1 Iniciar o Servidor de Desenvolvimento

Abra um **novo terminal** (mantenha o terminal do backend aberto) na raiz do projeto e execute:

```bash
npm run dev
```

### 3.2 Verificar se o Frontend Está Rodando

Você deve ver uma mensagem similar a:

```
  VITE v6.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 3.3 Acessar a Aplicação

Abra seu navegador e acesse:

```
http://localhost:5173
```

**⚠️ IMPORTANTE:** Mantenha este terminal aberto também. O frontend precisa estar rodando para acessar a interface.

---

## 📱 Passo 4: Usar a Aplicação

### 4.1 Preparar um Arquivo de Dados

O arquivo deve ser **CSV** ou **Excel** (.xlsx, .xls) com as seguintes colunas:

- **Coluna de Nomes:** Pode se chamar "Nome", "Pessoa", "Name", etc.
- **Coluna de Interesses:** Pode se chamar "Interesses", "Categorias", "Interests", etc.

**Exemplo de formato CSV:**

```csv
Nome,Interesses
João Silva,Esportes,Tecnologia,Música
Maria Santos,Artes,Tecnologia,Cinema
Pedro Costa,Esportes,Games
Ana Lima,Tecnologia,Música,Cinema
```

**Exemplo de formato Excel:**
| Nome | Interesses |
|------|------------|
| João Silva | Esportes,Tecnologia,Música |
| Maria Santos | Artes,Tecnologia,Cinema |

**Nota:** Os interesses podem ser separados por vírgula (`,`) ou ponto e vírgula (`;`)

### 4.2 Analisar os Dados

1. Na interface web, clique em **"Selecionar Arquivo"** ou **"Escolher Arquivo"**
2. Selecione seu arquivo CSV ou Excel
3. Clique em **"Analisar Dados"** ou botão similar
4. Aguarde o processamento (pode levar alguns segundos dependendo do tamanho do arquivo)

### 4.3 Visualizar os Resultados

Após a análise, você verá:

- **Total de pessoas** analisadas
- **Total de comunidades** identificadas
- **Lista de comunidades** com:
  - Membros de cada comunidade
  - Categorias compartilhadas com percentuais
  - Estatísticas de cada categoria

### 4.4 Editar Interesses (Opcional)

Alguns recursos permitem editar os interesses de uma pessoa:

1. Clique na pessoa que deseja editar
2. Modifique os interesses
3. Salve as alterações
4. As comunidades serão recalculadas automaticamente

---

## 🛑 Como Parar os Servidores

### Parar o Frontend

No terminal do frontend, pressione: `Ctrl + C`

### Parar o Backend

No terminal do backend, pressione: `Ctrl + C`

**Ordem recomendada:** Pare primeiro o frontend, depois o backend.

---

## 🚨 Solução de Problemas

### Problema: "python não é reconhecido como comando"

**Solução:**

- Use `python3` em vez de `python`
- No Windows, tente `py run_api.py`
- Verifique se Python está instalado: `python --version`

### Problema: "pip não é reconhecido como comando"

**Solução:**

- Use `pip3` em vez de `pip`
- No Windows, tente `python -m pip install -r requirements.txt`
- Verifique se pip está instalado: `pip --version`

### Problema: "npm não é reconhecido como comando"

**Solução:**

- Verifique se Node.js está instalado: `node --version`
- Reinstale Node.js se necessário: [nodejs.org](https://nodejs.org/)

### Problema: Backend não inicia (porta 8000 já em uso)

**Solução:**

1. Feche outros programas usando a porta 8000
2. Ou altere a porta no arquivo `run_api.py`:
   ```python
   port = int(os.environ.get('PORT', 8001))  # Mude para 8001 ou outra porta
   ```
3. Atualize a URL no frontend se necessário

### Problema: Frontend não conecta ao backend

**Solução:**

1. Verifique se o backend está rodando: `http://localhost:8000/api/health`
2. Verifique se ambos estão na mesma máquina
3. Verifique o console do navegador (F12) para erros
4. Certifique-se de que o CORS está habilitado no backend

### Problema: "Erro ao ler o arquivo"

**Solução:**

1. Verifique se o arquivo tem as colunas corretas (Nome e Interesses)
2. Verifique se o arquivo não está corrompido
3. Tente usar o arquivo de exemplo: `dados_exemplo.xlsx`
4. Verifique se os interesses estão separados por vírgula ou ponto e vírgula

### Problema: Dependências não instalam

**Solução:**

1. Atualize o pip: `python -m pip install --upgrade pip`
2. Atualize o npm: `npm install -g npm@latest`
3. Tente instalar as dependências novamente
4. No Windows, execute o terminal como Administrador

### Problema: Erro de permissão ao instalar dependências

**Solução:**

- Use ambiente virtual (recomendado):

  ```bash
  # Criar ambiente virtual
  python -m venv venv

  # Ativar (Windows)
  venv\Scripts\activate

  # Ativar (Linux/Mac)
  source venv/bin/activate

  # Depois instale as dependências
  pip install -r requirements.txt
  ```

---

## 📊 Estrutura de Terminais

Para executar o projeto completo, você precisará de **2 terminais abertos simultaneamente**:

### Terminal 1 - Backend

```bash
# Navegue até a pasta do projeto
cd caminho/para/o/projeto

# Execute o backend
python run_api.py
```

### Terminal 2 - Frontend

```bash
# Navegue até a pasta do projeto (mesma pasta)
cd caminho/para/o/projeto

# Execute o frontend
npm run dev
```

**Dica:** Use abas diferentes no terminal ou janelas separadas para facilitar.

---

## ✅ Checklist de Execução

Use este checklist para garantir que tudo está configurado corretamente:

- [ ] Python 3.x instalado e funcionando
- [ ] Node.js instalado e funcionando
- [ ] Dependências do Python instaladas (`pip install -r requirements.txt`)
- [ ] Dependências do Node.js instaladas (`npm install`)
- [ ] Backend rodando na porta 8000 (`python run_api.py`)
- [ ] Frontend rodando na porta 5173 (`npm run dev`)
- [ ] Navegador aberto em `http://localhost:5173`
- [ ] Arquivo de dados preparado (CSV ou Excel)

---

## 📝 Resumo dos Comandos

### Instalação (executar uma vez)

```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Execução (sempre que for usar o projeto)

```bash
# Terminal 1 - Backend
python run_api.py

# Terminal 2 - Frontend
npm run dev
```

### URLs Importantes

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Health Check:** http://localhost:8000/api/health

---

## 🎓 Informações Adicionais

### Sobre o Algoritmo de Malgrange

O algoritmo de Malgrange identifica **componentes fortemente conexas** em grafos direcionados. No contexto desta aplicação:

- **Vértices:** Pessoas
- **Arestas:** Conexões baseadas em interesses compartilhados
- **Componentes Fortemente Conexas:** Comunidades de pessoas que compartilham interesses

### Tecnologias Utilizadas

**Backend:**

- Flask: Framework web Python
- Pandas: Processamento de dados
- OpenPyXL: Leitura de arquivos Excel

**Frontend:**

- React: Biblioteca JavaScript para interfaces
- TypeScript: Superset do JavaScript com tipagem
- Vite: Build tool e servidor de desenvolvimento
- Tailwind CSS: Framework CSS utilitário

---

## 📞 Suporte

Se encontrar problemas não listados aqui:

1. Verifique os logs no terminal do backend
2. Verifique o console do navegador (F12 → Console)
3. Verifique se todas as dependências estão instaladas
4. Tente reiniciar os servidores (pare com Ctrl+C e inicie novamente)

---

**Boa sorte com sua apresentação! 🎉**
