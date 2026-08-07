import Link from 'next/link';

export default function Home() {
  return (
    <main className="animate-fade-in" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Navigation Bar */}
      <nav style={{ padding: '24px 0', borderBottom: '1px solid var(--border-light)', background: 'var(--glass-bg)', backdropFilter: 'blur(10px)', position: 'sticky', top: 0, zIndex: 50 }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '40px', height: '40px', background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '20px' }}>
              V
            </div>
            <h2 style={{ fontSize: '1.25rem', letterSpacing: '0' }}>VU<span className="text-gradient">Agent</span></h2>
          </div>
          <div>
            <Link href="/login" className="btn-secondary">
              Login to Dashboard
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container flex-center" style={{ flex: 1, flexDirection: 'column', textAlign: 'center', padding: '80px 24px', position: 'relative' }}>
        
        <div style={{ display: 'inline-block', padding: '6px 16px', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.2)', borderRadius: '20px', color: 'var(--accent-primary)', fontWeight: '600', fontSize: '0.875rem', marginBottom: '24px' }}>
          🚀 Revolutionizing VU Exam Preparations
        </div>

        <h1 style={{ fontSize: 'clamp(2.5rem, 5vw, 4.5rem)', lineHeight: '1.1', marginBottom: '24px', maxWidth: '900px' }}>
          Never Miss a VU Quiz Again with <br />
          <span className="text-gradient">Automated AI Tracking</span>
        </h1>
        
        <p style={{ fontSize: '1.125rem', color: 'var(--text-secondary)', maxWidth: '600px', marginBottom: '40px', lineHeight: '1.6' }}>
          Securely link your Virtual University portal. Our agent monitors your dashboard 24/7, alerts you about pending quizzes, and keeps your academic life completely stress-free.
        </p>
        
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', justifyContent: 'center' }}>
          <Link href="/login" className="btn-primary" style={{ padding: '16px 32px', fontSize: '1.125rem' }}>
            Get Started Free
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </Link>
          <button className="btn-secondary" style={{ padding: '16px 32px', fontSize: '1.125rem' }}>
            View Demo
          </button>
        </div>

        {/* Feature Cards Preview */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', width: '100%', marginTop: '80px', textAlign: 'left' }}>
          
          <div className="glass-card">
            <div style={{ width: '48px', height: '48px', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px', color: 'var(--accent-primary)' }}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>Real-time Monitoring</h3>
            <p style={{ color: 'var(--text-secondary)' }}>Our agents check your LMS continuously without triggering bot protections or logging you out.</p>
          </div>

          <div className="glass-card">
            <div style={{ width: '48px', height: '48px', background: 'rgba(139, 92, 246, 0.1)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px', color: 'var(--accent-secondary)' }}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>Smart Email Alerts</h3>
            <p style={{ color: 'var(--text-secondary)' }}>Get beautiful HTML email digests detailing your pending, attempted, and upcoming quizzes.</p>
          </div>

          <div className="glass-card">
            <div style={{ width: '48px', height: '48px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px', color: 'var(--success)' }}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>Bank-grade Security</h3>
            <p style={{ color: 'var(--text-secondary)' }}>Your credentials are encrypted using AES-256. We never store plaintext passwords.</p>
          </div>

        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid var(--border-light)', padding: '40px 0', textAlign: 'center', color: 'var(--text-tertiary)', fontSize: '0.875rem' }}>
        <p>© 2026 VU Quiz Agent SaaS. Created with ❤️ for Virtual University Students.</p>
      </footer>
    </main>
  );
}
