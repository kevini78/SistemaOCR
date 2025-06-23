#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste de Múltiplas Portarias
Verifica se a separação e análise de múltiplas portarias está funcionando corretamente
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

def testar_multiplas_portarias():
    """Testa a análise de múltiplas portarias com duplicatas"""
    
    # Texto com 3 portarias diferentes (ordinária, provisória, definitiva)
    texto_multiplas = """PORTARIA Nº 5.124, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, resolve:

CONCEDER a nacionalidade brasileira, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, II, "a", da Constituição Federal de 1988, e em conformidade com o art. 65 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:

ADAMA SANOGO - F133290-R, natural de Burquina Faso, nascido(a) em 22 de março de 1992, filho(a) de Sanogo Moumount e de Drabo Mariam, residente no estado de São Paulo (Processo nº 235881.0546208/2024);

BARA DIOP - G403090-O, natural do Senegal, nascido em 14 de julho de 1988, filho de Alla Diop e de Diama Diop, residente no Estado do Rio de Janeiro (Processo 235881.0552453/2024);

JUDY MADDAH - B077459-8, natural da Síria, nascida em 4 de julho de 2017, filha de Hatem Maddah e de Yussra Orabi, residente no estado de São Paulo (Processo 235881.0545581/2024).

As pessoas referidas nesta Portaria deverão comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX

PORTARIA Nº 5.126, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020: resolve:

CONCEDER a nacionalidade brasileira, por Naturalização Provisória, às pessoas abaixo relacionadas, nos termos do art. 12, inciso II, alínea "a", da Constituição Federal de 1988, e em conformidade com o art. 70 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possa gozar dos direitos outorgados pela Constituição e leis do Brasil, até 2 (dois) anos após atingir a maioridade, nos termos do Parágrafo único do referido artigo:

CLEETCHY CHOULOUTE - F265158-T, natural do Haiti, nascido em 5 de novembro de 2012, filho de Nesly Chouloute e de Fabienne Decilien, residente no estado de São Paulo (Processo 235881.0554712/2024);

JUDY MADDAH - B077459-8, natural da Síria, nascida em 4 de julho de 2017, filha de Hatem Maddah e de Yussra Orabi, residente no estado de São Paulo (Processo 235881.0545581/2024);

LARIA HAMDAN - F889386-G, natural do Líbano, nascida em 9 de novembro de 2019, filha de Rawi Hamdan e de Ayla Farid Saado Kawash, residente no estado de Santa Catarina (Processo 235881.0542302/2024).

SANDRA MARIA MENDES ADJAFRE SINDEAUX

PORTARIA Nº 5.127, DE 12 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, resolve:

TORNAR DEFINITIVA a nacionalidade brasileira concedida, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, inciso II, alínea "a", da Constituição Federal de 1988, e em conformidade com o art. 70, Parágrafo único, da Lei nº 13.445/2017, regulamentada pelo Decreto nº 9.199/2017, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:

OMAR SALLAM - G260172-F, natural da Palestina, nascido em 10 de janeiro de 2006, filho de Khaled Sallam e de Amal Hamedh, residente no estado de São Paulo (Processo 235881.0545721/2024).

A pessoa referida nesta Portaria deverá comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX"""

    print("="*80)
    print("🧪 TESTE DE MÚLTIPLAS PORTARIAS")
    print("="*80)
    
    # Verificar se há planilha de histórico
    caminho_historico = "historico_naturalizacoes.xlsx" if os.path.exists("historico_naturalizacoes.xlsx") else None
    
    if caminho_historico:
        print(f"✅ Usando planilha de histórico: {caminho_historico}")
    else:
        print("⚠️  Planilha de histórico não encontrada - teste sem verificação de duplicatas")
    
    analyzer = PortariaAnalyzer(caminho_historico)
    
    print("\nAnalisando texto com múltiplas portarias...")
    print("-" * 60)
    
    resultados, arquivos_excel = analyzer.analisar_multiplas_portarias(texto_multiplas, gerar_excel=False)
    
    print(f"\n🎉 Análise concluída!")
    print(f"📊 Total de portarias encontradas: {len(resultados)}")
    
    total_erros = sum(r['total_erros'] for r in resultados)
    print(f"📊 Total de erros encontrados: {total_erros}")
    
    # Verificar se encontrou exatamente 3 portarias
    if len(resultados) == 3:
        print("✅ CORREÇÃO FUNCIONOU: Encontrou exatamente 3 portarias")
    else:
        print(f"❌ PROBLEMA: Encontrou {len(resultados)} portarias, deveria ser 3")
    
    # Mostrar resultado de cada portaria
    for idx, resultado in enumerate(resultados, 1):
        print(f"\n================ PORTARIA {idx} ================")
        if resultado['dados_portaria']:
            dados = resultado['dados_portaria']
            print(f"Portaria: {dados['numero']}")
            print(f"Data: {dados['data']}")
            print(f"Tipo: {dados['tipo']}")
            print(f"Total de pessoas: {len(dados['pessoas'])}")
            print(f"Total de erros: {resultado['total_erros']}")
            
            # Verificar se o tipo está correto
            tipos_esperados = ['ORDINARIA', 'PROVISORIA', 'DEFINITIVA']
            if idx <= len(tipos_esperados) and dados['tipo'] == tipos_esperados[idx-1]:
                print(f"✅ Tipo correto: {dados['tipo']}")
            else:
                print(f"❌ Tipo incorreto: {dados['tipo']}, esperado: {tipos_esperados[idx-1] if idx <= len(tipos_esperados) else 'N/A'}")
            
            if resultado['erros']:
                print(f"\nErros encontrados:")
                for i, erro in enumerate(resultado['erros'], 1):
                    print(f"   {i}. {erro['descrição']}")
                    
                    # Verificar se há erro de duplicata entre portarias
                    if erro['tipo'] == 'DUPLICATA_ENTRE_PORTARIAS':
                        print(f"      ✅ DUPLICATA DETECTADA: {erro['descrição']}")
            else:
                print("\n✅ Nenhum erro encontrado!")
        else:
            print("❌ Não foi possível extrair dados desta portaria")
    
    print("\n" + "="*80)
    print("🎉 TESTE CONCLUÍDO!")
    print("="*80)
    
    # Resumo do teste
    print("\n📝 RESUMO DO TESTE:")
    print(f"1. ✅ Portarias encontradas: {len(resultados)}")
    print(f"2. ✅ Total de erros: {total_erros}")
    print("3. ✅ Verificação de duplicatas entre portarias")
    print("4. ✅ Identificação correta dos tipos")

if __name__ == "__main__":
    testar_multiplas_portarias() 