#!/usr/bin/env python3

# Script para limpar o arquivo portaria_analyzer.py
# Remove tudo após a linha 1026 (final da classe PortariaAnalyzer)

with open('portaria_analyzer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Manter apenas as primeiras 1026 linhas (até o final da classe)
cleaned_lines = lines[:1026]

# Escrever o arquivo limpo
with open('portaria_analyzer.py', 'w', encoding='utf-8') as f:
    f.writelines(cleaned_lines)

print(f"✅ Arquivo portaria_analyzer.py limpo! Removidas {len(lines) - len(cleaned_lines)} linhas.")

# Remover este script temporário
import os
os.remove('fix_portaria_analyzer.py') 