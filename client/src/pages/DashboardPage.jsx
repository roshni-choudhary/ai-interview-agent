import React, { useState, useEffect } from 'react';
import { progressApi } from '../services/api';
import { 
  Sparkles, 
  Flame, 
  CheckCircle2, 
  HelpCircle, 
  ArrowRight,
  TrendingUp,
  BrainCircuit,
  Bookmark
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import TopicBadge from '../components/common/TopicBadge';

const DashboardPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const dbData = await progressApi.getDashboard();
        setData(dbData);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-8rem)]">
        <LoadingSpinner size="lg" text="Loading progress board..." />
      </div>
    );
  }

  const { progress, recent_sessions, topic_breakdown, streak_data } = data || {
    progress: {}, recent_sessions: [], topic_breakdown: [], streak_data: {}
  };

  return (
    <div className="space-y-8 animate-fade-in">
      
      {/* Welcome Banner */}
      <div className="relative p-6 sm:p-8 rounded-2xl bg-gradient-to-r from-accent-600/20 to-cyber-500/10 border border-accent-500/20 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6 overflow-hidden">
        <div className="absolute top-1/2 left-1/4 -translate-y-1/2 w-64 h-64 bg-accent-500/10 rounded-full blur-[80px] pointer-events-none" />
        
        <div className="space-y-2 relative z-10">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-100 flex items-center gap-2">
            Welcome Back, Developer <Sparkles size={20} className="text-accent-400" />
          </h2>
          <p className="text-sm text-slate-400 leading-relaxed max-w-xl">
            Your personalized learning index suggests practicing **Graphs** next to strengthen optimal pathfinders.
          </p>
        </div>

        <Button
          variant="primary"
          size="lg"
          className="relative z-10 shrink-0 flex items-center gap-2 shadow-accent-500/20"
          onClick={() => navigate('/interview/setup')}
        >
          🚀 Launch Interview Session
        </Button>
      </div>

      {/* Aggregate Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        
        <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-accent-400">
            <Flame size={24} className={streak_data.current_streak > 0 ? "animate-pulse" : ""} />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100 font-mono">{streak_data.current_streak || 0}</div>
            <div className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Active Streak</div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-cyber-400">
            <CheckCircle2 size={24} />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100 font-mono">{progress.total_problems_solved || 0}</div>
            <div className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Solved Problems</div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-emerald-400">
            <TrendingUp size={24} />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100 font-mono">
              {progress.total_problems_attempted > 0 
                ? `${Math.round((progress.total_problems_solved / progress.total_problems_attempted) * 100)}%` 
                : '0%'
              }
            </div>
            <div className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Success Rate</div>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-yellow-400">
            <HelpCircle size={24} />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100 font-mono">{progress.total_sessions || 0}</div>
            <div className="text-xs text-slate-500 font-semibold uppercase tracking-wider">Sessions Run</div>
          </div>
        </div>

      </div>

      <div className="grid md:grid-cols-3 gap-6">
        
        {/* Topic Breakdown Index */}
        <div className="glass-panel p-6 rounded-2xl md:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-200 flex items-center gap-2">
              <BrainCircuit size={18} className="text-accent-400" />
              Algorithm Topic Mastery
            </h3>
            <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Accuracy Index</span>
          </div>

          <div className="space-y-4">
            {topic_breakdown.length > 0 ? (
              topic_breakdown.map((t, idx) => (
                <div key={idx} className="space-y-1.5 p-3 rounded-xl bg-slate-900/40 border border-slate-800/40">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-200 capitalize">{t.subject}</span>
                    <span className="text-xs font-bold text-slate-400 font-mono">{Math.round(t.avg_score)}%</span>
                  </div>
                  <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-accent-500 to-cyber-400 rounded-full"
                      style={{ width: `${t.avg_score}%` }}
                    />
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-slate-500">
                    <span>Solved {t.solved} of {t.attempted}</span>
                    <span>Mastery Level: {t.avg_score >= 80 ? 'Elite' : t.avg_score >= 50 ? 'Intermediate' : 'Novice'}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-xs text-slate-500 italic text-center p-8 border border-dashed border-slate-800 rounded-xl">
                No active metrics yet. Execute an interview to compile analytics.
              </div>
            )}
          </div>
        </div>

        {/* Personalized Roadmap */}
        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <h3 className="text-base font-bold text-slate-200 flex items-center gap-2">
            <Bookmark size={18} className="text-cyber-400" />
            AI Suggestion Roadmap
          </h3>
          
          <div className="space-y-4 max-h-[400px] overflow-y-auto pr-1">
            {progress.roadmap && progress.roadmap.length > 0 ? (
              progress.roadmap.map((item, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 flex flex-col justify-between h-36">
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-300 capitalize">{item.topic}</span>
                      <span className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded ${
                        item.priority === 'high' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'
                      }`}>
                        {item.priority}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-2 leading-relaxed">
                      {item.reason}
                    </p>
                  </div>
                  <div className="flex items-center justify-between border-t border-slate-800/80 pt-2 text-[10px] text-slate-500">
                    <span>Solve target: {item.suggested_count} problems</span>
                    <span className="capitalize text-accent-400 font-semibold">{item.difficulty}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-xs text-slate-500 italic text-center p-8 border border-dashed border-slate-800 rounded-xl">
                Roadmap calculations require at least 1 attempted challenge.
              </div>
            )}
          </div>
        </div>

      </div>

      {/* Recent Sessions Table */}
      <div className="glass-panel p-6 rounded-2xl space-y-6">
        <h3 className="text-base font-bold text-slate-200">Recent Interview Logs</h3>
        
        <div className="overflow-x-auto w-full">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-500 font-semibold">
                <th className="py-3 px-4">Topics</th>
                <th className="py-3 px-4">Difficulty</th>
                <th className="py-3 px-4">Score</th>
                <th className="py-3 px-4">Accuracy</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {recent_sessions.length > 0 ? (
                recent_sessions.map((s, idx) => (
                  <tr key={idx} className="border-b border-slate-800/50 hover:bg-slate-900/20">
                    <td className="py-3 px-4 flex gap-1">
                      {s.topics?.map((topic, i) => (
                        <span key={i} className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 capitalize">{topic}</span>
                      ))}
                    </td>
                    <td className="py-3 px-4 capitalize font-medium text-slate-300">{s.difficulty}</td>
                    <td className="py-3 px-4 font-mono font-bold text-accent-400">{Math.round(s.score)}%</td>
                    <td className="py-3 px-4 text-slate-400">{s.correct_answers} / {s.total_questions} Solved</td>
                    <td className="py-3 px-4 text-right">
                      <button 
                        onClick={() => navigate(`/results/${s.id}`)}
                        className="text-cyber-400 hover:text-cyber-300 font-semibold inline-flex items-center gap-1 hover:underline"
                      >
                        Details <ArrowRight size={12} />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="text-center py-6 text-slate-500 italic">
                    No sessions launched. Make your first attempt!
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};

export default DashboardPage;
