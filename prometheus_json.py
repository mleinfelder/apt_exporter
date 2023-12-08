from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    # Execute comandos para obter métricas
    updates_list = subprocess.check_output(['sudo', 'apt', 'list', '--upgradable']).decode('utf-8').strip().split('\n')[1:]
    updates_count = len(updates_list)

    # Verifique se é necessário reiniciar (apenas para sistemas baseados em Debian/Ubuntu)
    needs_reboot = subprocess.call(['checkrestart']) == 0

    # Retorne métricas no formato Prometheus
    metrics_list = [
        f'update_available {updates_count}',
        f'needs_reboot {int(needs_reboot)}'
    ]

    # Adicione a lista de pacotes à métrica se houver atualizações
    if updates_count > 0:
        for package in updates_list:
            metrics_list.append(f'update_package{{package="{package}"}} 1')

    return jsonify(metrics_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)
