import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LogOut, LayoutDashboard, Code2, User } from 'lucide-react';
import Button from '../common/Button';

const Header = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  if (!user) return null;

  const isActive = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 w-full bg-dark-900/60 backdrop-blur-md border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/dashboard" className="flex items-center gap-2 select-none group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-500 to-cyber-400 flex items-center justify-center font-bold text-dark-950 group-hover:scale-105 transition-transform duration-200">
            🤖
          </div>
          <span className="text-lg font-bold bg-gradient-to-r from-slate-100 to-slate-200 bg-clip-text text-transparent group-hover:text-accent-400 transition-colors duration-200">
            AI Interview Agent
          </span>
        </Link>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-1">
          <Link to="/dashboard">
            <span className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-150 flex items-center gap-2 ${
              isActive('/dashboard') 
                ? 'bg-slate-800/80 text-accent-400 font-semibold' 
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/30'
            }`}>
              <LayoutDashboard size={16} />
              Dashboard
            </span>
          </Link>
          <Link to="/interview/setup">
            <span className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-150 flex items-center gap-2 ${
              isActive('/interview/setup') 
                ? 'bg-slate-800/80 text-accent-400 font-semibold' 
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/30'
            }`}>
              <Code2 size={16} />
              New Session
            </span>
          </Link>
        </nav>

        {/* User profile actions */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/50 border border-slate-700/50">
            <User size={14} className="text-accent-400" />
            <span className="text-xs font-semibold text-slate-200">{user.username}</span>
          </div>
          
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={logout}
            className="flex items-center gap-1.5 text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 px-3 py-1.5 rounded-lg"
          >
            <LogOut size={14} />
            <span className="hidden sm:inline">Logout</span>
          </Button>
        </div>
        
      </div>
    </header>
  );
};

export default Header;
