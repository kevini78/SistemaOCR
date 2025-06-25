#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplo prático: Busca de portarias de naturalização de 2018-2025
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from busca_automatica_dou import BuscadorAutomaticoDOU
from datetime import datetime

def buscar_naturalizacoes_2018_2025():
    """Busca portarias de naturalização de 2018 a 2025"""
    print("🔍 BUSCA DE NATURALIZAÇÕES 2018-2025")
    print("=" * 60)
    print("Baseado no Ro-DOU (https://github.com/gestaogovbr/Ro-dou)")
    print()
    
    # Inicializar buscador
    print("🚀 Inicializando buscador automático...")
    buscador = BuscadorAutomaticoDOU()
    
    # Definir período
    data_inicio = "2018-01-01"
    data_fim = "2025-12-31"
    
    print(f"📅 Período de busca: {data_inicio} a {data_fim}")
    print(f"🎯 Objetivo: Encontrar todas as portarias de naturalização")
    print()
    
    try:
        # Realizar busca
        print("🔍 Iniciando busca automática...")
        print("⏳ Isso pode demorar alguns minutos...")
        print()
        
        arquivo = buscador.gerar_planilha_periodo(
            data_inicio=data_inicio,
            data_fim=data_fim,
            nome_arquivo="naturalizacoes_2018_2025.xlsx"
        )
        
        if arquivo and os.path.exists(arquivo):
            print("✅ Busca concluída com sucesso!")
            print(f"📊 Arquivo gerado: {arquivo}")
            
            # Ler estatísticas
            import pandas as pd
            df = pd.read_excel(arquivo)
            
            print(f"👥 Total de pessoas naturalizadas: {len(df)}")
            print(f"📋 Total de portarias processadas: {df['numero_portaria'].nunique()}")
            
            if not df.empty:
                print("\n📈 Estatísticas:")
                print(f"   • Período com mais naturalizações: {df['data_portaria'].value_counts().head(1).index[0]}")
                print(f"   • País mais comum: {df['pais'].value_counts().head(1).index[0]}")
                print(f"   • Estado com mais naturalizações: {df['estado'].value_counts().head(1).index[0]}")
                
                print("\n📋 Amostra dos dados:")
                print(df.head(3)[['nome', 'pais', 'estado', 'data_portaria']].to_string())
            
            print(f"\n💾 Arquivo salvo em: {os.path.abspath(arquivo)}")
            print("🎉 Processo concluído!")
            
        else:
            print("❌ Nenhuma portaria foi encontrada no período especificado")
            print("💡 Dicas:")
            print("   • Verifique se o período está correto")
            print("   • Tente um período menor (ex: 2024-2025)")
            print("   • Verifique sua conexão com a internet")
            
    except Exception as e:
        print(f"❌ Erro durante a busca: {e}")
        print("💡 Verifique:")
        print("   • Sua conexão com a internet")
        print("   • Se a API do Querido Diário está disponível")
        print("   • Se todas as dependências estão instaladas")

def buscar_por_ano(ano):
    """Busca portarias de um ano específico"""
    print(f"🔍 BUSCA DE NATURALIZAÇÕES - ANO {ano}")
    print("=" * 50)
    
    buscador = BuscadorAutomaticoDOU()
    
    data_inicio = f"{ano}-01-01"
    data_fim = f"{ano}-12-31"
    
    print(f"📅 Período: {data_inicio} a {data_fim}")
    
    try:
        arquivo = buscador.gerar_planilha_periodo(
            data_inicio=data_inicio,
            data_fim=data_fim,
            nome_arquivo=f"naturalizacoes_{ano}.xlsx"
        )
        
        if arquivo and os.path.exists(arquivo):
            import pandas as pd
            df = pd.read_excel(arquivo)
            print(f"✅ {len(df)} pessoas naturalizadas em {ano}")
            return arquivo
        else:
            print(f"❌ Nenhuma portaria encontrada em {ano}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    print("🎯 EXEMPLO PRÁTICO: BUSCA AUTOMÁTICA DOU")
    print("=" * 60)
    print("Este script demonstra como buscar portarias de naturalização")
    print("de 2018 a 2025 usando o sistema baseado no Ro-DOU")
    print()
    
    # Opção 1: Busca completa 2018-2025
    print("1️⃣ Busca completa 2018-2025")
    buscar_naturalizacoes_2018_2025()
    
    print("\n" + "="*60 + "\n")
    
    # Opção 2: Busca por ano (exemplo com 2024)
    print("2️⃣ Busca por ano específico (2024)")
    buscar_por_ano(2024)
    
    print("\n✅ Exemplo concluído!")
    print("\n💡 Para usar no sistema web:")
    print("   1. Acesse http://localhost:5000/busca_automatica")
    print("   2. Defina o período desejado")
    print("   3. Clique em 'Iniciar Busca Automática'") 