import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { interviewApi } from '../services/api';
import { 
  CheckCircle, 
  HelpCircle, 
  Clock, 
  ArrowRight, 
  RotateCcw,
  Sparkles,
  TrendingUp,
  AlertCircle
} from 'lucide-react';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ProgressRing from '../components/common/ProgressRing';

const ResultsPage = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await interviewApi.endSession(sessionId);
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, [sessionId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-8rem)]">
        <LoadingSpinner size="lg" text="Compiling structural evaluation..." />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="max-w-md mx-auto text-center space-y-4 p-8 glass-panel rounded-2xl">
        <AlertCircle size={40} className="mx-auto text-rose-500" />
        <h3 className="text-lg font-bold text-slate-200">Evaluation session record missing</h3>
        <p className="text-xs text-slate-400">Failed to aggregate attempts from database.</p>
        <Button variant="secondary" size="sm" onClick={() => navigate('/dashboard')}>
          Back to Dashboard
        </Button>
      </div>
    );
  }

  const score = Math.round(data.score || 0.0);
  const durationMins = Math.floor(data.duration_seconds / 60);

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      
      {/* Score Dashboard Card */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-8 relative overflow-hidden">
        <div className="absolute top-1/2 left-1/4 -translate-y-1/2 w-64 h-64 bg-accent-500/10 rounded-full blur-[80px] pointer-events-none" />
        
        <div className="space-y-4 text-center md:text-left relative z-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-semibold text-accent-400">
            ⚡ Performance Index Verified
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-100">
            Structural Session Summary
          </h2>
          <p className="text-xs text-slate-400 max-w-md leading-relaxed">
            Your logical constructs and time complexities are logged on your learning timeline to adapt future challenges.
          </p>
        </div>

        {/* Circular score ring */}
        <div className="relative shrink-0 select-none scale-90 sm:scale-100">
          <ProgressRing 
            radius={80} 
            stroke={12} 
            progress={score} 
            colorClass={score >= 80 ? 'text-emerald-400' : score >= 50 ? 'text-accent-500' : 'text-rose-500'} 
          />
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-4xl font-extrabold text-slate-100 font-mono leading-none">{score}%</span>
            <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider mt-1">Average Score</span>
          </div>
        </div>
      </div>

      {/* Numerical logs details */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        
        <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-accent-400 shrink-0">
            <CheckCircle size={24} />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-100 font-mono">
              {data.correct_answers} / {data.total_questions}
            </div>
            <div className="text-xs text-slate-500 font-medium">Challenges Solved</div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-cyber-400 shrink-0">
            <Clock size={24} />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-100 font-mono">
              {durationMins} min
            </div>
            <div className="text-xs text-slate-500 font-medium">Timing Elapsed</div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-yellow-500 shrink-0">
            <TrendingUp size={24} />
          </div>
          <div>
            <div className="text-xl font-bold text-slate-100 font-mono">
              {data.difficulty.toUpperCase()}
            </div>
            <div className="text-xs text-slate-500 font-medium">Target Difficulty</div>
          </div>
        </div>

      </div>

      {/* AI Post Attempt recommendations */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl space-y-6">
        <h3 className="text-base font-bold text-slate-200 flex items-center gap-2">
          <Sparkles size={18} className="text-accent-400" />
          AI Interviewer Recommendations & Logic Gaps
        </h3>
        
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/80 leading-relaxed text-slate-300 text-xs">
          Your single-pass array complements was highly efficient. However, during the dynamic backtracking, 
          you triggered hints to handle subproblem coin boundary allocations. Focus on **Dynamic Programming base exercises** 
          prior to scaling complexity upwards.
        </div>

        <div className="grid md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-900/20 border border-slate-800 space-y-2">
            <h4 className="font-bold text-emerald-400">💡 Strengths identified</h4>
            <ul className="list-disc pl-4 text-slate-400 space-y-1">
              <li>Excellent linear space optimization profiles.</li>
              <li>Syntactically correct boundary structures.</li>
            </ul>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/20 border border-slate-800 space-y-2">
            <h4 className="font-bold text-yellow-400">📈 Logic expansion opportunities</h4>
            <ul className="list-disc pl-4 text-slate-400 space-y-1">
              <li>Exhaustive memoization maps mapping duplicates.</li>
              <li>Recursive stack checks for potential array pointer exceptions.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-4">
        <Button
          variant="primary"
          size="md"
          className="flex-1 py-3 flex items-center justify-center gap-2 shadow-accent-500/10"
          onClick={() => navigate('/interview/setup')}
        >
          <RotateCcw size={16} /> Practice Again
        </Button>
        <Button
          variant="secondary"
          size="md"
          className="flex-1 py-3 flex items-center justify-center gap-2"
          onClick={() => navigate('/dashboard')}
        >
          View Progress Dashboard <ArrowRight size={16} />
        </Button>
      </div>

    </div>
  );
};

export default ResultsPage;
