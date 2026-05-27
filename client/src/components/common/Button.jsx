import React from 'react';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  loading = false, 
  disabled = false, 
  onClick,
  ...props 
}) => {
  const baseStyle = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed select-none';
  
  const variants = {
    primary: 'bg-gradient-to-r from-accent-600 to-accent-500 hover:from-accent-500 hover:to-accent-400 text-white shadow-lg shadow-accent-500/20 active:scale-95',
    secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-100 border border-slate-700 active:scale-95',
    cyber: 'bg-gradient-to-r from-cyber-500 to-cyber-400 hover:from-cyber-400 hover:to-cyber-500 text-dark-950 font-semibold shadow-lg shadow-cyber-500/20 active:scale-95',
    danger: 'bg-rose-600 hover:bg-rose-500 text-white shadow-lg shadow-rose-600/25 active:scale-95',
    ghost: 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/50'
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  };

  return (
    <button
      className={`${baseStyle} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading ? (
        <>
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          Loading...
        </>
      ) : children}
    </button>
  );
};

export default Button;
