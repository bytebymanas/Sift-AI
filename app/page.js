'use client';

import { useState } from 'react';

export default function ControlDashboard() {
  const [isExecuting, setIsExecuting] = useState(false);
  const [logStatus, setLogStatus] = useState('System Standby');

  const dispatchRun = async () => {
    setIsExecuting(true);
    setLogStatus('Sending trigger signal to GitHub Actions Cloud Runner...');

    try {
      const response = await fetch('/api/trigger', { method: 'POST' });
      const data = await response.json();

      if (response.ok) {
        setLogStatus('[✓] Success: Cloud worker engaged. Google Colab execution started!');
      } else {
        setLogStatus(`[X] Dispatch Error: ${data.error || 'Server error'}`);
      }
    } catch (err) {
      setLogStatus(`[X] Network Error: ${err.message}`);
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <main style={styles.main}>
      <section style={styles.card}>
        <div style={styles.statusIndicator}>SYSTEM ONLINE</div>
        <h1 style={styles.header}>CrewAI Agent Controller</h1>
        <p style={styles.subtext}>Google Colab Cloud Execution Engine</p>

        <div style={styles.console}>
          <span style={styles.consoleLabel}>Execution Logs:</span>
          <p style={styles.consoleText}>{logStatus}</p>
        </div>

        <button
          onClick={dispatchRun}
          disabled={isExecuting}
          style={{
            ...styles.button,
            opacity: isExecuting ? 0.6 : 1,
            cursor: isExecuting ? 'not-allowed' : 'pointer',
          }}
        >
          {isExecuting ? 'Dispatching...' : '▶ Trigger Agent Workflow Now'}
        </button>

        <div style={styles.metaBox}>
          <div><strong>Schedule:</strong> Daily Cron (GitHub Actions)</div>
          <div><strong>Runner:</strong> Headless Playwright (Ubuntu)</div>
          <div><strong>Execution Target:</strong> Google Colab GPU</div>
        </div>
      </section>
    </main>
  );
}

const styles = {
  main: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'monospace',
    color: '#f8fafc',
  },
  card: {
    backgroundColor: '#1e293b',
    padding: '2rem',
    borderRadius: '12px',
    border: '1px solid #334155',
    width: '100%',
    maxWidth: '480px',
    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)',
  },
  statusIndicator: {
    display: 'inline-block',
    fontSize: '0.7rem',
    fontWeight: 'bold',
    color: '#22c55e',
    backgroundColor: '#052e16',
    padding: '0.2rem 0.6rem',
    borderRadius: '9999px',
    marginBottom: '1rem',
    border: '1px solid #15803d',
  },
  header: { fontSize: '1.3rem', margin: '0 0 0.4rem 0' },
  subtext: { color: '#94a3b8', fontSize: '0.85rem', margin: '0 0 1.5rem 0' },
  console: {
    backgroundColor: '#020617',
    padding: '1rem',
    borderRadius: '6px',
    border: '1px solid #1e293b',
    marginBottom: '1.5rem',
  },
  consoleLabel: { color: '#64748b', fontSize: '0.75rem' },
  consoleText: { color: '#38bdf8', margin: '0.5rem 0 0 0', fontSize: '0.875rem' },
  button: {
    width: '100%',
    padding: '0.85rem',
    backgroundColor: '#2563eb',
    color: '#ffffff',
    border: 'none',
    borderRadius: '6px',
    fontWeight: 'bold',
    fontSize: '0.95rem',
  },
  metaBox: {
    marginTop: '1.5rem',
    paddingTop: '1rem',
    borderTop: '1px solid #334155',
    fontSize: '0.75rem',
    color: '#94a3b8',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.4rem',
  },
};