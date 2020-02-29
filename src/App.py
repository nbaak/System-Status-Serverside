from flask import Flask
import shutil
import json
import psutil

app = Flask(__name__)

@app.route("/status")
def status():
    '''
    returns system stats like harddisk storage, memory usage and cpu temperature
    '''
    data = {'storage': disk_usage(),
            'memory': memory_usage(),
            'cpu': cpu_stats()}

    return json.dumps(data)

def cpu_stats ():
    stats = psutil.sensors_temperatures()
    
    data = {'percent' : psutil.cpu_percent(interval=None, percpu=True),
            'temperature': cpu_temperatures(stats),
            'count': psutil.cpu_count(),
            'frequencys': cpu_frequencys()
            }
    return data

def cpu_temperatures(stats):
    data = []
    
    for group in stats:
        for item in stats[group]:
            d= {'label': default_value(item.label, f"{group}_CPU"),
                'current': default_value(item.current, 100),
                'high': default_value(item.high, 100),
                'critical': default_value(item.critical, 100)
                }
            data.append(d)
        
    return data

def cpu_frequencys(pc = True):
    freqs = psutil.cpu_freq(percpu=pc)
    data = []
    if pc:
        for freq in freqs:
            # frequencies in MHz
             d = {'current': freq.current,
                  'min': freq.min,
                  'max': freq.max}
             
             data.append(d)
    else:
        data = freqs

    return data

def memory_usage():
    memory = psutil.virtual_memory()
    
    data = {'free': default_value(round(memory.free / 2**30,2), 0),
            'used': default_value(round(memory.used / 2**30,2), 0),
            'total': default_value(round(memory.total / 2**30,2), 0),
            'percent': default_value(round(memory.used/memory.total * 100, 2), 0)
            }
    return data

def disk_usage():
    total, used, free = shutil.disk_usage('/')
    # data in GB
    data = {'total': default_value(round(total / 2**30,2), 100),
            'used': default_value(round(used / 2**30,2), 100),
            'free': default_value(round(free / 2**30,2), 100),
            'percent': default_value(round(used/total * 100, 2), 100)
            }
    
    return data

def default_value(value, default):
    if value:
        return value
    else:
        return default

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5555)
    
    
    
    
    
    
    