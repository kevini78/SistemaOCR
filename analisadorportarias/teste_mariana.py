import pandas as pd
import re

def testar_busca_mariana():
    """Testa a busca específica por MARIANA DA CONCEICAO MATIAS NGUNZA"""
    
    try:
        # Carregar planilha
        df = pd.read_excel('historico_naturalizacoes.xlsx')
        print(f"Planilha carregada: {len(df)} registros")
        print(f"Colunas: {list(df.columns)}")
        
        # Nome para testar
        nome_teste = "MARIANA DA CONCEICAO MATIAS NGUNZA"
        
        print(f"\n🔍 Testando busca por: {nome_teste}")
        print("="*60)
        
        # 1. Busca exata
        mask_exato = df['NOME COMPLETO'].str.upper() == nome_teste
        resultados_exatos = df[mask_exato]
        
        print(f"1. Busca exata: {len(resultados_exatos)} resultados")
        if len(resultados_exatos) > 0:
            for _, row in resultados_exatos.iterrows():
                print(f"   - {row['NOME COMPLETO']} | Data: {row.get('DATA DE NASCIMENTO', 'N/A')} | Portaria: {row.get('Nº da Portaria', 'N/A')}")
        
        # 2. Busca por contém
        mask_contem = df['NOME COMPLETO'].str.upper().str.contains(nome_teste, na=False)
        resultados_contem = df[mask_contem]
        
        print(f"\n2. Busca por contém: {len(resultados_contem)} resultados")
        if len(resultados_contem) > 0:
            for _, row in resultados_contem.iterrows():
                print(f"   - {row['NOME COMPLETO']} | Data: {row.get('DATA DE NASCIMENTO', 'N/A')} | Portaria: {row.get('Nº da Portaria', 'N/A')}")
        
        # 3. Busca por palavras individuais
        palavras = nome_teste.split()
        print(f"\n3. Busca por palavras individuais: {palavras}")
        
        for palavra in palavras:
            if len(palavra) > 2:  # Ignorar palavras muito pequenas
                mask_palavra = df['NOME COMPLETO'].str.upper().str.contains(palavra, na=False)
                resultados_palavra = df[mask_palavra]
                print(f"   '{palavra}': {len(resultados_palavra)} resultados")
                
                if len(resultados_palavra) > 0 and len(resultados_palavra) <= 5:
                    for _, row in resultados_palavra.iterrows():
                        print(f"     - {row['NOME COMPLETO']}")
        
        # 4. Busca por "MARIANA"
        print(f"\n4. Busca por 'MARIANA':")
        mask_mariana = df['NOME COMPLETO'].str.upper().str.contains('MARIANA', na=False)
        resultados_mariana = df[mask_mariana]
        print(f"   Encontrados {len(resultados_mariana)} registros com 'MARIANA'")
        
        if len(resultados_mariana) > 0 and len(resultados_mariana) <= 10:
            for _, row in resultados_mariana.iterrows():
                print(f"   - {row['NOME COMPLETO']} | Data: {row.get('DATA DE NASCIMENTO', 'N/A')} | Portaria: {row.get('Nº da Portaria', 'N/A')}")
        
        # 5. Busca por "NGUNZA"
        print(f"\n5. Busca por 'NGUNZA':")
        mask_ngunza = df['NOME COMPLETO'].str.upper().str.contains('NGUNZA', na=False)
        resultados_ngunza = df[mask_ngunza]
        print(f"   Encontrados {len(resultados_ngunza)} registros com 'NGUNZA'")
        
        if len(resultados_ngunza) > 0:
            for _, row in resultados_ngunza.iterrows():
                print(f"   - {row['NOME COMPLETO']} | Data: {row.get('DATA DE NASCIMENTO', 'N/A')} | Portaria: {row.get('Nº da Portaria', 'N/A')}")
        
        # 6. Busca por "MATIAS"
        print(f"\n6. Busca por 'MATIAS':")
        mask_matias = df['NOME COMPLETO'].str.upper().str.contains('MATIAS', na=False)
        resultados_matias = df[mask_matias]
        print(f"   Encontrados {len(resultados_matias)} registros com 'MATIAS'")
        
        if len(resultados_matias) > 0 and len(resultados_matias) <= 10:
            for _, row in resultados_matias.iterrows():
                print(f"   - {row['NOME COMPLETO']} | Data: {row.get('DATA DE NASCIMENTO', 'N/A')} | Portaria: {row.get('Nº da Portaria', 'N/A')}")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_busca_mariana() 