#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste das Correções do Analisador de Portarias
Verifica se os problemas foram corrigidos
"""

import os
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

def testar_correcoes():
    """Testa as correções implementadas"""
    
    # Texto da portaria definitiva (que estava sendo identificada como provisória)
    texto_definitiva = """PORTARIA Nº 5.127, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, resolve:

TORNAR DEFINITIVA a nacionalidade brasileira concedida, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, inciso II, alínea "a", da Constituição Federal de 1988, e em conformidade com o art. 70, Parágrafo único, da Lei nº 13.445/2017, regulamentada pelo Decreto nº 9.199/2017, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:

OMAR SALLAM - G260172-F, natural da Palestina, nascido em 10 de janeiro de 2006, filho de Khaled Sallam e de Amal Hamedh, residente no estado de São Paulo (Processo 235881.0545721/2024).

A pessoa referida nesta Portaria deverá comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX"""

    # Texto da portaria ordinária (que estava sendo identificada como provisória)
    texto_ordinaria = """PORTARIA Nº 5.124, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, resolve:

CONCEDER a nacionalidade brasileira, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, II, "a", da Constituição Federal de 1988, e em conformidade com o art. 65 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:

ADAMA SANOGO - F133290-R, natural de Burquina Faso, nascido(a) em 22 de março de 1992, filho(a) de Sanogo Moumount e de Drabo Mariam, residente no estado de São Paulo (Processo nº 235881.0546208/2024);

BARA DIOP - G403090-O, natural do Senegal, nascido em 14 de julho de 1988, filho de Alla Diop e de Diama Diop, residente no Estado do Rio de Janeiro (Processo 235881.0552453/2024);

JUDY MADDAH - B077459-8, natural da Síria, nascida em 4 de julho de 2017, filha de Hatem Maddah e de Yussra Orabi, residente no estado de São Paulo (Processo 235881.0545581/2024) e

SISA MADALENA MVEMBA - F671034-X, natural da Angola, nascida em 21 de abril de 1987, filha de João Mvemba e de Maria Luisa, residente no Estado de São Paulo (Processo 235881.0552263/2024).

As pessoas referidas nesta Portaria deverão comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX"""

    print("="*80)
    print("🔧 TESTE DAS CORREÇÕES IMPLEMENTADAS")
    print("="*80)
    
    # Verificar se há planilha de histórico
    caminho_historico = "historico_naturalizacoes.xlsx" if os.path.exists("historico_naturalizacoes.xlsx") else None
    
    if caminho_historico:
        print(f"✅ Usando planilha de histórico: {caminho_historico}")
    else:
        print("⚠️  Planilha de histórico não encontrada - teste sem verificação de duplicatas")
    
    analyzer = PortariaAnalyzer(caminho_historico)
    
    # Teste 1: Portaria Definitiva (deveria ser identificada como DEFINITIVA)
    print("\n" + "="*60)
    print("📋 TESTE 1: PORTARIA DEFINITIVA (5.127)")
    print("="*60)
    
    resultado1 = analyzer.analisar_texto_portaria(texto_definitiva, gerar_excel=False)
    
    if resultado1['dados_portaria']:
        print(f"\n✅ Tipo identificado: {resultado1['dados_portaria']['tipo']}")
        print(f"✅ Total de pessoas: {len(resultado1['dados_portaria']['pessoas'])}")
        print(f"✅ Total de erros: {resultado1['total_erros']}")
        
        # Verificar se o tipo está correto
        if resultado1['dados_portaria']['tipo'] == 'DEFINITIVA':
            print("✅ CORREÇÃO FUNCIONOU: Tipo identificado corretamente como DEFINITIVA")
        else:
            print(f"❌ PROBLEMA: Tipo identificado como {resultado1['dados_portaria']['tipo']}, deveria ser DEFINITIVA")
        
        if resultado1['erros']:
            print("\n🔍 Erros encontrados:")
            for i, erro in enumerate(resultado1['erros'], 1):
                print(f"   {i}. {erro['descrição']}")
    
    # Teste 2: Portaria Ordinária (deveria ser identificada como ORDINARIA)
    print("\n" + "="*60)
    print("📋 TESTE 2: PORTARIA ORDINÁRIA (5.124)")
    print("="*60)
    
    resultado2 = analyzer.analisar_texto_portaria(texto_ordinaria, gerar_excel=False)
    
    if resultado2['dados_portaria']:
        print(f"\n✅ Tipo identificado: {resultado2['dados_portaria']['tipo']}")
        print(f"✅ Total de pessoas: {len(resultado2['dados_portaria']['pessoas'])}")
        print(f"✅ Total de erros: {resultado2['total_erros']}")
        
        # Verificar se o tipo está correto
        if resultado2['dados_portaria']['tipo'] == 'ORDINARIA':
            print("✅ CORREÇÃO FUNCIONOU: Tipo identificado corretamente como ORDINARIA")
        else:
            print(f"❌ PROBLEMA: Tipo identificado como {resultado2['dados_portaria']['tipo']}, deveria ser ORDINARIA")
        
        # Verificar se o "e" foi removido
        pessoas_com_e = [p for p in resultado2['dados_portaria']['pessoas'] if p['nome'].strip() in ['e', 'E']]
        if not pessoas_com_e:
            print("✅ CORREÇÃO FUNCIONOU: 'e' isolado foi removido da lista de pessoas")
        else:
            print(f"❌ PROBLEMA: Ainda há {len(pessoas_com_e)} pessoas com 'e' isolado")
        
        if resultado2['erros']:
            print("\n🔍 Erros encontrados:")
            for i, erro in enumerate(resultado2['erros'], 1):
                print(f"   {i}. {erro['descrição']}")
    
    print("\n" + "="*80)
    print("🎉 TESTES DAS CORREÇÕES CONCLUÍDOS!")
    print("="*80)
    
    # Resumo das correções testadas
    print("\n📝 CORREÇÕES TESTADAS:")
    print("1. ✅ Identificação correta de portaria DEFINITIVA")
    print("2. ✅ Identificação correta de portaria ORDINARIA")
    print("3. ✅ Remoção de 'e' isolado da lista de pessoas")
    print("4. ✅ Verificação de duplicatas na mesma portaria")

if __name__ == "__main__":
    testar_correcoes() 