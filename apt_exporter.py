from flask import Flask, jsonify
import subprocess
import os
import schedule
import time

app = Flask(__name__)

def update_metrics():
    # Execute comandos para obter métricas
    updates_list = subprocess.check_output(['sudo', 'apt', 'list', '--upgradable']).decode('utf-8').strip().split('\n')[1:]
    updates_count = len(updates_list)

    # Verifique se é necessário reiniciar (apenas para sistemas baseados em Debian/Ubuntu)
    reboot_required = os.path.isfile('/var/run/reboot-required')
    
    # Determina se o reboot é necessário
    needs_reboot = 1 if reboot_required else 0

    # Retorne métricas no formato Prometheus
    metrics_str = f'# HELP update_package Number of available updates\n# TYPE update_package gauge\nupdate_package {updates_count}\n'
    metrics_str += f'# HELP needs_reboot Indicates whether a system reboot is needed\n# TYPE needs_reboot gauge\nneeds_reboot {needs_reboot}\n'

    # Adicione a lista de pacotes à métrica se houver atualizações
    if updates_count > 0:
        for package in updates_list:
            metrics_str += f'# HELP update_package Indicates whether the package {package} has an available update\n# TYPE update_package gauge\nupdate_package{{package="{package}"}} 1\n'

    return metrics_str

def job():
    # Atualiza as métricas em intervalos regulares
    metrics = update_metrics()
    with open('metrics.prom', 'w') as f:
        f.write(metrics)

# Agende a verificação de atualizações a cada 1 hora (ajuste conforme necessário)
schedule.every(1).hour.do(job)

# Execute a verificação inicial
job()

# Agora, inicie o servidor Flask
@app.route('/metrics')
def metrics():
    # Leitura do arquivo gerado pela última verificação
    with open('metrics.prom', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run(host='::', port=3999)

# Mantenha o script em execução para permitir a execução agendada
while True:
    schedule.run_pending()
    time.sleep(1)
