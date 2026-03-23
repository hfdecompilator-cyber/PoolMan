import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';

export default function RemoteControlApp() {
  const [pcIp, setPcIp] = useState('192.168.1.100');
  const [code, setCode] = useState('import platform\nprint(platform.system())');
  const [output, setOutput] = useState('Output will appear here');
  const [loading, setLoading] = useState(false);

  const executeScript = async () => {
    if (!pcIp || !code) {
      setOutput('Enter IP and code');
      return;
    }

    setLoading(true);
    setOutput('Executing...');

    try {
      const url = `http://${pcIp}:5000/api/execute`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ script: code })
      });

      const data = await response.json();
      setOutput(data.output || data.error || 'No output');
    } catch (e) {
      setOutput('Error: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (preset) => {
    const presets = {
      'system': 'import platform\nprint(f"OS: {platform.system()}")',
      'time': 'from datetime import datetime\nprint(datetime.now())',
      'files': 'from pathlib import Path\nfiles = list(Path.home().glob("*"))[:5]\nfor f in files: print(f.name)',
      'ip': 'import socket\nprint(socket.gethostbyname(socket.gethostname()))'
    };
    setCode(presets[preset] || '');
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>CommandCube Remote Control</Text>

      <View style={styles.section}>
        <Text style={styles.label}>PC IP Address</Text>
        <TextInput
          style={styles.input}
          placeholder="192.168.1.100"
          value={pcIp}
          onChangeText={setPcIp}
          placeholderTextColor="#999"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Python Code</Text>
        <TextInput
          style={[styles.input, styles.codeInput]}
          placeholder="Enter Python code..."
          value={code}
          onChangeText={setCode}
          multiline
          placeholderTextColor="#999"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Presets</Text>
        <View style={styles.presets}>
          {['system', 'time', 'files', 'ip'].map(p => (
            <TouchableOpacity
              key={p}
              style={styles.presetBtn}
              onPress={() => loadPreset(p)}
            >
              <Text style={styles.presetText}>{p.toUpperCase()}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.buttons}>
        <TouchableOpacity style={styles.executeBtn} onPress={executeScript} disabled={loading}>
          <Text style={styles.btnText}>EXECUTE</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.clearBtn} onPress={() => { setCode(''); setOutput(''); }}>
          <Text style={styles.btnText}>CLEAR</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.label}>Output</Text>
        <View style={styles.output}>
          <Text style={styles.outputText}>{output}</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#00d4ff',
    textAlign: 'center',
    marginBottom: 30,
  },
  section: {
    marginBottom: 20,
  },
  label: {
    color: '#00d4ff',
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 8,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  input: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.3)',
    borderRadius: 8,
    color: '#fff',
    padding: 12,
    fontSize: 14,
  },
  codeInput: {
    height: 150,
    textAlignVertical: 'top',
  },
  presets: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  presetBtn: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: 'rgba(0, 212, 255, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(0, 212, 255, 0.3)',
    borderRadius: 6,
    padding: 10,
    alignItems: 'center',
  },
  presetText: {
    color: '#00d4ff',
    fontSize: 12,
    fontWeight: '600',
  },
  buttons: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 20,
  },
  executeBtn: {
    flex: 1,
    backgroundColor: '#00d4ff',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  clearBtn: {
    flex: 1,
    backgroundColor: 'rgba(0, 212, 255, 0.2)',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  btnText: {
    color: '#000',
    fontWeight: '600',
    fontSize: 13,
  },
  output: {
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 8,
    padding: 12,
    minHeight: 150,
  },
  outputText: {
    color: '#00ff88',
    fontSize: 12,
    fontFamily: 'monospace',
  },
});
