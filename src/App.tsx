import React, { useState } from 'react';
import { Upload, FileText, Users, BarChart3 } from 'lucide-react';

interface Community {
  id: number;
  members: string[];
  shared_categories: {
    category: string;
    people: number;
    percentage: number;
  }[];
}

interface AnalysisResult {
  communities: Community[];
  total_people: number;
  total_communities: number;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string>('');

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setError('');
    }
  };

  const analyzeData = async () => {
    if (!file) {
      setError('Por favor, selecione um arquivo primeiro.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Erro ao analisar os dados');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Erro ao conectar com o servidor. Verifique se o backend está rodando.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearResults = () => {
    setResult(null);
    setFile(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Analisador de Comunidades - Algoritmo de Malgrange
          </h1>
          <p className="text-lg text-gray-600">
            Importe uma planilha Excel para descobrir comunidades baseadas em interesses compartilhados
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <FileText className="inline w-4 h-4 mr-2" />
              Selecionar arquivo Excel (.xlsx, .xls)
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
              <input
                type="file"
                accept=".xlsx,.xls,.csv"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-600">
                  {file ? file.name : 'Clique para selecionar um arquivo'}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Formatos aceitos: Excel (.xlsx, .xls) ou CSV
                </p>
              </label>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={analyzeData}
              disabled={!file || loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Analisando...' : 'Analisar Dados'}
            </button>
            {result && (
              <button
                onClick={clearResults}
                className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
              >
                Limpar Resultados
              </button>
            )}
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}
        </div>

        {result && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-center mb-4">
                <BarChart3 className="w-6 h-6 text-blue-600 mr-2" />
                <h2 className="text-2xl font-bold text-gray-900">Resumo da Análise</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-blue-600 font-medium">Total de Pessoas</p>
                  <p className="text-2xl font-bold text-blue-900">{result.total_people}</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <p className="text-sm text-green-600 font-medium">Comunidades Encontradas</p>
                  <p className="text-2xl font-bold text-green-900">{result.total_communities}</p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <p className="text-sm text-purple-600 font-medium">Média por Comunidade</p>
                  <p className="text-2xl font-bold text-purple-900">
                    {Math.round(result.total_people / result.total_communities)}
                  </p>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                <Users className="w-6 h-6 text-blue-600 mr-2" />
                Comunidades Identificadas
              </h2>
              {result.communities.map((community) => (
                <div key={community.id} className="bg-white rounded-lg shadow-lg p-6">
                  <div className="mb-4">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      Comunidade {community.id + 1}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {community.members.length} membros • {community.shared_categories.length} interesses compartilhados
                    </p>
                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Membros</h4>
                      <div className="bg-gray-50 rounded-lg p-3 max-h-32 overflow-y-auto">
                        {community.members.map((member, index) => (
                          <div key={index} className="text-sm text-gray-700 py-1">
                            • {member}
                          </div>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Interesses Compartilhados</h4>
                      <div className="space-y-2">
                        {community.shared_categories.map((category, index) => (
                          <div key={index} className="flex justify-between items-center bg-gray-50 rounded-lg p-2">
                            <span className="text-sm font-medium text-gray-900">
                              {category.category}
                            </span>
                            <div className="text-right">
                              <div className="text-sm text-gray-600">
                                {category.people} pessoas
                              </div>
                              <div className="text-xs text-gray-500">
                                {category.percentage.toFixed(1)}%
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
