from flask import Flask, render_template, request, redirect, url_for, send_file, session, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import json
import io
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Counter logic
COUNTER_FILE = 'user_count.txt'

def get_user_count():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def increment_user_count():
    count = get_user_count() + 1
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(count))
    return count

@app.route('/')
def index():
    count = get_user_count()
    theme = session.get('theme', 'dark')
    return render_template('index.html', theme=theme, user_count=count)

@app.route('/toggle_theme', methods=['GET', 'POST'])
def toggle_theme():
    try:
        session['theme'] = 'light' if session.get('theme') == 'dark' else 'dark'
        return redirect(request.referrer or '/')
    except Exception as e:
        print(f"Toggle error: {e}")
        return redirect('/')

@app.route('/analyze', methods=['POST'])
def analyze():
    revenues = list(map(float, request.form.getlist('revenue')))
    costs = list(map(float, request.form.getlist('cost')))
    periods = list(range(1, len(revenues) + 1))
    
    profits = [r - c for r, c in zip(revenues, costs)]
    
    # Forecasting
    model = LinearRegression()
    model.fit(np.array(periods).reshape(-1, 1), profits)
    future_periods = np.array([len(periods) + i for i in range(1, 6)]).reshape(-1, 1)
    future_profits = model.predict(future_periods)
    
    # Anomaly detection
    anomalies = [i+1 for i in range(1, len(profits)) if profits[i] < profits[i-1] * 0.8]
    
    summary = {
        'total_profit': sum(profits),
        'avg_profit': np.mean(profits),
        'avg_revenue': np.mean(revenues),
        'avg_cost': np.mean(costs)
    }
    
    tips = []
    if summary['total_profit'] < 0:
        tips.append("Reduce costs to turn losses into profits.")
    if anomalies:
        tips.append(f"Investigate profit drops in periods: {', '.join(map(str, anomalies))}")
    tips.extend(["Boost sales with marketing.", "Diversify for stability."])
    
    # Fun facts and badges
    fun_facts = [
        "Did you know? Your highest profit period was " + str(profits.index(max(profits)) + 1) + ".",
        "Fun fact: Profits increased by " + str(round((profits[-1] - profits[0]) / profits[0] * 100, 2)) + "% overall."
    ]
    badges = []
    if summary['total_profit'] > 1000:
        badges.append("Profit Master")
    if len(profits) > 5:
        badges.append("Data Guru")
    
    # Mastery level
    mastery_level = min(100, int((summary['total_profit'] / 2000) * 100))
    
    data = {
        'periods': periods,
        'profits': profits,
        'revenues': revenues,
        'costs': costs,
        'future_periods': future_periods.flatten().tolist(),
        'future_profits': future_profits.tolist(),
        'anomalies': anomalies,
        'summary': summary,
        'tips': tips,
        'fun_facts': random.choice(fun_facts),
        'badges': badges,
        'mastery_level': mastery_level
    }
    
    # Store data in session for export
    session['analysis_data'] = data
    
    # Increment counter on analysis
    increment_user_count()
    
    theme = session.get('theme', 'dark')
    return render_template('results.html', data=data, theme=theme)

@app.route('/predict_score', methods=['POST'])
def predict_score():
    data = request.get_json()
    actual = data['actual']
    guess = data['guess']
    score = max(0, 100 - abs(actual - guess) / actual * 100) if actual != 0 else 100
    return jsonify({'score': round(score, 2)})

@app.route('/fortune_teller', methods=['GET'])
def fortune_teller():
    fortunes = [
        "Your profits will skyrocket like a rocket in the next quarter!",
        "Beware of unexpected costs—diversify to stay safe.",
        "A golden opportunity awaits in digital marketing."
    ]
    return jsonify({'fortune': random.choice(fortunes)})

@app.route('/demo_mode', methods=['GET'])
def demo_mode():
    demo_data = {
        'revenues': [1000, 1200, 1100, 1300, 1400],
        'costs': [800, 1300, 850, 1400, 1000]  # Includes losses
    }
    return jsonify(demo_data)

@app.route('/export_csv')
def export_csv():
    # Retrieve data from session
    data = session.get('analysis_data')
    if not data:
        # Fallback to sample data if no session data
        periods = [1, 2, 3, 4, 5]
        revenues = [1000, 1200, 1100, 1300, 1400]
        costs = [800, 1300, 850, 1400, 1000]
        profits = [r - c for r, c in zip(revenues, costs)]
    else:
        periods = data['periods']
        revenues = data['revenues']
        costs = data['costs']
        profits = data['profits']
    
    csv_data = "Period,Revenue,Cost,Profit,Loss\n"
    for i, p in enumerate(periods):
        profit_value = profits[i] if profits[i] >= 0 else 0
        loss_value = abs(profits[i]) if profits[i] < 0 else 0
        csv_data += f"{p},{revenues[i]},{costs[i]},{profit_value},{loss_value}\n"
    
    return send_file(io.BytesIO(csv_data.encode()), mimetype='text/csv', as_attachment=True, download_name='profit_data.csv')

@app.route('/tips')
def tips():
    theme = session.get('theme', 'dark')
    return render_template('tips.html', theme=theme)

@app.route('/donate')
def donate():
    theme = session.get('theme', 'dark')
    return render_template('donate.html', theme=theme)

app = Flask(__name__)

