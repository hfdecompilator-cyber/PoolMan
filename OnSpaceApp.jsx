/*
CommandCube - OnSpace AI App with Persistence
Saves scripts and settings automatically
*/

import React, { useState, useEffect } from 'react';

export default function CommandCubeApp() {
  const [pcIp, setPcIp] = useState('192.168.1.100');
  const [port, setPort] = useState('5000');
  const [script, setScript] = useState('');
  const [output, setOutput] = useState('Ready...');
  const [loading, setLoading] = useState(false);
  const [connected, setConnected] = useState(false);
  const [autoRun, setAutoRun] = useState(false);

  // Load saved data on app start
  useEffect(() => {
    loadSavedData();
  }, []);

  // Auto-save script when it changes
  useEffect(() => {
    if (script) {
      localStorage.setItem('commandcube_script', script);
    }
  }, [script]);

  // Save settings
  useEffect(() => {
    localStorage.setItem('commandcube_ip', pcIp);
    localStorage.setItem('commandcube_port', port);
    localStorage.setItem('commandcube_autorun', autoRun);
  }, [pcIp, port, autoRun]);

  const loadSavedData = async () => {
    const savedScript = localStorage.getItem('commandcube_script') || 'import platform\nprint(platform.system())';
    const savedIp = localStorage.getItem('commandcube_ip') || '192.168.1.100';
    const savedPort = localStorage.getItem('commandcube_port') || '5000';
    const savedAutoRun = localStorage.getItem('commandcube_autorun') === 'true';

    setScript(savedScript);
    setPcIp(savedIp);
    setPort(savedPort);
    setAutoRun(savedAutoRun);

    // Auto-connect on load
    setTimeout(() => testConnection(savedIp, savedPort), 500);

    // Auto-run if enabled
    if (savedAutoRun) {
      setTimeout(() => executeScript(savedScript, savedIp, savedPort), 1000);
    }
  };

  const testConnection = async (ip = pcIp, p = port) => {
    try {
      const response = await fetch(`http://${ip}:${p}/api/status`, { timeout: 5000 });
      if (response.ok) {
        setConnected(true);
        setOutput('Connected to PC!');
        return true;
      }
    } catch (e) {
      setOutput('Cannot connect to PC');
      setConnected(false);
    }
    return false;
  };

  const executeScript = async (scriptToRun = script, ip = pcIp, p = port) => {
    if (!scriptToRun.trim()) {
      setOutput('Enter script');
      return;
    }

    setLoading(true);
    setOutput('Executing...');

    try {
      const response = await fetch(`http://${ip}:${p}/api/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ script: scriptToRun })
      });
      const data = await response.json();
      setOutput(data.output || data.error || 'Executed');
    } catch (e) {
      setOutput('Error: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (code) => setScript(code);

  const presets = {
    'System': 'import platform\nprint(f"OS: {platform.system()}")\nprint(f"Processor: {platform.processor()}")',
    'Time': 'from datetime import datetime\nprint(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))',
    'IP': 'import socket\nprint(socket.gethostbyname(socket.gethostname()))',
    'Files': 'from pathlib import Path\nfiles = list(Path.home().glob("*"))[:10]\nfor f in files: print(f.name)',
    'Memory': 'import psutil\nprint(f"RAM: {psutil.virtual_memory().percent}%")',
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>⚡ CommandCube</h1>
      
      <div style={styles.section}>
        <label style={styles.label}>PC Connection</label>
        <div style={styles.connSettings}>
          <input
            type="text"
            placeholder="IP"
            value={pcIp}
            onChange={(e) => setPcIp(e.target.value)}
            style={styles.input}
          />
          <input
            type="text"
            placeholder="Port"
            value={port}
            onChange={(e) => setPort(e.target.value)}
            style={styles.input}
          />
          <button onClick={() => testConnection()} style={styles.connectBtn}>
            {connected ? '✓' : 'Connect'}
          </button>
        </div>
      </div>

      <div style={styles.section}>
        <div style={styles.autoRunSection}>
          <label style={{ ...styles.label, marginBottom: '0' }}>
            <input
              type="checkbox"
              checked={autoRun}
              onChange={(e) => setAutoRun(e.target.checked)}
              style={{ marginRight: '8px' }}
            />
            Auto-run on startup
          </label>
        </div>
      </div>

      <div style={styles.section}>
        <label style={styles.label}>Python Script (Auto-saved)</label>
        <textarea
          value={script}
          onChange={(e) => setScript(e.target.value)}
          style={styles.textarea}
          placeholder="Enter Python code..."
        />
      </div>

      <div style={styles.section}>
        <label style={styles.label}>Quick Presets</label>
        <div style={styles.presets}>
          {Object.entries(presets).map(([name, code]) => (
            <button
              key={name}
              onClick={() => loadPreset(code)}
              style={styles.presetBtn}
            >
              {name}
            </button>
          ))}
        </div>
      </div>

      <div style={styles.buttonGroup}>
        <button
          onClick={() => executeScript()}
          disabled={!connected || loading}
          style={{...styles.executeBtn, opacity: (!connected || loading) ? 0.5 : 1}}
        >
          {loading ? 'Running...' : 'Execute'}
        </button>
        <button
          onClick={() => {
            setScript('');
            setOutput('Ready...');
            localStorage.removeItem('commandcube_script');
          }}
          style={styles.clearBtn}
        >
          Clear
        </button>
      </div>

      <div style={styles.section}>
        <label style={styles.label}>Output</label>
        <div style={styles.output}>
          {output}
        </div>
      </div>

      <div style={styles.statusBar}>
        {connected ? '🟢 Connected' : '🔴 Offline'} | Script saved automatically
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px',
    background: 'linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%)',
    minHeight: '100vh',
    color: '#fff',
    fontFamily: 'Segoe UI, sans-serif'
  },
  title: {
    textAlign: 'center',
    fontSize: '28px',
    marginBottom: '30px',
    background: 'linear-gradient(135deg, #00d4ff, #0099cc)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text'
  },
  section: {
    marginBottom: '25px'
  },
  label: {
    display: 'block',
    marginBottom: '10px',
    fontSize: '12px',
    fontWeight: '600',
    color: '#00d4ff',
    textTransform: 'uppercase',
    letterSpacing: '1px'
  },
  autoRunSection: {
    background: 'rgba(0, 212, 255, 0.1)',
    padding: '12px',
    borderRadius: '6px',
    border: '1px solid rgba(0, 212, 255, 0.3)'
  },
  connSettings: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr auto',
    gap: '10px'
  },
  input: {
    padding: '10px',
    background: 'rgba(255, 255, 255, 0.05)',
    border: '1px solid rgba(0, 212, 255, 0.3)',
    borderRadius: '6px',
    color: '#fff',
    fontSize: '14px'
  },
  connectBtn: {
    padding: '10px 15px',
    background: '#00d4ff',
    color: '#000',
    border: 'none',
    borderRadius: '6px',
    fontWeight: '600',
    cursor: 'pointer',
    fontSize: '12px'
  },
  textarea: {
    width: '100%',
    height: '180px',
    padding: '12px',
    background: 'rgba(255, 255, 255, 0.05)',
    border: '1px solid rgba(0, 212, 255, 0.3)',
    borderRadius: '6px',
    color: '#fff',
    fontFamily: 'monospace',
    fontSize: '13px',
    resize: 'vertical'
  },
  presets: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '10px'
  },
  presetBtn: {
    padding: '10px',
    background: 'rgba(0, 212, 255, 0.1)',
    border: '1px solid rgba(0, 212, 255, 0.3)',
    borderRadius: '6px',
    color: '#00d4ff',
    cursor: 'pointer',
    fontWeight: '600',
    fontSize: '12px'
  },
  buttonGroup: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '10px',
    marginBottom: '25px'
  },
  executeBtn: {
    padding: '12px',
    background: 'linear-gradient(135deg, #00d4ff, #0099cc)',
    color: '#000',
    border: 'none',
    borderRadius: '6px',
    fontWeight: '600',
    cursor: 'pointer',
    fontSize: '14px'
  },
  clearBtn: {
    padding: '12px',
    background: 'rgba(0, 212, 255, 0.2)',
    color: '#00d4ff',
    border: '1px solid rgba(0, 212, 255, 0.3)',
    borderRadius: '6px',
    fontWeight: '600',
    cursor: 'pointer',
    fontSize: '14px'
  },
  output: {
    background: 'rgba(0, 0, 0, 0.3)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    borderRadius: '6px',
    padding: '15px',
    minHeight: '150px',
    maxHeight: '400px',
    overflowY: 'auto',
    whiteSpace: 'pre-wrap',
    wordWrap: 'break-word',
    fontFamily: 'monospace',
    fontSize: '12px',
    color: '#00ff88'
  },
  statusBar: {
    textAlign: 'center',
    fontSize: '12px',
    color: '#888',
    paddingTop: '20px',
    borderTop: '1px solid rgba(255, 255, 255, 0.1)',
    marginTop: '20px'
  }
};
