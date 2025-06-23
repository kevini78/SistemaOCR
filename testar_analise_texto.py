from analisadorportarias.portaria_analyzer import PortariaAnalyzer

# Criar analisador
analyzer = PortariaAnalyzer()

# Texto de exemplo da portaria 4.384
texto = """
PORTARIA Nº 4.384, DE 23 DE JANEIRO DE 2025

O MINISTRO DE ESTADO DA JUSTIÇA E SEGURANÇA PÚBLICA, no uso das atribuições que lhe conferem o inciso II do parágrafo único do art. 87 da Constituição Federal e o Decreto nº 10.567, de 2020, e tendo em vista o disposto no art. 65 da Lei nº 6.015, de 31 de dezembro de 1973,

RESOLVE:

Art. 1º Tornar definitiva a naturalização brasileira:

I - do(a) brasileiro(a) naturalizado(a) por naturalização ordinária:

- RNM 1234567890, natural do(a) BRASIL, nascido(a) em 01 de janeiro de 1980, filho(a) de JOÃO SILVA;
- RNM 1234567891, natural do(a) BRASIL, nascido(a) em 02 de janeiro de 1980, filho(a) de MARIA SILVA;
- RNM 1234567892, natural do(a) BRASIL, nascido(a) em 03 de janeiro de 1980, filho(a) de PEDRO SILVA;
- RNM 1234567893, natural do(a) BRASIL, nascido(a) em 04 de janeiro de 1980, filho(a) de ANA SILVA;
- RNM 1234567894, natural do(a) BRASIL, nascido(a) em 05 de janeiro de 1980, filho(a) de LUCAS SILVA;
- RNM 1234567895, natural do(a) BRASIL, nascido(a) em 06 de janeiro de 1980, filho(a) de CARLOS SILVA;
- RNM 1234567896, natural do(a) BRASIL, nascido(a) em 07 de janeiro de 1980, filho(a) de FERNANDO SILVA;
- RNM 1234567897, natural do(a) BRASIL, nascido(a) em 08 de janeiro de 1980, filho(a) de PAULO SILVA;
- RNM 1234567898, natural do(a) BRASIL, nascido(a) em 09 de janeiro de 1980, filho(a) de RICARDO SILVA;
- RNM 1234567899, natural do(a) BRASIL, nascido(a) em 10 de janeiro de 1980, filho(a) de MARCOS SILVA;

Art. 2º Esta Portaria entra em vigor na data de sua publicação.

Brasília, 23 de janeiro de 2025.

ANDRÉ MENDONÇA

Ministro de Estado da Justiça e Segurança Pública
"""

# Analisar texto
resultado = analyzer.analisar_texto_portaria(texto)

# Mostrar resultados
print(f'\nResultado da análise:')
print(f'Pessoas encontradas: {len(resultado.get("dados_portaria", {}).get("pessoas", []))}')
print(f'Tipo de naturalização: {resultado.get("dados_portaria", {}).get("tipo")}')
print(f'Número da portaria: {resultado.get("dados_portaria", {}).get("numero")}')
