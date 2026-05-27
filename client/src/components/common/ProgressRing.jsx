import React from 'react';

const ProgressRing = ({ 
  radius = 60, 
  stroke = 10, 
  progress = 0, 
  colorClass = 'text-accent-500', 
  trailColorClass = 'text-slate-800' 
}) => {
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (Math.min(progress, 100) / 100) * circumference;

  return (
    <svg
      height={radius * 2}
      width={radius * 2}
      className="transform -rotate-90 select-none"
    >
      {/* Background ring */}
      <circle
        className={`${trailColorClass} stroke-current`}
        fill="transparent"
        strokeWidth={stroke}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
      {/* Active progress ring */}
      <circle
        className={`${colorClass} stroke-current transition-all duration-500 ease-out`}
        fill="transparent"
        strokeWidth={stroke}
        strokeDasharray={circumference + ' ' + circumference}
        style={{ strokeDashoffset }}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
        strokeLinecap="round"
      />
    </svg>
  );
};

export default ProgressRing;
