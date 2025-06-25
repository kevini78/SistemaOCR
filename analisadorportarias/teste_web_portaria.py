#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste para verificar se os campos processo e estado estão sendo extraídos corretamente
"""

from portaria_analyzer import PortariaAnalyzer

def testar_campos_processo_estado():
    """Testa se os campos processo e estado estão sendo extraídos"""
    
    # Texto de teste com uma pessoa
    texto_teste = """PORTARIA, Nº 5.149, DE 24 DE JUNHO DE 2025

A COORDENADORA DE PROCESSOS MIGRATÓRIOS, no uso da competência delegada pela Portaria nº 623 de 13 de novembro de 2020, publicada no Diário Oficial da União, de 17 de novembro de 2020, RESOLVE:

CONCEDER a nacionalidade brasileira, por naturalização, às pessoas abaixo relacionadas, nos termos do art. 12, II, "a", da Constituição Federal de 1988, e em conformidade com o art. 65 da Lei nº 13.445, de 24 de maio de 2017, regulamentada pelo Decreto nº 9.199/2017, de 20 de novembro de 2020, a fim de que possam gozar dos direitos outorgados pela Constituição e leis do Brasil:

DIAMANTINO GOMES IOIA - F010378-A, natural da Guiné-Bissau, nascido em 25 de setembro de 1991, filho de João Gomes Ioia e de Maria Gomes Ioia, residente no estado de São Paulo (Processo nº 235881.0499242/2024);

As pessoas referidas nesta Portaria deverão comparecer perante a Justiça Eleitoral para o devido cadastramento, nos termos do art. 231 do Decreto nº 9.199/2017, que regulamenta a Lei nº 13.445/2017."""

    print("🧪 TESTE DE CAMPOS PROCESSO E ESTADO")
    print("=" * 50)
    
    # Criar analisador
    analyzer = PortariaAnalyzer()
    
    # Analisar texto
    resultados, arquivos_excel = analyzer.analisar_multiplas_portarias(texto_teste, gerar_excel=False)
    
    if resultados and len(resultados) > 0:
        resultado = resultados[0]
        dados = resultado['dados_portaria']
        pessoas = dados['pessoas']
        
        print(f"✅ Portaria encontrada: {dados['numero']}")
        print(f"✅ Tipo: {dados['tipo']}")
        print(f"✅ Pessoas extraídas: {len(pessoas)}")
        
        for i, pessoa in enumerate(pessoas, 1):
            print(f"\n--- PESSOA {i} ---")
            print(f"Nome: {pessoa['nome']}")
            print(f"Documento: {pessoa['documento']} ({pessoa['tipo_documento']})")
            print(f"Processo: {pessoa.get('processo', 'NÃO ENCONTRADO')}")
            print(f"País: {pessoa['pais']}")
            print(f"Estado: {pessoa.get('estado', 'NÃO ENCONTRADO')}")
            print(f"Idade: {pessoa['idade']} anos")
            print(f"Nascimento: {pessoa['data_nascimento']}")
            
            # Verificar se os campos estão presentes
            if pessoa.get('processo'):
                print("✅ Processo extraído corretamente")
            else:
                print("❌ Processo NÃO encontrado")
                
            if pessoa.get('estado'):
                print("✅ Estado extraído corretamente")
            else:
                print("❌ Estado NÃO encontrado")
    else:
        print("❌ Nenhum resultado encontrado")

if __name__ == "__main__":
    testar_campos_processo_estado() 