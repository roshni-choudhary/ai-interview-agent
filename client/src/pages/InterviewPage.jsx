import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useInterview } from '../context/InterviewContext';
import { useTimer } from '../hooks/useTimer';
import Editor from '@monaco-editor/react';
import Sidebar from '../components/layout/Sidebar';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import TopicBadge from '../components/common/TopicBadge';
import { 
  Play, 
  Send, 
  HelpCircle, 
  Terminal as TermIcon, 
  FileText, 
  CheckCircle, 
  XCircle,
  Lightbulb
} from 'lucide-react';

const InterviewPage = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { 
    session, 
    messages, 
    activeQuestion, 
    loading, 
    loadSession, 
    sendChatMessage, 
    submitSolution,
    requestHint 
  } = useInterview();

  const { formatTime } = useTimer();
  const [chatInput, setChatInput] = useState('');
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [activeTab, setActiveTab] = useState('problem'); // problem, results
  const [evalResults, setEvalResults] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (sessionId) {
      loadSession(sessionId);
    }
  }, [sessionId]);

  useEffect(() => {
    // Populate code template once question updates
    if (activeQuestion && activeQuestion.starter_code) {
      setCode(activeQuestion.starter_code[language] || '');
    }
  }, [activeQuestion, language]);

  useEffect(() => {
    // Scroll chat to bottom on new messages
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendChat = (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    sendChatMessage(chatInput.trim());
    setChatInput('');
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setActiveTab('results');
    try {
      const res = await submitSolution(code, language);
      setEvalResults(res);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (!session) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-dark-950">
        <LoadingSpinner size="lg" text="Loading active sandbox..." />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-dark-950">
      
      {/* Sidebar Control Pane */}
      <Sidebar timerValue={formatTime()} />

      {/* Central Workspace Grid */}
      <div className="flex-1 flex flex-col md:flex-row min-w-0">
        
        {/* Left Column: Chat Dialogue (Multi-turn Agent) */}
        <div className="flex-1 flex flex-col border-r border-slate-800 bg-dark-950/20 h-[calc(100vh-4rem)] sticky top-16">
          <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
              Interviewer Dialogue
            </h3>
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider font-mono">Agent Mode</span>
          </div>

          {/* Message Streams */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((msg, idx) => {
              const isAssistant = msg.role === 'assistant';
              return (
                <div key={idx} className={`flex gap-3 max-w-[85%] ${isAssistant ? 'mr-auto' : 'ml-auto flex-row-reverse'}`}>
                  {isAssistant && (
                    <div className="w-8 h-8 rounded-lg bg-accent-500/20 text-accent-400 border border-accent-500/30 flex items-center justify-center font-bold text-xs select-none shrink-0">
                      🤖
                    </div>
                  )}
                  <div>
                    <div className={`p-4 rounded-2xl text-xs leading-relaxed ${
                      isAssistant 
                        ? 'bg-slate-900/60 border border-slate-800 text-slate-200 rounded-tl-none' 
                        : 'bg-accent-600/20 border border-accent-500/20 text-slate-100 rounded-tr-none'
                    }`}>
                      <div className="whitespace-pre-line font-sans">
                        {msg.content}
                      </div>
                    </div>
                    <span className="text-[9px] text-slate-600 mt-1 block select-none px-1">
                      {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              );
            })}
            <div ref={chatEndRef} />
          </div>

          {/* Message Prompt Input */}
          <form onSubmit={handleSendChat} className="p-4 border-t border-slate-800/80 bg-slate-900/10 flex gap-2">
            <input
              type="text"
              placeholder="Discuss logic complexity or ask details..."
              className="flex-1 px-4 py-2.5 bg-slate-900/60 border border-slate-800 focus:border-accent-500 focus:ring-1 focus:ring-accent-500 rounded-lg text-xs text-slate-200 placeholder-slate-600 transition-all outline-none"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
            />
            <Button variant="primary" size="sm" type="submit" className="px-4">
              <Send size={14} />
            </Button>
          </form>
        </div>

        {/* Right Column: Code Editor Workspace */}
        <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] sticky top-16 min-w-0">
          
          {/* Header controls */}
          <div className="px-6 py-3 border-b border-slate-800 flex items-center justify-between shrink-0">
            <div className="flex items-center gap-3">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-slate-900 border border-slate-800 rounded-lg px-2.5 py-1 text-xs text-slate-300 font-semibold focus:border-accent-500 outline-none capitalize"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="cpp">C++</option>
              </select>
            </div>
            
            <div className="flex gap-2">
              <Button
                variant="primary"
                size="sm"
                className="flex items-center gap-1 px-4 bg-emerald-600 hover:bg-emerald-500 hover:to-emerald-400 border-none shadow-emerald-500/10"
                onClick={handleSubmit}
                loading={submitting}
              >
                <Play size={12} /> Run Submission
              </Button>
            </div>
          </div>

          {/* Code Window (Split Editor and Output Tabs) */}
          <div className="flex-1 min-h-0 flex flex-col">
            <div className="flex-1 min-h-0">
              <Editor
                height="100%"
                language={language === 'cpp' ? 'cpp' : language === 'javascript' ? 'javascript' : 'python'}
                theme="vs-dark"
                value={code}
                onChange={(val) => setCode(val || '')}
                options={{
                  fontSize: 13,
                  fontFamily: 'JetBrains Mono',
                  minimap: { enabled: false },
                  automaticLayout: true,
                  scrollbar: {
                    verticalScrollbarSize: 6,
                    horizontalScrollbarSize: 6
                  }
                }}
              />
            </div>

            {/* Test Case Output & Evaluation Results Tabs */}
            <div className="h-64 border-t border-slate-800 bg-slate-950/40 flex flex-col shrink-0">
              <div className="flex border-b border-slate-800 shrink-0">
                <button
                  onClick={() => setActiveTab('problem')}
                  className={`px-4 py-2 text-xs font-semibold flex items-center gap-1.5 transition-colors border-b-2 ${
                    activeTab === 'problem' 
                      ? 'border-accent-500 text-slate-100' 
                      : 'border-transparent text-slate-500 hover:text-slate-300'
                  }`}
                >
                  <FileText size={12} /> Problem Specifications
                </button>
                <button
                  onClick={() => setActiveTab('results')}
                  className={`px-4 py-2 text-xs font-semibold flex items-center gap-1.5 transition-colors border-b-2 ${
                    activeTab === 'results' 
                      ? 'border-accent-500 text-slate-100' 
                      : 'border-transparent text-slate-500 hover:text-slate-300'
                  }`}
                >
                  <TermIcon size={12} /> Compiler Results
                </button>
              </div>

              {/* Tab panels */}
              <div className="flex-1 overflow-y-auto p-4 text-xs">
                {activeTab === 'problem' && activeQuestion && (
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold text-slate-200">Optimal Complexity Target</h4>
                      <div className="flex gap-4 mt-1 font-mono text-[10px] text-accent-400">
                        <span>Time: {activeQuestion.optimal_complexity?.time}</span>
                        <span>Space: {activeQuestion.optimal_complexity?.space}</span>
                      </div>
                    </div>
                    {activeQuestion.constraints && (
                      <div>
                        <h4 className="font-semibold text-slate-200">Constraints check bounds</h4>
                        <ul className="list-disc pl-4 text-slate-400 space-y-0.5 mt-1">
                          {activeQuestion.constraints.map((c, i) => <li key={i}>{c}</li>)}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'results' && (
                  <div className="space-y-4 h-full flex flex-col">
                    {submitting ? (
                      <div className="flex-1 flex items-center justify-center">
                        <LoadingSpinner size="sm" text="Compiling sandbox execution..." />
                      </div>
                    ) : evalResults ? (
                      <div className="space-y-3">
                        <div className="flex items-center gap-2">
                          <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold inline-flex items-center gap-1 ${
                            evalResults.evaluation?.all_passed 
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          }`}>
                            {evalResults.evaluation?.all_passed ? <CheckCircle size={12} /> : <XCircle size={12} />}
                            {evalResults.evaluation?.all_passed ? 'All Cases Passed' : 'Test Failures Identified'}
                          </span>
                          <span className="text-[10px] text-slate-500">
                            Ran in {evalResults.evaluation?.overall_time_ms}ms
                          </span>
                        </div>

                        <div className="space-y-2">
                          {evalResults.evaluation?.results?.map((res, i) => (
                            <div key={i} className="p-3 rounded-lg bg-slate-900 border border-slate-800 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                              <div className="font-mono text-[10px] text-slate-400 truncate max-w-sm">
                                Input: {res.input}
                              </div>
                              <div className="flex items-center gap-4">
                                <div className="text-right text-[10px] font-mono">
                                  <div className="text-slate-500">Expected: {res.expected}</div>
                                  <div className={res.passed ? "text-emerald-400" : "text-rose-400"}>Actual: {res.actual}</div>
                                </div>
                                <span className={`text-[10px] font-bold ${res.passed ? 'text-emerald-400' : 'text-rose-400'}`}>
                                  {res.passed ? '✓ Pass' : '✗ Fail'}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ) : (
                      <div className="flex-1 flex flex-col items-center justify-center text-slate-600 space-y-1">
                        <TermIcon size={24} />
                        <span>Ready to run compiler checks. Click 'Run Submission'.</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};

export default InterviewPage;
