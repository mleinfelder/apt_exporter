from flask import Flask
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
    metrics_str = f'# HELP update_available Number of available updates\n# TYPE update_available gauge\nupdate_available {updates_count}\n'
    metrics_str += f'# HELP needs_reboot Indicates whether a system reboot is needed\n# TYPE needs_reboot gauge\nneeds_reboot {int(needs_reboot)}\n'

    # Adicione a lista de pacotes à métrica se houver atualizações
    if updates_count > 0:
        for package in updates_list:
            metrics_str += f'# HELP update_package Indicates whether the package {package} has an available update\n# TYPE update_package gauge\nupdate_package{{package="{package}"}} 1\n'

    return metrics_str

if __name__ == '__main__':
    app.run(host='::', port=9091)
