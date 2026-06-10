import React from 'react';

interface SkillBadgeProps {
  name: string;
  type: 'matched' | 'missing' | 'extra' | 'default';
}

export const SkillBadge: React.FC<SkillBadgeProps> = ({ name, type }) => {
  const styles = {
    matched: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
    missing: 'bg-rose-500/10 border-rose-500/30 text-rose-400',
    extra: 'bg-blue-500/10 border-blue-500/30 text-blue-400',
    default: 'bg-slate-800 border-slate-700 text-slate-300'
  };

  return (
    <span className={`px-2.5 py-1 text-xs font-semibold rounded-full border transition-all ${styles[type]}`}>
      {name}
    </span>
  );
};
