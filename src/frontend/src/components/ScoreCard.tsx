import React from 'react';

interface ScoreCardProps {
  score: number;
  label: string;
  size?: number;
  strokeWidth?: number;
  colorClass?: string;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({
  score,
  label,
  size = 120,
  strokeWidth = 10,
  colorClass = 'stroke-brand-500'
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-4 bg-slate-900 border border-slate-800 rounded-2xl shadow-lg">
      <div className="relative" style={{ width: size, height: size }}>
        {/* SVG Circle */}
        <svg className="w-full h-full transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className="stroke-slate-800"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            className={`transition-all duration-1000 ease-out ${colorClass}`}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>
        
        {/* Score Value Display */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-2xl font-black text-slate-100">{Math.round(score)}%</span>
        </div>
      </div>
      <span className="mt-3 text-xs font-semibold text-slate-400 uppercase tracking-widest">{label}</span>
    </div>
  );
};
