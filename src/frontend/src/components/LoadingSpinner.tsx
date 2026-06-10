import React from 'react';

interface LoadingSpinnerProps {
  message?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ message = 'Processing data...' }) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 space-y-4">
      {/* Outer spinning ring */}
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 border-4 border-brand-500/10 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-transparent border-t-brand-500 rounded-full animate-spin"></div>
      </div>
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest animate-pulse">{message}</p>
    </div>
  );
};
