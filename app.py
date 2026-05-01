from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import pickle
from tensorflow.keras.models import load_model
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)

# Load models and preprocessing objects
print("Loading models...")
try:
    rf_model = joblib.load('models/random_forest_model.pkl')
    lstm_model = load_model('models/lstm_model.h5')
    scaler = joblib.load('models/scaler.pkl')
    label_encoder = joblib.load('models/label_encoder.pkl')
    
    with open('models/rf_features.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    print("✓ All models loaded successfully!")
    print(f"✓ Features: {feature_names}")
except Exception as e:
    print(f"Error loading models: {e}")
    raise

@app.route('/')
def home():
    return render_template('index.html', features=feature_names)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data
        data = request.get_json()
        model_type = data.get('model_type', 'both')
        
        # Extract features in correct order
        features = []
        for feature in feature_names:
            value = float(data.get(feature, 0))
            features.append(value)
        
        features_array = np.array(features).reshape(1, -1)
        
        results = {}
        
        # Random Forest Prediction
        if model_type in ['rf', 'both']:
            rf_pred = rf_model.predict(features_array)[0]
            rf_proba = rf_model.predict_proba(features_array)[0]
            results['random_forest'] = {
                'prediction': label_encoder.inverse_transform([rf_pred])[0],
                'confidence': float(max(rf_proba) * 100),
                'probabilities': {
                    label_encoder.classes_[0]: float(rf_proba[0] * 100),
                    label_encoder.classes_[1]: float(rf_proba[1] * 100)
                }
            }
        
        # LSTM Prediction
        if model_type in ['lstm', 'both']:
            features_scaled = scaler.transform(features_array)
            features_reshaped = features_scaled.reshape((1, 1, len(feature_names)))
            lstm_pred_proba = lstm_model.predict(features_reshaped, verbose=0)[0][0]
            lstm_pred = 1 if lstm_pred_proba > 0.5 else 0
            
            results['lstm'] = {
                'prediction': label_encoder.inverse_transform([lstm_pred])[0],
                'confidence': float(max(lstm_pred_proba, 1-lstm_pred_proba) * 100),
                'probabilities': {
                    label_encoder.classes_[0]: float((1 - lstm_pred_proba) * 100),
                    label_encoder.classes_[1]: float(lstm_pred_proba * 100)
                }
            }
        
        # Generate visualizations
        charts = generate_charts(results, features_array[0])
        results['charts'] = charts
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def generate_charts(results, features):
    charts = {}
    
    # 1. Model Comparison Chart
    if 'random_forest' in results and 'lstm' in results:
        fig = go.Figure(data=[
            go.Bar(name='Random Forest', 
                   x=['DDoS Attack', 'Normal'], 
                   y=[results['random_forest']['probabilities']['DDos Attack'],
                      results['random_forest']['probabilities']['Normal']],
                   marker_color='#e74c3c',
                   text=[f"{results['random_forest']['probabilities']['DDos Attack']:.1f}%",
                         f"{results['random_forest']['probabilities']['Normal']:.1f}%"],
                   textposition='auto'),
            go.Bar(name='LSTM', 
                   x=['DDoS Attack', 'Normal'], 
                   y=[results['lstm']['probabilities']['DDos Attack'],
                      results['lstm']['probabilities']['Normal']],
                   marker_color='#3498db',
                   text=[f"{results['lstm']['probabilities']['DDos Attack']:.1f}%",
                         f"{results['lstm']['probabilities']['Normal']:.1f}%"],
                   textposition='auto')
        ])
        fig.update_layout(
            title='Model Predictions Comparison',
            xaxis_title='Traffic Type',
            yaxis_title='Probability (%)',
            barmode='group',
            height=400,
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        charts['comparison'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 2. Confidence Gauge Chart
    model_key = 'random_forest' if 'random_forest' in results else 'lstm'
    confidence = results[model_key]['confidence']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{model_key.replace('_', ' ').title()} Confidence", 'font': {'size': 20}},
        delta={'reference': 90, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2ecc71" if confidence > 80 else "#f39c12" if confidence > 50 else "#e74c3c"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffcccc'},
                {'range': [50, 80], 'color': '#fff4cc'},
                {'range': [80, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        height=400,
        font={'size': 14},
        paper_bgcolor='rgba(0,0,0,0)'
    )
    charts['confidence'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 3. Feature Values Radar Chart
    # Normalize features for better visualization
    features_normalized = (features - np.min(features)) / (np.max(features) - np.min(features) + 1e-10) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=features_normalized,
        theta=feature_names,
        fill='toself',
        name='Input Features',
        line_color='#9b59b6',
        fillcolor='rgba(155, 89, 182, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title='Input Feature Values (Normalized)',
        height=400,
        font=dict(size=12),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    charts['features'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 4. Probability Distribution Pie Chart
    model_key = 'random_forest' if 'random_forest' in results else 'lstm'
    probs = results[model_key]['probabilities']
    
    fig = go.Figure(data=[go.Pie(
        labels=list(probs.keys()),
        values=list(probs.values()),
        hole=.4,
        marker_colors=['#e74c3c', '#2ecc71'],
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig.update_layout(
        title=f'{model_key.replace("_", " ").title()} Probability Distribution',
        height=400,
        font=dict(size=12),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    charts['probability'] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'models_loaded': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)