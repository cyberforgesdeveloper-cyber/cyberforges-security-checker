'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [scanStep, setScanStep] = useState('');
  const [scanResult, setScanResult] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState('');

  // Scanning progress steps text animation
  useEffect(() => {
    if (!loading) return;
    const steps = [
      'Resolving domain & checking connectivity...',
      'Validating SSL/TLS certificates...',
      'Inspecting security headers (HSTS, CSP)...',
      'Calculating final security posture...'
    ];
    let i = 0;
    setScanStep(steps[0]);
    const interval = setInterval(() => {
      i++;
      if (i < steps.length) {
        setScanStep(steps[i]);
      }
    }, 600);
    return () => clearInterval(interval);
  }, [loading]);

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) {
      setErrorMsg('Please enter a website domain.');
      return;
    }

    setLoading(true);
    setErrorMsg('');
    setScanResult(null);

    try {
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (data.success) {
        // Chota sa delay taake smooth animation feel ho
        setTimeout(() => {
          setScanResult(data.data);
          setLoading(false);
        }, 1200);
      } else {
        setErrorMsg(data.error || 'Failed to scan the website.');
        setLoading(false);
      }
    } catch (err) {
      setErrorMsg('Something went wrong. Please try again.');
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white selection:bg-cyan-500 selection:text-white">
      {/* Navbar */}
      <nav className="border-b border-slate-800 sticky top-0 bg-slate-950/80 backdrop-blur-md z-50">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="text-xl font-bold flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-cyan-500/20 border border-cyan-500/40 flex items-center justify-center text-cyan-400 text-sm font-extrabold">
              CF
            </div>
            Cyber<span className="text-cyan-400">Forges</span>
          </div>
          <div className="text-xs text-slate-400 border border-slate-800 px-3 py-1.5 rounded-full bg-slate-900/50">
            Security Checker v1.0
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_right,_rgba(6,182,212,0.12),_transparent_40%)]" />

        <div className="mx-auto max-w-7xl px-6 py-20 text-center md:py-28">
          <div className="mx-auto mb-6 inline-flex rounded-full border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-300 shadow-lg shadow-cyan-500/5">
            🔐 Free Real-Time Website Security Inspection
          </div>

          <h1 className="mx-auto max-w-4xl text-4xl font-bold leading-tight tracking-tight md:text-6xl">
            Check Your Website
            <span className="block text-cyan-400 mt-1">Security in Seconds</span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-400">
            Analyze SSL protocols, security headers, and overall configuration instantly to protect your digital assets.
          </p>

          {/* Scanner Box */}
          <div className="mx-auto mt-10 max-w-3xl rounded-2xl border border-slate-700/80 bg-slate-900/80 p-3 shadow-2xl backdrop-blur-xl">
            <form onSubmit={handleScan} className="flex flex-col gap-3 md:flex-row">
              <div className="relative flex-1">
                <span className="absolute inset-y-0 left-0 pl-4 flex items-center text-slate-500 text-sm font-mono pointer-events-none">
                  https://
                </span>
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="example.com"
                  className="w-full rounded-xl border border-slate-700 bg-slate-950 py-4 pl-20 pr-4 text-white outline-none placeholder:text-slate-600 focus:border-cyan-400 font-medium text-sm transition"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="rounded-xl bg-gradient-to-r from-cyan-400 to-blue-500 px-8 py-4 font-semibold text-slate-950 transition hover:from-cyan-300 hover:to-blue-400 disabled:opacity-50 cursor-pointer flex items-center justify-center min-w-[160px] shadow-lg shadow-cyan-500/20"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-slate-950" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Scanning...</span>
                  </div>
                ) : (
                  <span>Scan Website</span>
                )}
              </button>
            </form>
          </div>

          {/* Dynamic Loading Step Text */}
          {loading && (
            <div className="mt-6 flex items-center justify-center gap-2 text-cyan-400 text-sm font-medium animate-pulse">
              <span className="h-2 w-2 rounded-full bg-cyan-400"></span>
              <span>{scanStep}</span>
            </div>
          )}

          {errorMsg && <p className="mt-4 text-sm text-red-400 font-medium">{errorMsg}</p>}
        </div>
      </section>

      {/* Results Section */}
      {scanResult && !loading && (
        <section className="border-t border-slate-800 bg-slate-900/60 py-16 px-6">
          <div className="mx-auto max-w-4xl rounded-2xl border border-slate-800 bg-slate-950 p-6 md:p-8 shadow-2xl">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-800 pb-6 gap-4">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">Security Assessment Report</span>
                <h2 className="text-2xl font-bold mt-1 text-white">{scanResult.domain}</h2>
              </div>
              <div className="flex items-center gap-4 bg-slate-900/80 border border-slate-800 px-4 py-2 rounded-xl">
                <div className="text-right">
                  <div className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Security Score</div>
                  <div className="text-3xl font-extrabold text-cyan-400">{scanResult.score}/100</div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 my-6">
              <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-800/80">
                <div className="text-slate-400 text-xs">Response Time</div>
                <div className="text-lg font-semibold mt-1 text-white">{scanResult.responseTime}</div>
              </div>
              <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-800/80">
                <div className="text-slate-400 text-xs">HTTP Status</div>
                <div className="text-lg font-semibold mt-1 text-white">{scanResult.statusCode} (Active)</div>
              </div>
            </div>

            <h3 className="text-lg font-semibold mb-4 text-white">Detailed Configurations</h3>
            <div className="space-y-3">
              {Object.entries(scanResult.checks).map(([key, check]) => {
                const c = check as any;
                return (
                  <div key={key} className="flex items-center justify-between p-4 rounded-xl border border-slate-800/80 bg-slate-900/30 hover:bg-slate-900/50 transition">
                    <div>
                      <div className="font-medium capitalize text-slate-200">{key.replace(/([A-Z])/g, ' $1')}</div>
                      <div className="text-xs text-slate-400 mt-0.5">{c.message}</div>
                    </div>
                    <span className={`text-xs px-3 py-1 rounded-full font-semibold border ${c.status ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20'}`}>
                      {c.status ? 'Passed' : 'Warning'}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        <p>© {new Date().getFullYear()} CyberForges. All rights reserved.</p>
      </footer>
    </main>
  );
}