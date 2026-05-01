#!/usr/bin/env python
"""
DDoS Detection System - Application Starter
"""
import os
import sys

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'flask', 'numpy', 'tensorflow', 
        'sklearn', 'joblib', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\nPlease install them using:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print("✓ All required packages are installed")

def check_model_files():
    """Check if all model files exist"""
    model_files = [
        'models/random_forest_model.pkl',
        'models/lstm_model.h5',
        'models/scaler.pkl',
        'models/label_encoder.pkl',
        'models/rf_features.pkl'
    ]
    
    missing_files = []
    
    for file in model_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required model files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all model files are in the 'models/' directory")
        sys.exit(1)
    
    print("✓ All model files found")

def check_templates():
    """Check if template files exist"""
    if not os.path.exists('templates/index.html'):
        print("❌ Missing template file: templates/index.html")
        sys.exit(1)
    
    print("✓ Template files found")

def main():
    """Main function to start the application"""
    print("="*70)
    print("DDoS ATTACK DETECTION SYSTEM")
    print("="*70)
    print("\nPerforming pre-flight checks...\n")
    
    # Run checks
    check_requirements()
    check_model_files()
    check_templates()
    
    print("\n" + "="*70)
    print("Starting Flask application...")
    print("="*70)
    print("\n🚀 Server will start at: http://localhost:5000")
    print("📊 Press CTRL+C to stop the server\n")
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()