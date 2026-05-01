"""
Configuration file for DDoS Detection System
"""
import os

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Model paths
    MODEL_DIR = 'models'
    RF_MODEL_PATH = os.path.join(MODEL_DIR, 'random_forest_model.pkl')
    LSTM_MODEL_PATH = os.path.join(MODEL_DIR, 'lstm_model.h5')
    SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
    LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.pkl')
    FEATURES_PATH = os.path.join(MODEL_DIR, 'rf_features.pkl')
    
    # Model parameters
    RF_ACCURACY = 98.29
    LSTM_ACCURACY = 97.30
    
    # Feature information
    FEATURE_DESCRIPTIONS = {
        'protocol': 'Network protocol (6=TCP, 17=UDP)',
        'fwd_seg_size_min': 'Minimum forward segment size',
        'src_port': 'Source port number',
        'fin_flag_cnt': 'Number of FIN flags',
        'init_fwd_win_byts': 'Initial forward window bytes'
    }
    
    # Prediction settings
    CONFIDENCE_THRESHOLD = 0.5
    HIGH_CONFIDENCE_THRESHOLD = 0.8
    
    # Logging
    LOG_FILE = 'app.log'
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}