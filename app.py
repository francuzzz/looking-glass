from flask import Flask, request, render_template, jsonify
import subprocess
import platform

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form.get('command')
    target = request.form.get('target')
    
    if not target:
        return jsonify('Target is required'), 400

    if command == 'ping':
        cmd = ['ping', '-c', '4', target]
    elif command == 'traceroute':
        cmd = ['traceroute', target]
    elif command == 'browser_ping':
        if platform.system() == 'Windows':
            cmd = ['ping', '-n', '4', target]
        else:
            cmd = ['ping', '-c', '4', target]
    else:
        return jsonify('Invalid command'), 400

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return jsonify(result.stdout)
    except subprocess.CalledProcessError as e:
        return jsonify(f'Command failed: {e.stderr}'), 500
    except Exception as e:
        return jsonify(f'Error: {str(e)}'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
