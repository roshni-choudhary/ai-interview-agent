import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, User, Terminal } from 'lucide-react';
import Button from '../components/common/Button';

const LoginPage = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, register, loading } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!username || !password || (isRegister && !email)) {
      setError('Please fill in all fields.');
      return;
    }

    try {
      if (isRegister) {
        await register(username, email, password);
      } else {
        await login(username, password);
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify credentials.');
    }
  };

  const handleGuestMode = async () => {
    // Guest auto registration logic
    const rnd = Math.floor(1000 + Math.random() * 9000);
    const guestUser = `developer_${rnd}`;
    const guestEmail = `dev_${rnd}@sandbox.io`;
    const guestPass = 'Developer@123';
    
    setError('');
    try {
      await register(guestUser, guestEmail, guestPass);
    } catch (err) {
      // If user randomly exists, attempt auto-login
      try {
        await login(guestUser, guestPass);
      } catch (logErr) {
        setError('Auto guest connection failed. Please register manually.');
      }
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-6 relative">
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[400px] h-[400px] bg-accent-500/5 rounded-full blur-[80px] pointer-events-none" />
      
      <div className="w-full max-w-md glass-panel p-8 rounded-2xl shadow-xl border border-slate-800/80 relative z-10 animate-fade-in">
        
        {/* Form Header */}
        <div className="text-center space-y-2 mb-8">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-500 to-accent-600 flex items-center justify-center font-bold text-dark-950 mx-auto select-none">
            🤖
          </div>
          <h2 className="text-2xl font-bold text-slate-100">
            {isRegister ? 'Create Developer Account' : 'Sign In to Sandbox'}
          </h2>
          <p className="text-sm text-slate-400">
            {isRegister ? 'Start practicing structured coding challenges' : 'Access your personalized learning roadmap'}
          </p>
        </div>

        {error && (
          <div className="p-3 mb-6 rounded-lg bg-rose-500/10 border border-rose-500/20 text-xs font-semibold text-rose-400 text-center">
            {error}
          </div>
        )}

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Username</label>
            <div className="relative">
              <User size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                placeholder="e.g. hackercat"
                className="w-full pl-10 pr-4 py-2.5 bg-slate-900/60 border border-slate-800 focus:border-accent-500 focus:ring-1 focus:ring-accent-500 rounded-lg text-slate-200 placeholder-slate-600 transition-all outline-none"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
          </div>

          {isRegister && (
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Email Address</label>
              <div className="relative">
                <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="email"
                  placeholder="e.g. dev@sandbox.io"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900/60 border border-slate-800 focus:border-accent-500 focus:ring-1 focus:ring-accent-500 rounded-lg text-slate-200 placeholder-slate-600 transition-all outline-none"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
          )}

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Password</label>
            <div className="relative">
              <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="password"
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 bg-slate-900/60 border border-slate-800 focus:border-accent-500 focus:ring-1 focus:ring-accent-500 rounded-lg text-slate-200 placeholder-slate-600 transition-all outline-none"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <Button 
            variant="primary" 
            size="md" 
            className="w-full py-3 mt-4" 
            type="submit" 
            loading={loading}
          >
            {isRegister ? 'Register Account' : 'Authenticate Credentials'}
          </Button>

        </form>

        {/* Guest and Toggles */}
        <div className="mt-6 flex flex-col space-y-4">
          <Button
            variant="secondary"
            size="md"
            className="w-full flex items-center justify-center gap-2 bg-slate-800/40 text-cyber-400 hover:bg-slate-800 hover:text-cyber-500 border-dashed border-slate-700"
            onClick={handleGuestMode}
          >
            <Terminal size={14} />
            Quick Guest Demo Launch
          </Button>
          
          <div className="text-center">
            <button
              onClick={() => {
                setError('');
                setIsRegister(!isRegister);
              }}
              className="text-xs text-slate-400 hover:text-accent-400 font-semibold"
            >
              {isRegister ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default LoginPage;
