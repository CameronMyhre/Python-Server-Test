from flask import Flask, jsonify, render_template  
import psutil
import subprocess
import sys
import datetime

# Redirect stdout and stderr to a log file
sys.stdout = open("/home/camer/logs/output.log", "w")
sys.stderr = sys.stdout

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def get_gpu_info():
    try:
        # Get GPU memory usage and clean the output
        gpu_mem_raw = subprocess.check_output(['vcgencmd', 'get_mem', 'gpu']).decode('utf-8').strip()
        gpu_mem = gpu_mem_raw.split('=')[1].replace('M', '')  # Get the memory in MB and remove 'M'

        # Get GPU temperature and clean the output
        gpu_temp_raw = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8').strip()
        gpu_temp = gpu_temp_raw.split('=')[1].replace("'", '')  # Remove the 'C'

        return {
            'gpu_mem': gpu_mem,  # In MB
            'gpu_temp': gpu_temp,  # In Celsius
        }
    except Exception as e:
        return {'error': str(e)}

def get_cpu_temperature():
    try:
        # Get CPU temperature in Celsius
        temp = float(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000
        return round(temp, 2)
    except Exception as e:
        return f"Error: {e}"

def get_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            # Convert uptime to hours, minutes, and seconds
            uptime = str(datetime.timedelta(seconds=uptime_seconds))
            return uptime
    except Exception as e:
        return f"Error: {e}"

def get_network_usage():
    try:
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent / (1024 ** 2),  # MB
            'bytes_recv': net_io.bytes_recv / (1024 ** 2)   # MB
        }
    except Exception as e:
        return f"Error: {e}"

def get_disk_health():
    try:
        disk_io = psutil.disk_io_counters()
        return {
            'read_count': disk_io.read_count,
            'write_count': disk_io.write_count
        }
    except Exception as e:
        return f"Error: {e}"

def get_system_load():
    try:
        load = psutil.getloadavg()
        return {
            '1min': load[0],
            '5min': load[1],
            '15min': load[2]
        }
    except Exception as e:
        return f"Error: {e}"

def get_swap_usage():
    try:
        swap = psutil.swap_memory()
        return {
            'used': swap.used / (1024 ** 3),  # GB
            'free': swap.free / (1024 ** 3),  # GB
            'percent': swap.percent
        }
    except Exception as e:
        return f"Error: {e}"

def get_processes_info():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            processes.append(proc.info)
        return processes
    except Exception as e:
        return f"Error: {e}"

def terminal_output():
    try:
        with open("/home/camer/logs/output.log", 'r') as file:

            # Read all lines from the file and get the last 25 lines
            lines = file.readlines()[-25:]

            # Join the lines with <br> for line breaks
            return "<br>".join([line.strip() for line in lines])
    except Exception as e:
        
        # Return the error message with <br> for line breaks
        return f"Error reading log file: {str(e)}".replace("\n", "<br>")

@app.route('/api/status')
def status():

    # Example data for testing
    data = {
        'cpu_usage': psutil.cpu_percent(),
        'memory_used': psutil.virtual_memory().used / (1024 ** 3),
        'memory_total': psutil.virtual_memory().total / (1024 ** 3),
        'disk_used': psutil.disk_usage('/').used / (1024 ** 3),
        'disk_total': psutil.disk_usage('/').total / (1024 ** 3),
        'gpu_info': get_gpu_info(),
        'temperature': get_cpu_temperature(),
        'network_usage': get_network_usage(),
        'uptime': get_uptime(),
        'disk_health': get_disk_health(),
        'system_load': get_system_load(),
        'swap_usage': get_swap_usage(),
        'process_info': get_processes_info(),
        'terminal_output': terminal_output()
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)