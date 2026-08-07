"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Onboarding() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [vuId, setVuId] = useState('');
  const [vuPassword, setVuPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/save-credentials', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vuId, vuPassword }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Failed to save credentials");

      // Once successfully saved, redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex-center animate-fade-in" style={{ minHeight: '100vh', padding: '24px' }}>
      <div className="glass-card" style={{ width: '100%', maxWidth: '440px', padding: '40px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{ width: '56px', height: '56px', background: 'linear-gradient(135deg, var(--accent-primary), var(--success))', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', marginBottom: '16px', margin: '0 auto' }}>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
          <h1 style={{ fontSize: '1.75rem', marginBottom: '8px' }}>Final Step</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>Link your Virtual University portal to enable AI Automation.</p>
        </div>

        {error && (
          <div style={{ padding: '12px', background: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)', borderRadius: '8px', marginBottom: '16px', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <label className="input-label" htmlFor="vu_id">VU Student ID</label>
            <input 
              type="text" 
              id="vu_id" 
              className="input-field" 
              placeholder="e.g. BC200200000" 
              value={vuId}
              onChange={(e) => setVuId(e.target.value)}
              required 
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <label className="input-label" htmlFor="vu_password" style={{ marginBottom: 0 }}>LMS Password</label>
            </div>
            <input 
              type="password" 
              id="vu_password" 
              className="input-field" 
              placeholder="••••••••" 
              value={vuPassword}
              onChange={(e) => setVuPassword(e.target.value)}
              required 
            />
          </div>

          <div style={{ padding: '12px', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: '8px', display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
            <svg style={{ color: 'var(--accent-primary)', flexShrink: 0, marginTop: '2px' }} width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: 0, lineHeight: 1.5 }}>
              Your password is encrypted locally using AES-256 before being stored. It can only be read by our secure background agent.
            </p>
          </div>

          <button type="submit" className="btn-primary" style={{ marginTop: '8px', width: '100%' }} disabled={isLoading}>
            {isLoading ? (
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <svg className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                Encrypting & Saving...
              </span>
            ) : "Connect & Enter Dashboard"}
          </button>
        </form>
        
        <style jsx>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </main>
  );
}
