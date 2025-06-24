#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analisadorportarias.portaria_analyzer import PortariaAnalyzer

def testar_analise_atual():
    """Testa o comportamento atual do código"""
    
    # Ler o arquivo de teste
    with open('teste_portarias.txt', 'r', encoding='utf-8') as f:
        texto_completo = f.read()
    
    print("=== TESTE DO CÓDIGO ATUAL ===")
    print(f"Tamanho do texto: {len(texto_completo)} caracteres")
    
    # Criar instância do analisador
    analyzer = PortariaAnalyzer()
    
    # Analisar múltiplas portarias
    resultados, arquivos_excel = analyzer.analisar_multiplas_portarias(texto_completo, gerar_excel=False)
    
    print(f"\n=== RESULTADOS ===")
    print(f"Portarias encontradas: {len(resultados)}")
    
    total_pessoas = 0
    for i, resultado in enumerate(resultados, 1):
        dados = resultado['dados_portaria']
        pessoas = dados.get('pessoas', [])
        tipo = dados.get('tipo', 'DESCONHECIDO')
        numero = dados.get('numero', 'N/A')
        
        print(f"\nPortaria {i}: {numero} ({tipo})")
        print(f"  Pessoas encontradas: {len(pessoas)}")
        
        for pessoa in pessoas:
            print(f"    - {pessoa['nome']} ({pessoa['pais']}) - {pessoa['idade']} anos")
        
        total_pessoas += len(pessoas)
    
    print(f"\n=== RESUMO ===")
    print(f"Total de pessoas captadas: {total_pessoas}")
    
    # Contar manualmente as pessoas no texto
    print(f"\n=== CONTAGEM MANUAL ===")
    linhas = texto_completo.split('\n')
    pessoas_manuais = []
    
    for linha in linhas:
        # Padrão para encontrar pessoas: NOME - DOCUMENTO, natural do PAÍS
        if ' - ' in linha and 'natural' in linha and ('F' in linha or 'G' in linha or 'V' in linha or 'B' in linha):
            if not linha.startswith('PORTARIA') and not linha.startswith('A COORDENADORA'):
                pessoas_manuais.append(linha.strip())
    
    print(f"Pessoas encontradas manualmente: {len(pessoas_manuais)}")
    for pessoa in pessoas_manuais[:5]:  # Mostrar apenas as primeiras 5
        print(f"  - {pessoa}")
    if len(pessoas_manuais) > 5:
        print(f"  ... e mais {len(pessoas_manuais) - 5} pessoas")

if __name__ == "__main__":
    testar_analise_atual() 