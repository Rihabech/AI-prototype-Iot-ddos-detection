# 🛡️ DDoS Attack Detection System

Detecting Distributed Denial of Service (DDoS) attacks using Machine Learning. The system employs both Random Forest and LSTM Neural Network models for accurate traffic classification.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange.svg)


## 🌟 Features

- **Dual Model Architecture**: Utilizes both Random Forest and LSTM models for robust predictions
- **Real-time Analysis**: Instant classification of network traffic patterns
- **Interactive Visualizations**: 
  - Model comparison charts
  - Confidence gauge meters
  - Feature radar charts
  - Probability distribution plots
- **User-Friendly Interface**: Modern, responsive web interface with gradient design
- **High Accuracy**: 
  - Random Forest: 98.29% accuracy
  - LSTM Network: 97.30% accuracy
- **Quick Fill Examples**: Pre-loaded DDoS and Normal traffic examples for testing

## 📊 Model Performance

| Model | Accuracy | Parameters | Training Time |
|-------|----------|------------|---------------|
| Random Forest | 98.29% | 20 trees, depth 4 | 0.15s |
| LSTM Network | 97.30% | 3,193 params | 10.67s |

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download
```bash
# Navigate to your project directory
cd ddos-detection-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Model Files
Ensure all model files are in the `models/` directory:
```
models/
├── random_forest_model.pkl
├── lstm_model.h5
├── scaler.pkl
├── label_encoder.pkl
└── rf_features.pkl
```

## 🎯 Usage

### Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser and navigate to:**
```
http://localhost:5000
```

3. **Using the Interface:**
   - **Quick Fill**: Use "Load DDoS Example" or "Load Normal Example" buttons
   - **Manual Input**: Enter network feature values manually
   - **Model Selection**: Choose between Both Models, Random Forest, or LSTM
   - **Analyze**: Click "Analyze Traffic" to get predictions

## 📋 Input Features

The system analyzes 5 key network features:

1. **Protocol**: Network protocol (6=TCP, 17=UDP)
2. **Forward Segment Size Min**: Minimum forward segment size
3. **Source Port**: Source port number
4. **FIN Flag Count**: Number of FIN flags
5. **Initial Forward Window Bytes**: Initial forward window size

## 📁 Project Structure

```
ddos-detection-system/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── models/                     # Trained model files
│   ├── random_forest_model.pkl
│   ├── lstm_model.h5
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── rf_features.pkl
│
└── templates/                  # HTML templates
    └── index.html
```

## 🔧 API Endpoints

### 1. Home Page
- **URL**: `/`
- **Method**: GET
- **Description**: Renders the main interface

### 2. Predict
- **URL**: `/predict`
- **Method**: POST
- **Content-Type**: application/json
- **Body**:
```json
{
  "model_type": "both",
  "protocol": 6,
  "fwd_seg_size_min": 20,
  "src_port": 16389,
  "fin_flag_cnt": 1,
  "init_fwd_win_byts": 64
}
```
- **Response**:
```json
{
  "random_forest": {
    "prediction": "DDos Attack",
    "confidence": 98.5,
    "probabilities": {
      "DDos Attack": 98.5,
      "Normal": 1.5
    }
  },
  "lstm": { ... },
  "charts": { ... }
}
```

### 3. Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: `{"status": "healthy", "models_loaded": true}`

## 🎨 Visualizations

The system provides four interactive Plotly visualizations:

1. **Model Comparison**: Side-by-side probability comparison
2. **Confidence Gauge**: Visual confidence meter (0-100%)
3. **Feature Radar**: Normalized input feature values
4. **Probability Distribution**: Pie chart of class probabilities

## 🔬 Technical Details

### Random Forest Model
- **Trees**: 20
- **Max Depth**: 4
- **Min Samples Split**: 50
- **Min Samples Leaf**: 20
- **Max Features**: 3

### LSTM Model Architecture
```
Layer (type)                Output Shape              Param #
=================================================================
LSTM                        (None, 24)                2,880
Dropout (0.4)               (None, 24)                0
Dense                       (None, 12)                300
Dropout (0.3)               (None, 12)                0
Dense (sigmoid)             (None, 1)                 13
=================================================================
Total params: 3,193
```

## 🐛 Troubleshooting

### Issue: Models not loading
```bash
# Verify model files exist
ls -la models/
```

### Issue: Port already in use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: TensorFlow warnings
```python
# Add to app.py
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
```

## 📈 Future Enhancements

- [ ] Real-time packet capture integration
- [ ] Multi-class attack type detection
- [ ] Model retraining pipeline
- [ ] Alert notification system

