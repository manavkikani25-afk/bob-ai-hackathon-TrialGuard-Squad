import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import './index.css';

class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { hasError: boolean; error: Error | null }> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("React Error Boundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 40, background: '#F8FAFC', color: '#0F172A', fontFamily: 'sans-serif', minHeight: '100vh' }}>
          <div style={{ maxWidth: 800, margin: '0 auto', background: '#FFFFFF', padding: 32, borderRadius: 16, border: '1px solid #E2E8F0', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
            <h2 style={{ color: '#DC2626', fontSize: 20, fontWeight: 'bold', marginBottom: 12 }}>TrialGuard AI — Application Error</h2>
            <p style={{ fontSize: 14, color: '#475569', marginBottom: 16 }}>An error occurred while rendering the clinical trial dashboard.</p>
            <pre style={{ background: '#F1F5F9', padding: 16, borderRadius: 8, fontSize: 12, color: '#1E293B', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>
              {this.state.error?.toString()}
              {'\n\n'}
              {this.state.error?.stack}
            </pre>
            <button
              onClick={() => window.location.reload()}
              style={{ marginTop: 20, padding: '10px 20px', background: '#064E3B', color: '#FFFFFF', border: 'none', borderRadius: 8, fontWeight: 'bold', cursor: 'pointer' }}
            >
              Reload Dashboard
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
);
