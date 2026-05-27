import React from 'react';
import { useInterview } from '../../context/InterviewContext';
import { AlertCircle, BookOpen, Clock, HelpCircle } from 'lucide-react';
import Button from '../common/Button';

const Sidebar = ({ timerValue }) => {
  const { session, activeQuestion, hintsUsed, requestHint, endSession } = useInterview();

  if (!session) return null;

  return (
    <aside className="w-80 border-r border-slate-800 bg-dark-900/40 p-6 flex flex-col h-[calc(100vh-4rem)] sticky top-16">
      
      {/* Session Header Stats */}
      <div className="space-y-4 mb-6">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Session</span>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs px-2 py-0.5 rounded-md font-semibold bg-accent-500/10 text-accent-400 border border-accent-500/20 capitalize">
              {session.difficulty}
            </span>
            <span className="text-xs text-slate-400">
              {session.topics?.join(', ')}
            </span>
          </div>
        </div>

        {/* Stopwatch */}
        <div className="flex items-center gap-3 p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
          <Clock className="text-cyber-400" size={18} />
          <div>
            <div className="text-2xl font-bold font-mono text-slate-100">{timerValue}</div>
            <div className="text-xs text-slate-500 font-medium">Session duration elapsed</div>
          </div>
        </div>
      </div>

      <hr className="border-slate-800/80 mb-6" />

      {/* Active Question Info */}
      <div className="flex-1 flex flex-col min-h-0">
        <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 flex items-center gap-2">
          <BookOpen size={12} />
          Active Problem
        </h4>
        
        {activeQuestion ? (
          <div className="bg-slate-900/30 border border-slate-800/60 rounded-xl p-4 flex-1 overflow-y-auto mb-6">
            <h5 className="font-semibold text-sm text-slate-200">{activeQuestion.title}</h5>
            <span className="inline-block mt-1.5 text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 capitalize">
              {activeQuestion.topic}
            </span>
            <div className="text-xs text-slate-400 mt-3 leading-relaxed max-h-48 overflow-y-auto pr-1">
              {activeQuestion.description ? (
                activeQuestion.description.length > 180 
                  ? activeQuestion.description.substring(0, 180) + '...' 
                  : activeQuestion.description
              ) : ''}
            </div>
          </div>
        ) : (
          <div className="text-xs text-slate-500 italic p-4 text-center border border-dashed border-slate-800 rounded-xl flex-1 mb-6 flex items-center justify-center">
            Initializing algorithm challenge...
          </div>
        )}

        {/* Hint helper system */}
        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800/60 mb-6">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400 font-semibold flex items-center gap-1.5">
              <HelpCircle size={14} className="text-accent-400" />
              Hints Used
            </span>
            <span className="text-xs font-bold text-slate-300 font-mono">
              {hintsUsed} / 3
            </span>
          </div>
          
          <Button
            variant="secondary"
            size="sm"
            className="w-full mt-3 flex items-center justify-center gap-1 bg-slate-800/60 hover:bg-slate-700/60 border-slate-700"
            onClick={requestHint}
            disabled={hintsUsed >= 3}
          >
            💡 Request Next Hint
          </Button>
          <div className="text-[10px] text-slate-500 mt-2 text-center">
            Each hint provides progressive pseudo-structural context.
          </div>
        </div>
      </div>

      {/* End Session CTA */}
      <div className="pt-4 border-t border-slate-800/80">
        <Button 
          variant="danger" 
          size="md" 
          className="w-full flex items-center justify-center gap-2 bg-rose-600/10 hover:bg-rose-600 hover:text-white text-rose-400 border border-rose-500/20"
          onClick={endSession}
        >
          <AlertCircle size={16} />
          End Session & Review
        </Button>
      </div>

    </aside>
  );
};

export default Sidebar;
