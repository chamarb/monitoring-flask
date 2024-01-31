from flask import (
    Flask,
    send_file,
    redirect,
    render_template
)
from dal import IotDao
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO
from flask_mqtt import Mqtt
from services import perform_prediction
from models import db
from dal import Database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@db:3306/db_hosts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

matplotlib.use('agg')

app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'
app.config['MQTT_BROKER_PORT'] = 1883
from flask_mqtt import Mqtt

mqtt = Mqtt(app)

MQTT_TOPIC = 'iot/temperature'

@mqtt.on_connect()
def hand_connect(client, userData, flags, rc):
    if rc == 0:
        print('Connection ok')
        mqtt.subscribe(MQTT_TOPIC)
    else:
        print('Connection refused')

@mqtt.on_message()
def hand_message(client, userData, message):
    if message.topic == MQTT_TOPIC:
        print(message.payload.decode())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize')
def visualise():
    figure=plt.figure()
    data=IotDao.getAllTemp()
    temp=[]
    dates=[]
    for id,mac,t,date in data:
        temp.append(t)
        dates.append(date)
    plt.plot(dates,temp)
    img=BytesIO()
    figure.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='image/png')


# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if username == 'admin' and password == 'password':
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'new_user':
            # Registration successful
            return redirect(url_for('admin_dashboard'))
        else:
            # Registration failed
            return render_template('register.html', error='Registration failed. Please try again.')

    return render_template('register.html')

# Prediction Routes


import requests
import json

import requests

@app.route('/prediction/<location>')
def predict(location):
    openweathermap_api_key = 'bd5e378503939ddaee76f12ad7a97608'
    prediction_results = perform_prediction(location, openweathermap_api_key)
    return render_template('prediction.html', city_name=location, prediction_results=prediction_results)
    



@app.route('/admin/dashboard')
def admin_dashboard():
    # Fetch list of end devices and IoT devices
    end_devices = IotDao.getAllEndDevices()
    iot_devices = IotDao.getAllIoTData()

    return render_template('admin_dashboard.html', end_devices=end_devices, iot_devices=iot_devices)

@app.route('/client/details/<int:client_id>')
def client_details(client_id):
    # Fetch details for the specified client_id
    client_details = IotDao.getClientDetails(client_id)
    iot_entries = IotDao.getIoTDataForClient(client_id)

    return render_template('client_details.html', client=client_details, iot_entries=iot_entries)

@app.route('/client/list')
def list_clients():
    # Fetch a list of all clients
    clients = IotDao.getAllClients()
    iot_entries = IotDao.getAllIoTData()

    return render_template('list_client.html', clients=clients, iot_entries=iot_entries)

from flask import request, redirect, url_for

@app.route('/client/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        # Collect information from the form
        name = request.form['name']
        ip_address = request.form['ip']
        mac_address = request.form['mac']
        longitude = request.form['longitude']
        latitude = request.form['latitude']

        # Add the end device to the database
        IotDao.addEndDevice(name, ip_address, mac_address, longitude, latitude)

        # Redirect to the list of clients after adding
        return redirect(url_for('list_clients'))

    return render_template('add_client.html')

@app.route('/client/update/<int:client_id>', methods=['GET', 'POST'])
def update_client(client_id):
    # Fetch details for the specified client_id
    client_details = IotDao.getClientDetails(client_id)

    if request.method == 'POST':
        # Collect information from the form
        updated_data = {
            'name': request.form.get('updated_name'),
            'ip_address': request.form.get('updated_ip'),
            'mac_address': request.form.get('updated_mac'),
            'longitude': request.form.get('updated_longitude'),
            'latitude': request.form.get('updated_latitude')
        }

        # Update client information based on the form data
        IotDao.updateClient(client_id, updated_data)  

        # Redirect to client details page
        return redirect(url_for('client_details', client_id=client_id))

    return render_template('update_client.html', client=client_details)

@app.route('/client/delete/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    # Delete the specified client
    IotDao.deleteClient(client_id)

    # Redirect or respond as needed
    return redirect(url_for('list_clients'))

@app.route('/admin/list_end_devices')
def list_end_devices():
    # Fetch list of end devices
    end_devices = IotDao.getAllEndDevices()

    return render_template('list_end_devices.html', end_devices=end_devices)
####################################################################
from services import get

@app.route('/end_device/<int:client_id>/monitor')
def monitor_end_device(client_id):
    # Fetch end device details
    end_device = IotDao.getClientDetails(client_id)

    # SNMP parameters
    ip_address = end_device.ip
    community = 'public'
    oid = '1.3.6.1.2.1.25.2.3.1.6.1'  # Replace with the appropriate OID for CPU load

    # Get SNMP data
    cpu_load = get(ip_address, community, oid)

    return render_template('end_device_monitor.html', client_id=client_id, end_device=end_device, cpu_load=cpu_load)