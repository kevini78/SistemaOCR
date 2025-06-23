#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste do Analisador de Portarias de Naturalização
Demonstra as correções implementadas
"""

from datetime import datetime
import os

# Importar a classe do arquivo principal
from importlib import import_module
import sys

# Adicionar o diretório atual ao path
sys.path.append('.')

try:
    from importlib import import_module
    portaria_module = import_module('1')
    PortariaAnalyzer = portaria_module.PortariaAnalyzer
except ImportError as e:
    print(f"Erro ao importar módulo: {e}")
    sys.exit(1)

def testar_portaria():
    """Testa a análise de uma portaria específica"""
    
    # Texto da portaria de teste (Portaria 5.124)
    texto_portaria = """PORTARIA Nº 5.124, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, resolve:

CONCEDER a nacionalidade brasileira, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, II, "a", da Constituição Federal de 1988, e em conformidade com o art. 65 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:

ADAMA SANOGO - F133290-R, natural de Burquina Faso, nascido(a) em 22 de março de 1992, filho(a) de Sanogo Moumount e de Drabo Mariam, residente no estado de São Paulo (Processo nº 235881.0546208/2024);

BARA DIOP - G403090-O, natural do Senegal, nascido em 14 de julho de 1988, filho de Alla Diop e de Diama Diop, residente no Estado do Rio de Janeiro (Processo 235881.0552453/2024);

JUDY MADDAH - B077459-8, natural da Síria, nascida em 4 de julho de 2017, filha de Hatem Maddah e de Yussra Orabi, residente no estado de São Paulo (Processo 235881.0545581/2024);

REMAZ SAMEH IBRAHIM SHILLO - F224629-8, natural da Palestina, nascida em 5 de novembro de 2000, filha de Sameh Ibrahim Shillo e de Samar Abdel Qader, residente no Estado de Santa Catarina (Processo 235881.0543552/2024) e

SISA MADALENA MVEMBA - F671034-X, natural da Angola, nascida em 21 de abril de 1987, filha de João Mvemba e de Maria Luisa, residente no Estado de São Paulo (Processo 235881.0552263/2024).

As pessoas referidas nesta Portaria deverão comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX"""

    # Texto da portaria provisória (Portaria 5.126)
    texto_portaria_provisoria = """PORTARIA Nº 5.126, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020: resolve:

CONCEDER a nacionalidade brasileira, por Naturalização Provisória, às pessoas abaixo relacionadas, nos termos do art. 12, inciso II, alínea "a", da Constituição Federal de 1988, e em conformidade com o art. 70 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possa gozar dos direitos outorgados pela Constituição e leis do Brasil, até 2 (dois) anos após atingir a maioridade, nos termos do Parágrafo único do referido artigo:

CLEETCHY CHOULOUTE - F265158-T, natural do Haiti, nascido em 5 de novembro de 2012, filho de Nesly Chouloute e de Fabienne Decilien, residente no estado de São Paulo (Processo 235881.0554712/2024);

JUDY MADDAH - B077459-8, natural da Síria, nascida em 4 de julho de 2017, filha de Hatem Maddah e de Yussra Orabi, residente no estado de São Paulo (Processo 235881.0545581/2024);

LARIA HAMDAN - F889386-G, natural do Líbano, nascida em 9 de novembro de 2019, filha de Rawi Hamdan e de Ayla Farid Saado Kawash, residente no estado de Santa Catarina (Processo 235881.0542302/2024);

MAJED MADDAH - B077496-2, natural da Síria, nascido em 30 de março de 2016, filho de Hatem Maddah e de Yussra Orabi, residente no estado de São Paulo (Processo 235881.0545575/2024);

TALA ALZAFARI - G196769-D, natural da Síria, nascida em 9 de setembro de 2014, filha de Mhd Salim Al Zafari e de Nour Mourad, residente no estado de São Paulo (Processo 235881.0546141/2024) e

XAVIER DAVID MURRAY - B010625-E, natural do Reino Unido, nascido em 16 de junho de 2020, filho de Stuart Patrick Allison Murray e Jonalin Samontina Siano, residente no estado de São Paulo (Processo 235881.0556160/2024).

SANDRA MARIA MENDES ADJAFRE SINDEAUX"""

    # Texto da portaria definitiva (Portaria 5.127)
    texto_portaria_definitiva = """PORTARIA Nº 5.127, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, resolve:

