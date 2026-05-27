import { useState, useEffect, useRef } from 'react';

export const useTimer = (initialSeconds = 0) => {
  const [seconds, setSeconds] = useState(initialSeconds);
  const [isRunning, setIsRunning] = useState(true);
  const timerRef = useRef(null);

  useEffect(() => {
    if (isRunning) {
      timerRef.current = setInterval(() => {
        setSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isRunning]);

  const start = () => setIsRunning(true);
  const pause = () => setIsRunning(false);
  const reset = () => setSeconds(0);

  const formatTime = () => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return {
    seconds,
    isRunning,
    start,
    pause,
    reset,
    formatTime
  };
};
