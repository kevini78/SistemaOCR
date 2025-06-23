import pandas as pd

try:
    df = pd.read_excel('historico_naturalizacoes.xlsx')
    print("Colunas da planilha:")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    print(f"\nTotal de linhas: {len(df)}")
    print(f"Total de colunas: {len(df.columns)}")
    
    print("\nPrimeiras 3 linhas:")
    print(df.head(3))
    
    # Verificar se há dados de exemplo
    if 'NOME COMPLETO' in df.columns:
        print(f"\nExemplos de nomes:")
        print(df['NOME COMPLETO'].head(5).tolist())
    
    if 'DATA DE NASCIMENTO' in df.columns:
        print(f"\nExemplos de datas:")
        print(df['DATA DE NASCIMENTO'].head(5).tolist())
        
except Exception as e:
    print(f"Erro: {e}") 