TORNAR DEFINITIVA a nacionalidade brasileira concedida, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, inciso II, alínea "a", da Constituição Federal de 1988, e em conformidade com o art. 70, Parágrafo único, da Lei nº 13.445/2017, regulamentada pelo Decreto nº 9.199/2017, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:

OMAR SALLAM - G260172-F, natural da Palestina, nascido em 10 de janeiro de 2006, filho de Khaled Sallam e de Amal Hamedh, residente no estado de São Paulo (Processo 235881.0545721/2024).

A pessoa referida nesta Portaria deverá comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX"""

    print("="*80)
    print("🧪 TESTE DO ANALISADOR DE PORTARIAS - CORREÇÕES IMPLEMENTADAS")
    print("="*80)
    
    # Verificar se há planilha de histórico
    caminho_historico = "historico_naturalizacoes.xlsx" if os.path.exists("historico_naturalizacoes.xlsx") else None
    
    if caminho_historico:
        print(f"✅ Usando planilha de histórico: {caminho_historico}")
    else:
        print("⚠️  Planilha de histórico não encontrada - teste sem verificação de duplicatas")
    
    analyzer = PortariaAnalyzer(caminho_historico)
    
    # Teste 1: Portaria Ordinária
    print("\n" + "="*60)
    print("📋 TESTE 1: PORTARIA ORDINÁRIA (5.124)")
    print("="*60)
    
    resultado1 = analyzer.analisar_texto_portaria(texto_portaria, gerar_excel=False)
    
    if resultado1['dados_portaria']:
        print(f"\n✅ Tipo identificado: {resultado1['dados_portaria']['tipo']}")
        print(f"✅ Total de pessoas: {len(resultado1['dados_portaria']['pessoas'])}")
        print(f"✅ Total de erros: {resultado1['total_erros']}")
        
        if resultado1['erros']:
            print("\n🔍 Erros encontrados:")
            for i, erro in enumerate(resultado1['erros'], 1):
                print(f"   {i}. {erro['descrição']}")
    
    # Teste 2: Portaria Provisória
    print("\n" + "="*60)
    print("📋 TESTE 2: PORTARIA PROVISÓRIA (5.126)")
    print("="*60)
    
    resultado2 = analyzer.analisar_texto_portaria(texto_portaria_provisoria, gerar_excel=False)
    
    if resultado2['dados_portaria']:
        print(f"\n✅ Tipo identificado: {resultado2['dados_portaria']['tipo']}")
        print(f"✅ Total de pessoas: {len(resultado2['dados_portaria']['pessoas'])}")
        print(f"✅ Total de erros: {resultado2['total_erros']}")
        
        if resultado2['erros']:
            print("\n🔍 Erros encontrados:")
            for i, erro in enumerate(resultado2['erros'], 1):
                print(f"   {i}. {erro['descrição']}")
    
    # Teste 3: Portaria Definitiva
    print("\n" + "="*60)
    print("📋 TESTE 3: PORTARIA DEFINITIVA (5.127)")
    print("="*60)
    
    resultado3 = analyzer.analisar_texto_portaria(texto_portaria_definitiva, gerar_excel=False)
    
    if resultado3['dados_portaria']:
        print(f"\n✅ Tipo identificado: {resultado3['dados_portaria']['tipo']}")
        print(f"✅ Total de pessoas: {len(resultado3['dados_portaria']['pessoas'])}")
        print(f"✅ Total de erros: {resultado3['total_erros']}")
        
        if resultado3['erros']:
            print("\n🔍 Erros encontrados:")
            for i, erro in enumerate(resultado3['erros'], 1):
                print(f"   {i}. {erro['descrição']}")
    
    print("\n" + "="*80)
    print("🎉 TESTES CONCLUÍDOS!")
    print("="*80)
    
    # Resumo das correções
    print("\n📝 RESUMO DAS CORREÇÕES IMPLEMENTADAS:")
    print("1. ✅ Identificação correta dos tipos de naturalização")
    print("2. ✅ Adição de PALESTINA à lista de países oficiais")
    print("3. ✅ Mensagem específica quando pessoa não foi publicada anteriormente")
    print("4. ✅ Melhor tratamento de duplicatas na mesma portaria")
    print("5. ✅ Filtro para remover 'e' isolado no final das listas")
    print("6. ✅ Nova função para analisar texto direto da portaria")

if __name__ == "__main__":
    testar_portaria() 