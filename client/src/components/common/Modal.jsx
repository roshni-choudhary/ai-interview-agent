import React from 'react';
import { X } from 'lucide-react';

const Modal = ({ 
  isOpen, 
  onClose, 
  title, 
  children, 
  footer, 
  size = 'md' 
}) => {
  if (!isOpen) return null;

  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-xl',
    lg: 'max-w-3xl',
    full: 'max-w-full m-4'
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-dark-950/70 backdrop-blur-md animate-fade-in">
      <div className={`w-full ${sizes[size]} glass-panel-heavy rounded-2xl shadow-2xl overflow-hidden transform animate-slide-up`}>
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
          <button 
            onClick={onClose}
            className="text-slate-400 hover:text-slate-100 transition-colors duration-150"
          >
            <X size={20} />
          </button>
        </div>
        
        {/* Body */}
        <div className="px-6 py-6 overflow-y-auto max-h-[70vh]">
          {children}
        </div>
        
        {/* Footer */}
        {footer && (
          <div className="flex items-center justify-end gap-3 px-6 py-4 bg-slate-900/40 border-t border-slate-800">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};

export default Modal;
