import React, { useState } from 'react';
import { useInterview } from '../context/InterviewContext';
import { Layers, Code, GitCommit, Binary, Share2, Cpu, BarChart, Search, Sparkles } from 'lucide-react';
import Button from '../components/common/Button';

const InterviewSetupPage = () => {
  const [selectedTopics, setSelectedTopics] = useState(['arrays']);
  const [difficulty, setDifficulty] = useState('easy');
  const { startInterview, loading } = useInterview();

  const topicsList = [
    { id: 'arrays', label: 'Arrays & Matrices', icon: <Layers size={18} /> },
    { id: 'strings', label: 'Strings & Hashes', icon: <Code size={18} /> },
    { id: 'linked_lists', label: 'Linked Lists', icon: <GitCommit size={18} /> },
    { id: 'trees', label: 'Trees & traversals', icon: <Binary size={18} /> },
    { id: 'graphs', label: 'Graphs & BFS/DFS', icon: <Share2 size={18} /> },
    { id: 'dynamic_programming', label: 'Dynamic Programming', icon: <Cpu size={18} /> },
    { id: 'sorting', label: 'Sorting algorithms', icon: <BarChart size={18} /> },
    { id: 'searching', label: 'Searching algorithms', icon: <Search size={18} /> }
  ];

  const handleToggleTopic = (topicId) => {
    if (selectedTopics.includes(topicId)) {
      if (selectedTopics.length > 1) {
        setSelectedTopics(selectedTopics.filter(t => t !== topicId));
      }
    } else {
      setSelectedTopics([...selectedTopics, topicId]);
    }
  };

  const handleLaunch = () => {
    startInterview(selectedTopics, difficulty);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      
      {/* Page Header */}
      <div className="space-y-2 text-center md:text-left">
        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-100 flex items-center justify-center md:justify-start gap-2">
          Configure Interview <Sparkles size={22} className="text-accent-400" />
        </h2>
        <p className="text-sm text-slate-400 max-w-xl leading-relaxed">
          Select algorithm topics and difficulty settings. The AI agent will select appropriate questions based on your history.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        
        {/* Topic selector */}
        <div className="glass-panel p-6 rounded-2xl md:col-span-2 space-y-6">
          <h3 className="text-base font-bold text-slate-200 uppercase tracking-wide text-xs">
            1. Select Targeted Topics
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {topicsList.map((t) => {
              const active = selectedTopics.includes(t.id);
              return (
                <div
                  key={t.id}
                  onClick={() => handleToggleTopic(t.id)}
                  className={`p-4 rounded-xl border cursor-pointer select-none transition-all flex items-center gap-4 ${
                    active 
                      ? 'bg-accent-600/10 border-accent-500 text-slate-100' 
                      : 'bg-slate-900/30 border-slate-800 hover:border-slate-700 text-slate-400'
                  }`}
                >
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    active ? 'bg-accent-500/20 text-accent-400' : 'bg-slate-900 text-slate-500'
                  }`}>
                    {t.icon}
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-slate-200">{t.label}</div>
                    <div className="text-[10px] text-slate-500 mt-0.5">Practice catalog pool</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Configurations panel */}
        <div className="glass-panel p-6 rounded-2xl space-y-6 flex flex-col justify-between">
          <div className="space-y-6">
            <h3 className="text-base font-bold text-slate-200 uppercase tracking-wide text-xs">
              2. Select Difficulty
            </h3>
            
            <div className="space-y-2">
              {['easy', 'medium', 'hard'].map((d) => {
                const active = difficulty === d;
                return (
                  <div
                    key={d}
                    onClick={() => setDifficulty(d)}
                    className={`p-3 rounded-lg border cursor-pointer capitalize text-sm text-center font-bold transition-all ${
                      active
                        ? 'bg-gradient-to-r from-accent-600 to-accent-500 text-white border-accent-500 shadow-md shadow-accent-500/10'
                        : 'bg-slate-900/40 border-slate-800 hover:border-slate-700 text-slate-400'
                    }`}
                  >
                    {d}
                  </div>
                );
              })}
            </div>

            <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/80 space-y-2">
              <h4 className="text-xs font-bold text-slate-300">⚡ Adaptive Learning Engine</h4>
              <p className="text-[10px] text-slate-500 leading-relaxed">
                If you solve questions quickly with high accuracy, the AI Interview Agent will automatically upgrade difficulty settings in real-time.
              </p>
            </div>
          </div>

          <Button
            variant="primary"
            size="lg"
            className="w-full mt-6 py-3"
            onClick={handleLaunch}
            loading={loading}
          >
            Start Real-Time Prep
          </Button>
        </div>

      </div>

    </div>
  );
};

export default InterviewSetupPage;
