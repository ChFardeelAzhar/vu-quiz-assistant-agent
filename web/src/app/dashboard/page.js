"use client";

import { useState } from 'react';
import Link from 'next/link';

export default function Dashboard() {
  const [isAgentActive, setIsAgentActive] = useState(true);

  // Mock data representing the backend scrape results
  const summaryData = {
    pending: [
      { subject: "Data Structures", title: "Quiz # 1", end: "May 06, 2026 11:59 PM" },
      { subject: "Database Management", title: "Quiz # 2", end: "May 08, 2026 11:59 PM" }
    ],
    upcoming: [
      { subject: "Object Oriented Programming", title: "Quiz # 2", start: "May 10, 2026 12:00 AM" }
    ],
    attempted: [
      { subject: "Pakistan Studies", title: "Quiz # 1", end: "May 01, 2026 11:59 PM", status: "Result Declared" }
    ]
  };

  return (
    <main className="animate-fade-in" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Top Bar */}
      <nav style={{ padding: '16px 0', borderBottom: '1px solid var(--border-light)', background: 'var(--glass-bg)', backdropFilter: 'blur(10px)', position: 'sticky', top: 0, zIndex: 50 }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '32px', height: '32px', background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '16px' }}>
              V
            </div>
            <h2 style={{ fontSize: '1rem', letterSpacing: '0' }}>Dashboard</h2>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>BC200200000</span>
            <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'var(--bg-tertiary)', border: '1px solid var(--border-light)', overflow: 'hidden' }}>
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="Avatar" style={{ width: '100%', height: '100%' }} />
            </div>
          </div>
        </div>
      </nav>

      <div className="container" style={{ padding: '40px 24px', flex: 1 }}>
        
        {/* Header Area */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '20px', marginBottom: '40px' }}>
          <div>
            <h1 style={{ fontSize: '2rem', marginBottom: '8px' }}>Overview</h1>
            <p style={{ color: 'var(--text-secondary)' }}>Welcome back! Here is your latest LMS quiz status.</p>
          </div>
          
          <div className="glass-card" style={{ padding: '16px 24px', display: 'flex', alignItems: 'center', gap: '16px', margin: 0 }}>
            <div>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>Agent Status</p>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600 }}>
                <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: isAgentActive ? 'var(--success)' : 'var(--text-tertiary)', boxShadow: isAgentActive ? '0 0 10px var(--success)' : 'none' }}></div>
                {isAgentActive ? 'Monitoring Active' : 'Paused'}
              </div>
            </div>
            <div style={{ height: '40px', width: '1px', background: 'var(--border-light)' }}></div>
            <button 
              onClick={() => setIsAgentActive(!isAgentActive)}
              className={isAgentActive ? "btn-secondary" : "btn-primary"} 
              style={{ padding: '8px 16px', fontSize: '0.875rem' }}
            >
              {isAgentActive ? 'Pause' : 'Resume'}
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px', marginBottom: '40px' }}>
          
          <div className="glass-card" style={{ borderLeft: '4px solid var(--danger)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '8px' }}>Action Required</p>
                <h2 style={{ fontSize: '2.5rem', margin: 0 }}>{summaryData.pending.length}</h2>
              </div>
              <div style={{ padding: '8px', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', color: 'var(--danger)' }}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              </div>
            </div>
            <p style={{ fontSize: '0.875rem', marginTop: '16px', fontWeight: 500 }}>Pending Quizzes</p>
          </div>

          <div className="glass-card" style={{ borderLeft: '4px solid var(--accent-primary)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '8px' }}>Scheduled</p>
                <h2 style={{ fontSize: '2.5rem', margin: 0 }}>{summaryData.upcoming.length}</h2>
              </div>
              <div style={{ padding: '8px', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '8px', color: 'var(--accent-primary)' }}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              </div>
            </div>
            <p style={{ fontSize: '0.875rem', marginTop: '16px', fontWeight: 500 }}>Upcoming Quizzes</p>
          </div>

          <div className="glass-card" style={{ borderLeft: '4px solid var(--success)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '8px' }}>Completed</p>
                <h2 style={{ fontSize: '2.5rem', margin: 0 }}>{summaryData.attempted.length}</h2>
              </div>
              <div style={{ padding: '8px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '8px', color: 'var(--success)' }}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              </div>
            </div>
            <p style={{ fontSize: '0.875rem', marginTop: '16px', fontWeight: 500 }}>Attempted / Closed</p>
          </div>

        </div>

        {/* Pending Quizzes List */}
        <h3 style={{ fontSize: '1.25rem', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--danger)' }}></span>
          Pending Quizzes
        </h3>
        
        <div className="glass-card" style={{ padding: 0, overflow: 'hidden', marginBottom: '40px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ background: 'rgba(255, 255, 255, 0.02)', borderBottom: '1px solid var(--border-light)' }}>
                <th style={{ padding: '16px 24px', fontWeight: 500, color: 'var(--text-secondary)' }}>Subject</th>
                <th style={{ padding: '16px 24px', fontWeight: 500, color: 'var(--text-secondary)' }}>Quiz Title</th>
                <th style={{ padding: '16px 24px', fontWeight: 500, color: 'var(--text-secondary)' }}>Deadline</th>
                <th style={{ padding: '16px 24px', fontWeight: 500, color: 'var(--text-secondary)', textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {summaryData.pending.length > 0 ? summaryData.pending.map((quiz, i) => (
                <tr key={i} style={{ borderBottom: i !== summaryData.pending.length - 1 ? '1px solid var(--border-light)' : 'none' }}>
                  <td style={{ padding: '16px 24px', fontWeight: 500 }}>{quiz.subject}</td>
                  <td style={{ padding: '16px 24px' }}>{quiz.title}</td>
                  <td style={{ padding: '16px 24px', color: 'var(--danger)' }}>{quiz.end}</td>
                  <td style={{ padding: '16px 24px', textAlign: 'right' }}>
                    <button className="btn-primary" style={{ padding: '6px 16px', fontSize: '0.875rem' }}>Solve Now</button>
                  </td>
                </tr>
              )) : (
                <tr>
                  <td colSpan="4" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-secondary)' }}>No pending quizzes! Good job.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        
      </div>
    </main>
  );
}
