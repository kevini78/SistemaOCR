# Busca Automática DOU - Sistema de Análise de Portarias

## 📋 Visão Geral

Esta funcionalidade implementa uma busca automática de portarias de naturalização no Diário Oficial da União (DOU), baseada no conceito do [Ro-DOU](https://github.com/gestaogovbr/Ro-dou). O sistema permite buscar portarias por período e automaticamente extrair e organizar os dados das pessoas naturalizadas em uma planilha Excel.

## 🚀 Funcionalidades

### ✨ Busca Automática
- **Busca por período**: Define datas de início e fim para a busca
- **Palavras-chave personalizáveis**: Use palavras-chave específicas ou as padrão
- **Filtro inteligente**: Identifica automaticamente portarias de naturalização
- **Remoção de duplicatas**: Evita processar a mesma portaria múltiplas vezes

### 📊 Extração de Dados
- **Nome completo** da pessoa naturalizada
- **Documento** (CPF, RG, etc.)
- **Número do processo**
- **País de origem**
- **Estado de residência**
- **Idade** e **data de nascimento**
- **Nome do pai**
- **Informações da portaria** (número, data, tipo)

### 📈 Geração de Relatórios
- **Planilha Excel** com todos os dados extraídos
- **Estatísticas** de registros encontrados
- **Download automático** do arquivo gerado

## 🛠️ Como Usar

### Interface Web
1. Acesse a página "Busca Automática" no sistema
2. Defina o período de busca (data início e fim)
3. (Opcional) Adicione palavras-chave específicas
4. Clique em "Iniciar Busca Automática"
5. Aguarde o processamento
6. Baixe a planilha gerada

### Linha de Comando
```python
from busca_automatica_dou import BuscadorAutomaticoDOU

# Inicializar buscador
buscador = BuscadorAutomaticoDOU()

# Buscar portarias de um período
arquivo = buscador.gerar_planilha_periodo(
    data_inicio="2024-01-01",
    data_fim="2024-12-31"
)

print(f"Planilha gerada: {arquivo}")
```

## 📁 Estrutura dos Arquivos

```
SistemaAnalisador/
├── analisadorportarias/
│   ├── busca_automatica_dou.py      # Módulo principal da busca
│   ├── templates/
│   │   └── busca_automatica.html    # Interface web
│   ├── app.py                       # Rotas da aplicação web
│   └── teste_busca_automatica.py    # Script de teste
└── README_BUSCA_AUTOMATICA.md       # Esta documentação
```

## 🔧 Configuração

### Dependências
O sistema utiliza a API do [Querido Diário](https://queridodiario.ok.org.br/) para buscar no DOU. As dependências necessárias estão no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Palavras-chave Padrão
O sistema usa as seguintes palavras-chave por padrão:
- `naturalização`
- `naturalizacao`
- `PORTARIA`
- `nacionalidade brasileira`
- `art. 65`
- `art. 67`
- `art. 70`

## 🧪 Testes

Execute o script de teste para verificar se a funcionalidade está funcionando:

```bash
cd SistemaAnalisador/analisadorportarias
python teste_busca_automatica.py
```

## 📊 Formato da Planilha Gerada

A planilha Excel contém as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| nome | Nome completo da pessoa |
| documento | Número do documento |
| tipo_documento | Tipo do documento (CPF, RG, etc.) |
| processo | Número do processo |
| pais | País de origem |
| estado | Estado de residência |
| idade | Idade da pessoa |
| data_nascimento | Data de nascimento |
| nome_pai | Nome do pai |
| numero_portaria | Número da portaria |
| data_portaria | Data da portaria |
| tipo_naturalizacao | Tipo de naturalização |
| data_publicacao_dou | Data de publicação no DOU |
| url_portaria | URL da portaria no DOU |

## ⚠️ Limitações e Considerações

### Rate Limiting
- O sistema inclui pausas entre requisições para não sobrecarregar a API
- Recomenda-se não fazer buscas muito frequentes

### Dependência da API
- O sistema depende da disponibilidade da API do Querido Diário
- Em caso de indisponibilidade, a busca pode falhar

### Períodos Longos
- Para períodos muito longos (ex: anos), a busca pode demorar
- Considere dividir buscas longas em períodos menores

## 🔍 Exemplo de Uso

### Busca de 2018-2025
Para buscar todas as portarias de naturalização de 2018 a 2025:

1. **Interface Web**:
   - Data início: `2018-01-01`
   - Data fim: `2025-12-31`
   - Clique em "Iniciar Busca Automática"

2. **Linha de Comando**:
```python
arquivo = buscador.gerar_planilha_periodo(
    data_inicio="2018-01-01",
    data_fim="2025-12-31",
    nome_arquivo="naturalizacoes_2018_2025.xlsx"
)
```

## 🆘 Solução de Problemas

### Erro de Conexão
- Verifique sua conexão com a internet
- Tente novamente em alguns minutos

### Nenhuma Portaria Encontrada
- Verifique se o período está correto
- Tente palavras-chave diferentes
- Considere um período menor

### Erro na Extração
- Algumas portarias podem ter formato diferente
- O sistema registra erros para análise posterior

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs de erro
2. Execute o script de teste
3. Consulte a documentação do Ro-DOU
4. Entre em contato com a equipe de desenvolvimento

---

**Baseado no projeto [Ro-DOU](https://github.com/gestaogovbr/Ro-dou) da Secretaria de Gestão e Inovação do Ministério da Gestão e da Inovação em Serviços Públicos.** 