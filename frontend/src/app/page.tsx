"use client";

import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#020617] text-slate-300 selection:bg-indigo-500/30">
      {/* Background Orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-24 -left-24 w-96 h-96 bg-indigo-500/10 rounded-full blur-[120px]"></div>
        <div className="absolute top-1/2 -right-24 w-80 h-80 bg-purple-500/10 rounded-full blur-[100px]"></div>
      </div>

      {/* Navigation */}
      <nav className="glass-header sticky top-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-500 rounded-lg flex items-center justify-center text-white font-bold shadow-lg shadow-indigo-500/20">T</div>
            <span className="text-xl font-bold text-white tracking-tight">Todo App</span>
          </div>
          <div className="flex gap-4 items-center">
            <Link
              href="/login"
              className="text-sm font-semibold text-slate-400 hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/signup"
              className="px-5 py-2.5 bg-indigo-600 text-white text-sm font-bold rounded-xl hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-500/20 active:scale-95"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative flex flex-col items-center justify-center pt-20 pb-32 px-4">
        <div className="text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-bold mb-8 animate-in fade-in slide-in-from-top-4 duration-1000">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
            </span>
            NOW IN PUBLIC BETA
          </div>
          
          <h1 className="text-6xl md:text-8xl font-black text-white mb-8 tracking-tighter leading-none animate-in fade-in slide-in-from-bottom-4 duration-700">
            Organize work, <br /> 
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
              Master your life.
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed animate-in fade-in slide-in-from-bottom-6 duration-1000">
            The next-gen task manager for individuals who demand peak performance. 
            Beautifully designed, lightning fast, and built for your workflow.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-in fade-in slide-in-from-bottom-8 duration-1000">
            <Link
              href="/signup"
              className="px-10 py-4 bg-indigo-600 text-white font-bold rounded-2xl hover:bg-indigo-500 transition-all shadow-xl shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:-translate-y-1 active:translate-y-0 text-lg"
            >
              Start for Free
            </Link>
            <Link
              href="/login"
              className="px-10 py-4 border border-slate-700 text-white font-bold rounded-2xl hover:bg-slate-800 transition-all hover:-translate-y-1 active:translate-y-0 text-lg"
            >
              Live Demo
            </Link>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-6 py-32 border-t border-slate-900">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {[
            { icon: "✨", title: "Pure Precision", desc: "Crafted with attention to every pixel for a focused work experience." },
            { icon: "🔐", title: "Enterprise Security", desc: "Your data is protected by industry-leading encryption and auth protocols." },
            { icon: "⚡", title: "Blink Fast", desc: "Optimized for speed. Zero lag, instant syncing, and fluid interactions." }
          ].map((feature, i) => (
            <div key={i} className="group p-8 rounded-3xl border border-slate-800 bg-slate-900/40 hover:bg-slate-800/60 transition-all duration-300">
              <div className="text-4xl mb-6 group-hover:scale-125 transition-transform duration-300 inline-block">{feature.icon}</div>
              <h3 className="text-xl font-bold text-white mb-3">
                {feature.title}
              </h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                {feature.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-20">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-indigo-500 rounded flex items-center justify-center text-white font-bold text-xs">T</div>
            <span className="font-bold text-white tracking-tight">Todo App</span>
          </div>
          <div className="text-slate-500 text-sm">
            &copy; 2026 Todo App. Built for peak performance.
          </div>
          <div className="flex gap-6">
             <a href="#" className="text-slate-500 hover:text-white transition-colors">Twitter</a>
             <a href="#" className="text-slate-500 hover:text-white transition-colors">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}