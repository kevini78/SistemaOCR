# Analisador de Portarias de Naturalização

Este é um sistema para análise automática de portarias de naturalização brasileira.

## Requisitos

- Python 3.7 ou superior
- ChromeDriver (para Selenium) - deve estar no PATH do sistema
- Google Chrome instalado

## Instalação

1. Clone este repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd AnalisadorPortariasWindsurf
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
python app.py
```

## Uso

1. Acesse o aplicativo através do navegador em: http://localhost:5000
2. Use a interface web para analisar portarias através de URL ou texto
3. O sistema irá processar as portarias e mostrar os resultados na interface

## Funcionalidades

- Análise de portarias de naturalização
- Verificação de erros e inconsistências
- Geração de relatórios em Excel
- Interface web interativa
- Suporte a análise de múltiplas portarias simultaneamente

## Notas

- Certifique-se de que o ChromeDriver está instalado e no PATH do sistema
- O sistema requer acesso à internet para baixar portarias de URLs
- Mantenha o Google Chrome atualizado
