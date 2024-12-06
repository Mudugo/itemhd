from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para armazenar os itens submetidos
submitted_items = []

# Dicionário com os valores mínimos e máximos para cada tipo de status
status_limits = {
    'ATK': (48, 72),
    'BDMG': (38, 58),
    'BRATE': (5, 7),
    'CDMG': (72, 108),
    'CRATE': (5, 7),
    'DEF': (48, 72),
    'HP': (160, 240)
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Tipos de status disponíveis
    status_types = ['ATK', 'BDMG', 'BRATE', 'CDMG', 'CRATE', 'DEF', 'HP']

    if request.method == 'POST':
        # Limpa a lista anterior ao adicionar novos itens
        submitted_items.clear()

        # Recupera os dados do formulário
        for i in range(1, 5):
            selected_status = request.form.get(f'status_type_{i}')
            value = request.form.get(f'value_{i}')
            flag = request.form.get(f'flag_{i}')

            if flag:  # Apenas adiciona se a flag estiver marcada
                try:
                    value = float(value)
                    min_val, max_val = status_limits.get(selected_status, (0, 1))
                    efficiency = ((value - min_val) / (max_val - min_val)) * 100
                    efficiency = max(0, min(100, efficiency))  # Garante que a eficiência esteja entre 0% e 100%
                    submitted_items.append({'status': selected_status, 'value': value, 'efficiency': round(efficiency, 2)})
                except ValueError:
                    pass

        return redirect(url_for('index'))

    # Calcula a porcentagem média do item apenas para os itens com a flag marcada
    if submitted_items:
        total_efficiency = sum(item['efficiency'] for item in submitted_items)
        average_efficiency = round(total_efficiency / len(submitted_items), 2)
    else:
        average_efficiency = 0

    return render_template('index.html', status_types=status_types, items=submitted_items, average_efficiency=average_efficiency)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
