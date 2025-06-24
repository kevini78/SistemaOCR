#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analisadorportarias.portaria_analyzer import PortariaAnalyzer

def testar_portaria_web():
    """Testa a análise da portaria real da web"""
    
    url_portaria = "https://www.in.gov.br/web/dou/-/portaria-n-5.124-de-12-de-junho-de-2025-636007509"
    
    print("=== TESTE DA PORTARIA REAL DA WEB ===")
    print(f"URL: {url_portaria}")
    print()
    
    # Criar instância do analisador
    analyzer = PortariaAnalyzer()
    
    # Analisar a portaria
    print("Iniciando análise da portaria...")
    resultado = analyzer.analisar_portaria(url_portaria, gerar_excel=False)
    
    if 'erro' in resultado:
        print(f"❌ Erro: {resultado['erro']}")
        return
    
    print(f"\n✅ Análise concluída!")
    print(f"📊 {resultado['total_erros']} erros encontrados em {resultado['total_portarias']} portarias.")
    
    # Mostrar resultados de cada portaria
    for idx, res in enumerate(resultado['resultados'], 1):
        if res['dados_portaria']:
            dados = res['dados_portaria']
            print(f"\n--- PORTARIA {idx}: Nº {dados['numero']} ({dados['tipo']}) ---")
            print(f"Data: {dados['data']}")
            print(f"Pessoas encontradas: {len(dados['pessoas'])}")
            
            # Listar todas as pessoas
            for i, pessoa in enumerate(dados['pessoas'], 1):
                print(f"  {i:2d}. {pessoa['nome']} ({pessoa['pais']}) - {pessoa['idade']} anos")
            
            # Verificar se as pessoas faltantes estão presentes
            pessoas_faltantes_esperadas = [
                'ADAMA SANOGO',
                'AMALIA LAURA PASQUALINI', 
                'CLEETCHY CHOULOUTE',
                'OMAR SALLAM'
            ]
            
            nomes_encontrados = [p['nome'].upper() for p in dados['pessoas']]
            
            print(f"\n--- VERIFICAÇÃO DAS PESSOAS FALTANTES ---")
            for pessoa_esperada in pessoas_faltantes_esperadas:
                if pessoa_esperada in nomes_encontrados:
                    print(f"✅ {pessoa_esperada} - ENCONTRADA")
                else:
                    print(f"❌ {pessoa_esperada} - NÃO ENCONTRADA")
            
            # Mostrar erros se houver
            if res['erros']:
                print(f"\n⚠️ Erros encontrados: {len(res['erros'])}")
                for erro in res['erros'][:3]:  # Mostrar apenas os primeiros 3
                    print(f"  - {erro['descrição']}")
    
    # Resumo final
    todas_pessoas = []
    for res in resultado['resultados']:
        if res['dados_portaria']:
            todas_pessoas.extend(res['dados_portaria']['pessoas'])
    
    print(f"\n{'='*60}")
    print(f"📋 RESUMO FINAL")
    print(f"{'='*60}")
    print(f"Total de portarias analisadas: {resultado['total_portarias']}")
    print(f"Total de pessoas captadas: {len(todas_pessoas)}")
    print(f"Total de erros: {resultado['total_erros']}")
    
    # Verificar se todas as pessoas esperadas foram encontradas
    nomes_todas = [p['nome'].upper() for p in todas_pessoas]
    pessoas_faltantes = []
    for pessoa in ['ADAMA SANOGO', 'AMALIA LAURA PASQUALINI', 'CLEETCHY CHOULOUTE', 'OMAR SALLAM']:
        if pessoa not in nomes_todas:
            pessoas_faltantes.append(pessoa)
    
    if pessoas_faltantes:
        print(f"\n❌ PESSOAS AINDA FALTANDO: {len(pessoas_faltantes)}")
        for pessoa in pessoas_faltantes:
            print(f"  - {pessoa}")
    else:
        print(f"\n🎉 SUCESSO! Todas as pessoas foram captadas!")

if __name__ == "__main__":
    testar_portaria_web() 