from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'caramelo'  # Use uma chave secreta para sessões

# Limites para os valores dos status
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
    status_types = ['ATK', 'BDMG', 'BRATE', 'CDMG', 'CRATE', 'DEF', 'HP']

    # Inicializa a lista de itens na sessão, se não existir
    if 'submitted_items' not in session:
        session['submitted_items'] = []

    if request.method == 'POST':
        session['submitted_items'].clear()  # Limpa os itens enviados

        for i in range(1, 5):
            selected_status = request.form.get(f'status_type_{i}')
            value = request.form.get(f'value_{i}')
            flag = request.form.get(f'flag_{i}')

            if flag:
                try:
                    value = float(value)
                    min_val, max_val = status_limits.get(selected_status, (0, 1))
                    efficiency = ((value - min_val) / (max_val - min_val)) * 100
                    efficiency = max(0, min(100, efficiency))
                    session['submitted_items'].append({'status': selected_status, 'value': value, 'efficiency': round(efficiency, 2)})
                except ValueError:
                    pass

        session.modified = True  # Marca a sessão como modificada para garantir que seja salva
        return redirect(url_for('index'))

    if session['submitted_items']:
        total_efficiency = sum(item['efficiency'] for item in session['submitted_items'])
        average_efficiency = round(total_efficiency / len(session['submitted_items']), 2)
    else:
        average_efficiency = 0

    return render_template('index.html', status_types=status_types, items=session['submitted_items'], average_efficiency=average_efficiency)

if __name__ == '__main__':
    app.run(debug=True)
