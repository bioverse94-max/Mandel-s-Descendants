import { useEffect, useState } from 'react';
// import { Rocket } from 'lucide-react';

interface LoadingScreenProps {
  onComplete: () => void;
}

export default function LoadingScreen({ onComplete }: LoadingScreenProps) {
  const [progress, setProgress] = useState(0);
  const [consoleLines, setConsoleLines] = useState<string[]>([]);
  const [currentLineIndex, setCurrentLineIndex] = useState(0);

  const lines = [
    'DIAGNOSTIC_CONSOLE_V3.7.2',
    '> INITIATING DEEP_SYSTEM_SCAN...',
    '> CALIBRATING QUANTUM SENSORS...',
    '> DATA MATRICES... RECONSTRUCTING',
    '> LOADING NEURAL PATHWAYS...',
    '> ESTABLISHING SECURE CONNECTION...',
    '> FINALIZING BOOT SEQUENCE...',
  ];

  useEffect(() => {
    const lineInterval = setInterval(() => {
      if (currentLineIndex < lines.length) {
        setConsoleLines((prev) => [...prev, lines[currentLineIndex]]);
        setCurrentLineIndex((prev) => prev + 1);
      }
    }, 400);

    return () => clearInterval(lineInterval);
  }, [currentLineIndex]);

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setTimeout(() => onComplete(), 500);
          return 100;
        }
        return prev + 1;
      });
    }, 40);

    return () => clearInterval(progressInterval);
  }, [onComplete]);

  return (
    <div className="relative min-h-screen bg-[#0a0e27] overflow-hidden">
      <div className="stars"></div>
      <div className="stars2"></div>
      <div className="stars3"></div>

      <div className="floating-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
        <div className="shape shape-4"></div>
      </div>

      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4">
        <div className="mb-12 relative">
          <div className="logo-glow"></div>
          <div className="w-32 h-32 rounded-full border-4 border-cyan-400 flex items-center justify-center bg-[#0a0e27] relative overflow-hidden">
            <div className="scan-line"></div>
            <div className="mb-0 relative">
              <div className="logo-glow"></div>
              <div className="w-48 h-48 rounded-full border-4 border-cyan-400 flex items-center justify-center bg-[#0a0e27] relative overflow-hidden">
                <div className="scan-line"></div>
                <img 
                    src="/logo.png" 
                    alt="Logo" 
                    className="w-65 h-105 object-contain"
                />
                </div>
              </div>
          </div>
        </div>

        <div className="glass-panel w-full max-w-3xl mb-8 p-8 text-center">
          <h1 className="neon-text text-4xl md:text-5xl font-bold mb-4 tracking-wider">
            SYSTEM UPGRADE IN PROGRESS
          </h1>
          <p className="text-lg md:text-xl">
            <span className="text-yellow-400 font-semibold">QUANTUM CORE</span>
            <span className="text-gray-300"> undergoing </span>
            <span className="text-cyan-400">dimensional recalibration</span>
            <span className="text-gray-300">.</span>
          </p>
        </div>

        <div className="console-box w-full max-w-3xl mb-8 p-6">
          <div className="flex justify-between items-center mb-4">
            <div className="text-green-400 font-mono text-sm">
              {consoleLines[0] || 'INITIALIZING...'}
            </div>
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500 glow-green"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500 glow-yellow"></div>
              <div className="w-3 h-3 rounded-full bg-red-500 glow-red"></div>
            </div>
          </div>
          <div className="space-y-2">
            {consoleLines.slice(1).map((line, index) => (
              <div
                key={index}
                className={`font-mono text-sm fade-in ${
                  line.includes('PROGRESS')
                    ? 'text-yellow-400'
                    : 'text-cyan-400'
                }`}
              >
                {line}
              </div>
            ))}
            {consoleLines.length > 1 && (
              <div className="font-mono text-sm text-yellow-400 flex items-center gap-2">
                <span>&gt; PROGRESS: [{progress}%]</span>
                <div className="flex-1 h-6 bg-black/50 border border-yellow-500/30 rounded overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-yellow-500 to-yellow-300 progress-bar"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>
          <div className="mt-4 font-mono text-xs text-green-400 typing-cursor">
            {progress < 100 ? '_' : 'SYSTEM READY'}
          </div>
        </div>

        <div className="flex gap-6 mt-4">
          <a
            href="#"
            className="social-icon w-14 h-14 border-2 border-cyan-400 rounded-lg flex items-center justify-center hover:bg-cyan-400/20 transition-all"
          >
            <svg className="w-6 h-6 text-cyan-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
          </a>
          <a
            href="#"
            className="social-icon w-14 h-14 border-2 border-cyan-400 rounded-lg flex items-center justify-center hover:bg-cyan-400/20 transition-all"
          >
            <svg className="w-6 h-6 text-cyan-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
          </a>
          <a
            href="#"
            className="social-icon w-14 h-14 border-2 border-cyan-400 rounded-lg flex items-center justify-center hover:bg-cyan-400/20 transition-all"
          >
            <svg className="w-6 h-6 text-cyan-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          </a>
        </div>

        <div className="mt-8 text-xs text-cyan-400/50 font-mono">
          MANDEL'S DESCENDENTS © 2025 | NASA SPACE APPS CHALLENGE
        </div>
      </div>
    </div>
  );
}
