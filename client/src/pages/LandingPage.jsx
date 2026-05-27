import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Terminal, 
  Cpu, 
  Sparkles, 
  Compass, 
  LineChart, 
  TrendingUp 
} from 'lucide-react';
import Button from '../components/common/Button';

const LandingPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleStart = () => {
    if (user) {
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  };

  const features = [
    {
      icon: <Terminal className="text-accent-400" size={24} />,
      title: "Adaptive Interview System",
      description: "Our AI adjusts algorithm difficulty in real-time as you solve, simulating high-pressure elite technical interviews."
    },
    {
      icon: <Cpu className="text-cyber-400" size={24} />,
      title: "Local Execution Sandbox",
      description: "Submit solutions directly. Run Python, JavaScript, and C++ with real unit checks and sub-second feedback loop."
    },
    {
      icon: <Sparkles className="text-pink-400" size={24} />,
      title: "AI-generated Progressive Hints",
      description: "Access 3-tier contextual hints ranging from high-level pattern recognition to detailed algorithm guides."
    },
    {
      icon: <Compass className="text-yellow-400" size={24} />,
      title: "Personalized Roadmap",
      description: "Receive AI recommendation roadmaps targeting weak structures (DP, Graphs, Heaps) to build well-rounded mastery."
    },
    {
      icon: <LineChart className="text-indigo-400" size={24} />,
      title: "Weak-Topic Analytics Tracker",
      description: "Uncover exactly where your logic gaps exist with topic accuracy, average score cards, and active streak boards."
    },
    {
      icon: <TrendingUp className="text-emerald-400" size={24} />,
      title: "Contest Simulation",
      description: "Practice under real stopwatch conditions with custom-selected topics to prepare for actual technical interviews."
    }
  ];

  return (
    <div className="relative min-h-[calc(100vh-4rem)] flex flex-col justify-center py-12 px-6">
      
      {/* Background Neon Glowing Particles */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-accent-500/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-10 left-1/4 w-[300px] h-[300px] bg-cyber-500/5 rounded-full blur-[100px] pointer-events-none" />

      {/* Hero Section */}
      <div className="text-center max-w-4xl mx-auto space-y-6 relative z-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-semibold text-accent-400 mb-4 animate-glow-pulse">
          ⚡ Elite Agentic AI Preparation
        </div>
        
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight leading-none text-slate-100">
          Master Your Coding Interview with{" "}
          <span className="bg-gradient-to-r from-accent-400 via-accent-500 to-cyber-400 bg-clip-text text-transparent">
            Agentic AI
          </span>
        </h1>
        
        <p className="text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Skip generic coding loops. Experience a live, highly-adaptive technical coding interview agent 
          that scores logic structures, analyzes complexity, and designs personalized learning paths.
        </p>

        <div className="flex justify-center gap-4 pt-6">
          <Button 
            variant="primary" 
            size="lg" 
            className="px-8 shadow-accent-600/30"
            onClick={handleStart}
          >
            {user ? 'Go to Dashboard' : 'Start Practicing'}
          </Button>
          <Button 
            variant="secondary" 
            size="lg" 
            onClick={() => navigate('/login')}
          >
            Sign In / Register
          </Button>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-6xl mx-auto mt-24 grid md:grid-cols-3 gap-6 relative z-10">
        {features.map((feat, idx) => (
          <div 
            key={idx} 
            className="glass-panel p-6 rounded-2xl flex flex-col justify-between hover:scale-[1.02] transition-transform duration-200"
          >
            <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center mb-6">
              {feat.icon}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-200 mb-2">{feat.title}</h3>
              <p className="text-sm text-slate-400 leading-relaxed">{feat.description}</p>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
};

export default LandingPage;
