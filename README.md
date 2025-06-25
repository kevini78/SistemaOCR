# Analisador de Portarias de Naturalização

Este é um sistema para análise automática de portarias de naturalização brasileira, incluindo **busca automática no DOU** baseada no [Ro-DOU](https://github.com/gestaogovbr/Ro-dou).

## 🚀 Novidades

### ✨ Busca Automática DOU
- **Busca automática** de portarias de naturalização no Diário Oficial da União
- **Extração automática** de dados das pessoas naturalizadas
- **Geração de planilhas** Excel com todos os dados organizados
- **Interface web** para busca por período (ex: 2018-2025)
- **Baseado no Ro-DOU** da Secretaria de Gestão e Inovação

## Requisitos

- Python 3.7 ou superior
- ChromeDriver (para Selenium) - deve estar no PATH do sistema
- Google Chrome instalado
- Conexão com internet (para busca no DOU)

## Instalação

1. Clone este repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd SistemaAnalisador
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo:
```bash
cd analisadorportarias
python app.py
```

## Uso

### Interface Web
1. Acesse o aplicativo através do navegador em: http://localhost:5000
2. Use a interface web para:
   - **Configurar** histórico de naturalizações
   - **Analisar** portarias através de URL ou texto
   - **Buscar automaticamente** no DOU por período

### Busca Automática DOU
1. Acesse a página "Busca Automática"
2. Defina o período desejado (ex: 2018-01-01 a 2025-12-31)
3. (Opcional) Adicione palavras-chave específicas
4. Clique em "Iniciar Busca Automática"
5. Aguarde o processamento e baixe a planilha gerada

### Linha de Comando
```python
from busca_automatica_dou import BuscadorAutomaticoDOU

# Buscar portarias de 2018-2025
buscador = BuscadorAutomaticoDOU()
arquivo = buscador.gerar_planilha_periodo(
    data_inicio="2018-01-01",
    data_fim="2025-12-31"
)
```

## Funcionalidades

### 🔍 Análise de Portarias
- Análise de portarias de naturalização
- Verificação de erros e inconsistências
- Geração de relatórios em Excel
- Interface web interativa
- Suporte a análise de múltiplas portarias simultaneamente

### 🚀 Busca Automática DOU
- **Busca por período**: Define datas de início e fim
- **Palavras-chave personalizáveis**: Use palavras-chave específicas
- **Filtro inteligente**: Identifica automaticamente portarias de naturalização
- **Extração completa**: Nome, documento, processo, país, estado, idade, etc.
- **Remoção de duplicatas**: Evita processar a mesma portaria múltiplas vezes
- **Geração automática de planilhas**: Excel com todos os dados organizados

## 📊 Dados Extraídos

O sistema extrai automaticamente:
- **Nome completo** da pessoa naturalizada
- **Documento** (CPF, RG, etc.)
- **Número do processo**
- **País de origem**
- **Estado de residência**
- **Idade** e **data de nascimento**
- **Nome do pai**
- **Informações da portaria** (número, data, tipo)

## 🧪 Testes

Execute os testes para verificar se tudo está funcionando:

```bash
cd analisadorportarias
python teste_busca_automatica.py
```

## 📚 Documentação

- [Documentação da Busca Automática](README_BUSCA_AUTOMATICA.md)
- [Exemplo prático](analisadorportarias/exemplo_busca_2018_2025.py)

## ⚠️ Limitações

- **Rate limiting**: O sistema inclui pausas entre requisições
- **Dependência da API**: Sistema depende da API do Querido Diário
- **Períodos longos**: Para períodos muito longos, considere dividir em partes menores

## Notas

- Certifique-se de que o ChromeDriver está instalado e no PATH do sistema
- O sistema requer acesso à internet para baixar portarias de URLs
- Mantenha o Google Chrome atualizado
- A busca automática pode demorar dependendo do período solicitado

## 📞 Suporte

Para dúvidas sobre a busca automática, consulte:
- [Documentação da Busca Automática](README_BUSCA_AUTOMATICA.md)
- [Projeto Ro-DOU](https://github.com/gestaogovbr/Ro-dou)
