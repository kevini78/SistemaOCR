#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste com o texto real fornecido pelo usuário
"""

from portaria_analyzer import PortariaAnalyzer

def testar_texto_real():
    """Testa com o texto real fornecido pelo usuário"""
    
    # Texto real fornecido pelo usuário
    texto_real = """DEPARTAMENTO DE MIGRAÇOES
##ATO PORTARIA, Nº 5.149, DE 24 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, RESOLVE:

CONCEDER a nacionalidade brasileira, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, II, "a", da Constituição Federal de 1988, e em conformidade com o art. 65 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:
 
AKEEM AKINOLA APENA - V005786-X, natural da Nigéria, nascido(a) em 5 de maio de 1965, filho(a) de Raheem Apena e de Safurat Apena, residente no estado de São Paulo (Processo nº 235881.0499242/2024);

As pessoas referidas nesta Portaria deverão comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX
Coordenadora de Processos Migratórios

DEPARTAMENTO DE MIGRAÇOES
##ATO PORTARIA, Nº 5.150, DE 24 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, RESOLVE:
 
CONCEDER a nacionalidade brasileira, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, II, "b", da Constituição Federal de 1988, e em conformidade com o art. 67 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:
 
PABLO CESAR LEHMANN ALBORNOZ - V278540-V, natural da Colômbia, nascido em 28 de março de 1974, filho de Fabricio Lehmann Gonzalez e de Gloria Isabel Albornoz Montilla, residente no Estado do Rio Grande do Sul (Processo 235881.0570932/2024);

As pessoas referidas nesta Portaria deverão comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX
Coordenadora de Processos Migratórios

DEPARTAMENTO DE MIGRAÇOES
##ATO PORTARIA, Nº 5.151, DE 24 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020: RESOLVE:

CONCEDER a nacionalidade brasileira, por Naturalização Provisória, às pessoas abaixo relacionadas, nos termos do art. 12, inciso II, alínea "a", da Constituição Federal de 1988, e em conformidade com o art. 70 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possa gozar dos direitos outorgados pela Constituição e leis do Brasil, até 2 (dois) anos após atingir a maioridade, nos termos do Parágrafo único do referido artigo:
 
ARAMIDE NGOZI AKINTOLA - F988304-5, natural da Nigéria, nascida em 14 de julho de 2015, filha de Oluwadare Akintola e de Ijeoma Akintola, residente no estado de São Paulo (Processo 235881.0512924/2024);
ATAHUALPA ABRAHAM YAQUIRA - F742007-5, natural da Argentina, nascido em 20 de outubro de 2020, filho de Mariano Yaquira e de Maria Paola Joffre Rosales, residente no estado de Santa Catarina (Processo 235881.0566628/2024);
BEGUM MARIAM - B013564-U, natural de Bangladesh, nascida em 11 de novembro de 2021, filha de Gulam Shahria e de Mazeda Akter Munni, residente no estado de São Paulo (Processo 235881.0531600/2024) e
ISMAIL ILYASOV - F988388-A, natural da Rússia, nascido em 28 de junho de 2016, filho de Rustam Ilyasov e de Aliya Tukhtarova, residente no estado de São Paulo (Processo 235881.0569859/2024).

As pessoas referidas nesta Portaria deverão comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017.

SANDRA MARIA MENDES ADJAFRE SINDEAUX
Coordenadora de Processos Migratórios"""

    print("="*60)
    print("🧪 TESTE COM TEXTO REAL")
    print("="*60)
    
    # Inicializar analisador
    analyzer = PortariaAnalyzer()
    
    print("\n📋 Analisando texto real...")
    print(f"Tamanho do texto: {len(texto_real)} caracteres")
    
    # Analisar múltiplas portarias
    resultados, arquivos_excel = analyzer.analisar_multiplas_portarias(texto_real, gerar_excel=False)
    
    print(f"\n✅ Análise concluída!")
    print(f"📊 Total de portarias encontradas: {len(resultados)}")
    
    total_pessoas = 0
    total_erros = 0
    
    for i, resultado in enumerate(resultados, 1):
        dados = resultado['dados_portaria']
        erros = resultado['erros']
        
        print(f"\n--- PORTARIA {i} ---")
        print(f"Número: {dados['numero']}")
        print(f"Data: {dados['data']}")
        print(f"Tipo: {dados['tipo']}")
        print(f"Pessoas: {len(dados['pessoas'])}")
        print(f"Erros: {len(erros)}")
        
        total_pessoas += len(dados['pessoas'])
        total_erros += len(erros)
        
        # Mostrar algumas pessoas
        for j, pessoa in enumerate(dados['pessoas'][:3], 1):
            print(f"  {j}. {pessoa['nome']} - {pessoa['pais']}")
        
        if len(dados['pessoas']) > 3:
            print(f"  ... e mais {len(dados['pessoas']) - 3} pessoas")
    
    print(f"\n📈 RESUMO FINAL:")
    print(f"Total de portarias: {len(resultados)}")
    print(f"Total de pessoas: {total_pessoas}")
    print(f"Total de erros: {total_erros}")
    
    # Verificar se a portaria 5.151 foi identificada como PROVISORIA
    portaria_5151 = None
    for resultado in resultados:
        if '5.151' in resultado['dados_portaria']['numero']:
            portaria_5151 = resultado
            break
    
    if portaria_5151:
        tipo_5151 = portaria_5151['dados_portaria']['tipo']
        print(f"\n🔍 VERIFICAÇÃO ESPECIAL:")
        print(f"Portaria 5.151 identificada como: {tipo_5151}")
        if tipo_5151 == 'PROVISORIA':
            print("✅ SUCESSO: Portaria 5.151 identificada corretamente como PROVISORIA!")
        else:
            print(f"❌ PROBLEMA: Portaria 5.151 deveria ser PROVISORIA, mas foi identificada como {tipo_5151}")
    else:
        print("❌ PROBLEMA: Portaria 5.151 não foi encontrada!")
    
    return resultados

if __name__ == "__main__":
    testar_texto_real() 