from flask import Flask, render_template, request, jsonify, send_file
import os
from datetime import datetime
import tempfile
import shutil
from werkzeug.utils import secure_filename
import pandas as pd

# Importar o analisador de portarias
from portaria_analyzer import PortariaAnalyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Variável global para armazenar o analisador
analyzer = None

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/configurar', methods=['GET', 'POST'])
def configurar():
    """Página de configuração do analisador"""
    global analyzer
    message = None
    
    if request.method == 'POST':
        # Verificar se foi enviado um arquivo de histórico
        if 'arquivo' in request.files:
            arquivo = request.files['arquivo']
            if arquivo and arquivo.filename != '':
                try:
                    # Salvar arquivo de forma segura
                    filename = secure_filename(arquivo.filename)
                    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    arquivo.save(caminho_arquivo)
                    
                    # Inicializar analisador com o arquivo
                    analyzer = PortariaAnalyzer(caminho_arquivo)
                    message = f'Sucesso! Histórico carregado a partir de: {filename}'
                    
                except Exception as e:
                    message = f'Erro ao carregar o arquivo: {str(e)}'
            else:
                # Se nenhum arquivo foi selecionado, mas o formulário foi enviado
                analyzer = PortariaAnalyzer()
                message = 'Aviso: Nenhum arquivo de histórico selecionado. O analisador usará apenas as regras padrão.'
        else:
            # Caso o formulário seja postado sem o campo 'arquivo'
            analyzer = PortariaAnalyzer()
            message = 'Aviso: Analisador configurado sem arquivo de histórico.'

        return render_template('configurar.html', message=message)
    
    # Se for GET, apenas renderiza a página
    return render_template('configurar.html', message=None)

@app.route('/analisar', methods=['GET', 'POST'])
def analisar():
    """Página de análise de portarias"""
    global analyzer
    
    if request.method == 'POST':
        if analyzer is None:
            return jsonify({
                'success': False,
                'message': 'Analisador não configurado. Configure primeiro!'
            })
        
        # Obter dados do formulário
        tipo_analise = request.form.get('tipo_analise')
        
        if tipo_analise == 'url':
            url_portaria = request.form.get('url_portaria')
            if not url_portaria:
                return jsonify({
                    'success': False,
                    'message': 'URL da portaria é obrigatória'
                })
            
            try:
                resultado = analyzer.analisar_portaria(url_portaria, gerar_excel=False)
                
                if 'erro' in resultado:
                    return jsonify({
                        'success': False,
                        'message': resultado['erro']
                    })
                
                # Preparar resultado para JSON (similar ao texto)
                resultado_json = {
                    'total_portarias': resultado['total_portarias'],
                    'total_erros': resultado['total_erros'],
                    'portarias': []
                }
                
                for res in resultado['resultados']:
                    if res['dados_portaria']:
                        portaria_info = {
                            'numero': res['dados_portaria']['numero'],
                            'data': res['dados_portaria']['data'],
                            'tipo': res['dados_portaria']['tipo'],
                            'total_pessoas': len(res['dados_portaria']['pessoas']),
                            'erros': res['erros'],
                            'pessoas': res['dados_portaria']['pessoas']
                        }
                        resultado_json['portarias'].append(portaria_info)
                
                return jsonify({
                    'success': True,
                    'resultado': resultado_json
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro ao analisar portaria: {str(e)}'
                })
        
        elif tipo_analise == 'texto':
            texto_portaria = request.form.get('texto_portaria')
            if not texto_portaria:
                return jsonify({
                    'success': False,
                    'message': 'Texto da portaria é obrigatório'
                })
            
            # Salvar o texto recebido em um arquivo para debug
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"debug_texto_recebido_{timestamp}.txt"
            
            with open(log_filename, 'w', encoding='utf-8') as f:
                f.write("=== TEXTO RECEBIDO DO FORMULARIO ===\n")
                f.write(texto_portaria)
                f.write("\n=== FIM DO TEXTO ===\n")
            
            print(f"Texto salvo em: {log_filename}")
            
            try:
                resultados, arquivos_excel = analyzer.analisar_multiplas_portarias(texto_portaria, gerar_excel=True)
                
                # Preparar resultado para JSON
                resultado_json = {
                    'total_portarias': len(resultados),
                    'total_erros': sum(r['total_erros'] for r in resultados),
                    'portarias': []
                }
                
                for res in resultados:
                    if res['dados_portaria']:
                        portaria_info = {
                            'numero': res['dados_portaria']['numero'],
                            'data': res['dados_portaria']['data'],
                            'tipo': res['dados_portaria']['tipo'],
                            'total_pessoas': len(res['dados_portaria']['pessoas']),
                            'erros': res['erros'],
                            'pessoas': res['dados_portaria']['pessoas']
                        }
                        resultado_json['portarias'].append(portaria_info)
                
                # Salvar arquivo Excel em pasta temporária
                if arquivos_excel:
                    temp_dir = tempfile.mkdtemp()
                    for arquivo in arquivos_excel:
                        if os.path.exists(arquivo):
                            shutil.copy2(arquivo, temp_dir)
                            os.remove(arquivo)  # Remover arquivo original
                    
                    resultado_json['arquivos_excel'] = [os.path.join(temp_dir, os.path.basename(f)) for f in arquivos_excel]
                
                return jsonify({
                    'success': True,
                    'resultado': resultado_json
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro ao analisar texto: {str(e)}'
                })
    
    return render_template('analisar.html')

@app.route('/download/<filename>')
def download_file(filename):
    """Download de arquivos Excel gerados"""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao baixar arquivo: {str(e)}'
        })

@app.route('/status')
def status():
    """Verificar status do analisador"""
    global analyzer
    return jsonify({
        'configurado': analyzer is not None,
        'tem_historico': analyzer.historico_df is not None if analyzer else False
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 