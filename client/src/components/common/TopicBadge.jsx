import React from 'react';
import { 
  Code, 
  Layers, 
  GitCommit, 
  Binary, 
  Share2, 
  Cpu, 
  Search, 
  Database,
  BarChart
} from 'lucide-react';

const TopicBadge = ({ topic, className = '' }) => {
  const normalized = topic?.toLowerCase().replace('_', ' ') || '';
  
  const getIcon = () => {
    switch (normalized) {
      case 'arrays':
        return <Layers size={12} />;
      case 'strings':
        return <Code size={12} />;
      case 'linked lists':
        return <GitCommit size={12} />;
      case 'trees':
        return <Binary size={12} />;
      case 'graphs':
        return <Share2 size={12} />;
      case 'dynamic programming':
        return <Cpu size={12} />;
      case 'sorting':
        return <BarChart size={12} />;
      case 'searching':
        return <Search size={12} />;
      default:
        return <Database size={12} />;
    }
  };

  const getStyle = () => {
    switch (normalized) {
      case 'arrays':
        return 'bg-blue-500/10 text-blue-400 border border-blue-500/20';
      case 'strings':
        return 'bg-green-500/10 text-green-400 border border-green-500/20';
      case 'linked lists':
        return 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20';
      case 'trees':
        return 'bg-purple-500/10 text-purple-400 border border-purple-500/20';
      case 'graphs':
        return 'bg-pink-500/10 text-pink-400 border border-pink-500/20';
      case 'dynamic programming':
        return 'bg-rose-500/10 text-rose-400 border border-rose-500/20';
      default:
        return 'bg-slate-500/10 text-slate-400 border border-slate-500/20';
    }
  };

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full capitalize ${getStyle()} ${className}`}>
      {getIcon()}
      {normalized}
    </span>
  );
};

export default TopicBadge;
