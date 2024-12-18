# Solar Energy Prediction Web Application

## Overview
This project aims to predict solar energy generation using machine learning models. The web application allows users to input geographical coordinates and select a model to forecast solar power output. The predictions are supported by weather data and presented alongside visualizations, including a heatmap for Delhi to represent solar potential.

---

## Features
- **Dual Model Support**:
  - **Prophet Model**: Time series forecasting with non-linear trends, seasonality, and external regressors.
  - **Random Forest Regressor (RFR)**: Ensemble model for non-linear relationships and feature importance analysis.
- **Interactive Web Interface**:
  - Input latitude and longitude for predictions.
  - Dropdown to select the desired machine learning model.
  - Display predictions and visualizations.
- **Heatmap Visualization**:
  - Heatmap for Delhi showcasing solar potential based on historical data.

---

## Models

### Prophet Model
- Developed by Facebook for time series forecasting.
- Captures non-linear trends, seasonality, and holiday effects.
- Customization:
  - Hourly and daily seasonality added.
  - Weather variables such as temperature and cloud coverage used as regressors.
- **Performance**:
  - RMSE: 0.45
  - Normalized RMSE: ~36%

### Random Forest Regressor
- Ensemble model using multiple decision trees.
- Key Features:
  - Feature importance analysis for selecting top variables.
  - Hyperparameter tuning with Optuna.
- **Performance**:
  - RMSE: 0.19
  - Normalized RMSE: ~21.8%

---

## Data Preprocessing
- **Scaling Techniques**:
  - Min-Max Scaling: For features like cloud coverage and relative humidity.
  - Standard Scaling: For normally distributed features like temperature and wind speed.
  - Log1+ Scaling: For features like Energy generated & its lag features.
- **Feature Engineering**:
  - Lag features for solar energy and weather variables.
  - Cyclical transformations (sine and cosine) for time features.

---

## Web Application
- Built using **Django Framework**.
- **Functionalities**:
  - Enter coordinates and select the model via a dropdown.
  - Real-time weather data retrieval using OpenWeatherMap API.
  - Display predictions and heatmap visualizations.

---

## Heatmap
- **Region**: Delhi
- **Purpose**: Visual representation of solar energy potential.
- **Technology**: Heatmap generated using historical solar data and geographical coordinates.

---

## How to Run

### Prerequisites
- Python 3.8+
- Django 4.x
- Required libraries: `joblib`, `pandas`, `numpy`, `scikit-learn`, `fbprophet`, `matplotlib`

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/solar-energy-prediction.git
   ```
2. Navigate to the project directory:
   ```bash
   cd solar-energy-prediction
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the Django server:
   ```bash
   python manage.py runserver
   ```
5. Access the web app:
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Project Structure
```
solar-energy-prediction/
│
├── power_app/                   # Django application
│   ├── templates/              # HTML templates
│   ├── static/                 # CSS, JS, images
│   ├── views.py                # Application logic
│   ├── urls.py                 # URL routing
│   └── ...
│
├── model_data/                 # Pretrained models and scalers
│   ├── min_max_scaler.joblib
│   ├── standard_scaler.joblib
│   ├── prophet_model.joblib
│   ├── rfr_model.joblib
│
├── requirements.txt            # Required Python libraries
├── manage.py                   # Django management script
└── README.md                   # Project documentation
```

---

## Contributions
Contributions are welcome! Feel free to submit a pull request or report issues.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author
**Mohak Kapoor**
- [GitHub](https://github.com/mohakapoor)
- [LinkedIn](https://www.linkedin.com/in/mohak-kapoor-24383828a/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

---
