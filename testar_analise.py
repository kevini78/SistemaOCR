from analisadorportarias.portaria_analyzer import PortariaAnalyzer
import requests

# Criar analisador
analyzer = PortariaAnalyzer()

# URL da portaria
url = 'https://www.in.gov.br/web/dou/-/portaria-n-4.384-de-12-de-dezembro-de-2024-601134381'

print(f'\nTentando acessar URL: {url}')

# Obter o conteúdo da portaria usando requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Usar BeautifulSoup para extrair o texto principal
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar o elemento principal que contém o texto da portaria
    conteudo = soup.find('div', {'class': 'conteudo-dou'})
    if conteudo:
        texto = conteudo.get_text(separator='\n', strip=True)
        print(f'\nTexto obtido com sucesso! Tamanho: {len(texto)} caracteres')
        print('Início do texto: ' + texto[:500])
        
        # Analisar diretamente o texto
        resultado = analyzer.analisar_texto_portaria(texto, gerar_excel=False)
        
        # Mostrar resultados
        print(f'\nResultado da análise:')
        print(f'Pessoas encontradas: {len(resultado.get("dados_portaria", {}).get("pessoas", []))}')
        print(f'Tipo de naturalização: {resultado.get("dados_portaria", {}).get("tipo")}')
        print(f'Número da portaria: {resultado.get("dados_portaria", {}).get("numero")}')
        
        # Para debug, mostrar as primeiras pessoas encontradas
        pessoas = resultado.get("dados_portaria", {}).get("pessoas", [])
        print('\nPessoas encontradas:')
        for i, pessoa in enumerate(pessoas[:5], 1):
            print(f'{i}. {pessoa["nome"]} ({pessoa["pais"]})')
    else:
        print('❌ Não foi possível encontrar o conteúdo principal da portaria')
        print('Texto bruto encontrado:')
        print(response.text[:500])
else:
    print(f'Erro ao obter a portaria: Status {response.status_code}')
    print('Resposta do servidor:')
    print(response.text)
