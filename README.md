# monitoring-flask

# Monitoring and Prediction Web Application

This Flask-based web application is designed for the monitoring and prediction of various data sources, including end devices (e.g., pc, switch) and IoT devices. The application utilizes SNMP and MQTT protocols for communication, fetches data from Open Meteo API, and provides a user-friendly front-end for visualization.

## Features

- **End Device Monitoring:**
  - Utilizes SNMP protocol to monitor end devices' memory usage, CPU load, and disk space.
  
- **IoT Device Monitoring:**
  - Simulated IoT devices send ambient temperature data using MQTT and HTTP protocols.

- **Prediction:**
  - Integrates scikit-learn for predictive analysis based on historical data.

- **Front-end:**
  - Allows administrators to manage clients (CRUD operations) and visualize historical data with customizable date intervals.

- **Technologies Used:**
  - Flask for the backend
  - MQTT and SNMP for communication
  - scikit-learn for predictions
  - SQLAlchemy for database management
  - Matplotlib for data visualization

## Project Structure

The project is organized into packages, each handling specific functionalities:
- `app/templates`: Holds HTML templates organized by components.
- `app/static`: Includes static files such as CSS and JavaScript.


## Contributors

- ROUINEB Chaimae

