from flask import Flask, render_template, jsonify
import psutil
import os
import platform

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def system_status():
    """Fetch system performance metrics."""
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    temperature = psutil.sensors_temperatures().get('cpu_thermal', [{}])[0].get('current', 'N/A')
    
    return jsonify({
        "cpu_usage": cpu_usage,
        "memory_used": memory_info.used / (1024 ** 3),
        "memory_total": memory_info.total / (1024 ** 3),
        "disk_used": disk_usage.used / (1024 ** 3),
        "disk_total": disk_usage.total / (1024 ** 3),
        "temperature": temperature
    })

if __name__ == "__main__":
    app.run(debug=True)