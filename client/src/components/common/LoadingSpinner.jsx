import React from 'react';

const LoadingSpinner = ({ size = 'md', text = 'Processing...' }) => {
  const sizes = {
    sm: 'w-6 h-6 border-2',
    md: 'w-10 h-10 border-3',
    lg: 'w-16 h-16 border-4'
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-4 p-6">
      <div className={`relative ${size === 'lg' ? 'w-16 h-16' : size === 'sm' ? 'w-6 h-6' : 'w-10 h-10'}`}>
        <div className={`absolute inset-0 rounded-full border-t-accent-500 border-r-transparent border-b-cyber-400 border-l-transparent animate-spin ${sizes[size]}`} />
        <div className={`absolute inset-1 rounded-full border border-slate-800 opacity-20`} />
      </div>
      {text && <span className="text-slate-400 text-sm font-medium animate-pulse">{text}</span>}
    </div>
  );
};

export default LoadingSpinner;
