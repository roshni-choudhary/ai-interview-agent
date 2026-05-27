import React, { createContext, useContext, useState } from 'react';
import { interviewApi } from '../services/api';
import { useNavigate } from 'react-router-dom';

const InterviewContext = createContext(null);

export const InterviewProvider = ({ children }) => {
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [activeQuestion, setActiveQuestion] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hintsUsed, setHintsUsed] = useState(0);
  const navigate = useNavigate();

  const startInterview = async (topics, difficulty) => {
    setLoading(true);
    try {
      const data = await interviewApi.start(topics, difficulty);
      setSession(data);
      setMessages(data.messages || []);
      
      // Look for latest question in messages metadata
      const qMsg = [...(data.messages || [])]
        .reverse()
        .find(m => m.message_type === 'question' && m.metadata_json);
        
      if (qMsg && qMsg.metadata_json) {
        setActiveQuestion(qMsg.metadata_json);
      }
      
      setHintsUsed(0);
      navigate(`/interview/${data.id}`);
    } catch (err) {
      console.error(err);
      alert('Failed to initialize session. Please check parameters.');
    } finally {
      setLoading(false);
    }
  };

  const loadSession = async (sessionId) => {
    setLoading(true);
    try {
      const data = await interviewApi.getSession(sessionId);
      setSession(data);
      setMessages(data.messages || []);
      
      const qMsg = [...(data.messages || [])]
        .reverse()
        .find(m => m.message_type === 'question' && m.metadata_json);
        
      if (qMsg && qMsg.metadata_json) {
        setActiveQuestion(qMsg.metadata_json);
      }
      
      const hCount = (data.messages || []).filter(m => m.message_type === 'hint').length;
      setHintsUsed(hCount);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const sendChatMessage = async (content) => {
    if (!session) return;
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content,
      message_type: 'chat',
      created_at: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMsg]);
    
    try {
      const reply = await interviewApi.sendMessage(session.id, content);
      setMessages(prev => [...prev, reply]);
    } catch (err) {
      console.error(err);
    }
  };

  const submitSolution = async (code, language) => {
    if (!session) return;
    setLoading(true);
    try {
      const res = await interviewApi.submitCode(session.id, code, language);
      
      // Update session/messages to get the new feedback and next question
      await loadSession(session.id);
      return res;
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const requestHint = async () => {
    if (!session) return;
    try {
      const hint = await interviewApi.requestHint(session.id);
      setMessages(prev => [...prev, hint]);
      setHintsUsed(prev => prev + 1);
      return hint;
    } catch (err) {
      console.error(err);
    }
  };

  const endSession = async () => {
    if (!session) return;
    setLoading(true);
    try {
      await interviewApi.endSession(session.id);
      navigate(`/results/${session.id}`);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <InterviewContext.Provider value={{
      session,
      messages,
      activeQuestion,
      loading,
      hintsUsed,
      startInterview,
      loadSession,
      sendChatMessage,
      submitSolution,
      requestHint,
      endSession
    }}>
      {children}
    </InterviewContext.Provider>
  );
};

export const useInterview = () => useContext(InterviewContext);
