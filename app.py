#!/usr/bin/env python3
"""CommandCube Server Pro - Flask API Backend"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import json
from pathlib import Path

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/api/status', methods=['GET'])
    def status():
        """Check server status"""
        return jsonify({
            'status': 'online',
            'version': '1.0.0',
            'timestamp': str(Path('commandcube_config.json').stat().st_mtime)
        })

    @app.route('/api/execute', methods=['POST'])
    def execute():
        """Execute Python script"""
        try:
            data = request.json
            script = data.get('script', '')
            
            if not script:
                return jsonify({'error': 'No script provided'}), 400
            
            result = subprocess.run(
                [sys.executable, '-c', script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            if result.stderr:
                output += result.stderr
            
            return jsonify({
                'success': True,
                'output': output or 'Script executed'
            })
        
        except subprocess.TimeoutExpired:
            return jsonify({'error': 'Script timeout (30s max)'}), 408
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/scripts', methods=['GET'])
    def get_scripts():
        """Get saved scripts"""
        try:
            scripts_file = Path('commandcube_scripts.json')
            if scripts_file.exists():
                with open(scripts_file) as f:
                    scripts = json.load(f)
                return jsonify(scripts)
            return jsonify({})
        except:
            return jsonify({})

    @app.route('/api/scripts', methods=['POST'])
    def save_scripts():
        """Save scripts"""
        try:
            scripts = request.json
            with open('commandcube_scripts.json', 'w') as f:
                json.dump(scripts, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
