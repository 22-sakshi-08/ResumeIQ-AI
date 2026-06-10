import React from 'react';
import { Briefcase, ShieldCheck } from 'lucide-react';
import type { MatchResult } from '../types';

interface JobCardProps {
  job: MatchResult;
}

export const JobCard: React.FC<JobCardProps> = ({ job }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 hover:border-slate-700 p-5 rounded-2xl transition-all shadow-md flex items-center justify-between">
      <div className="flex items-center space-x-4">
        {/* Job Icon */}
        <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center text-brand-400 border border-slate-700">
          <Briefcase size={20} />
        </div>
        
        <div>
          <h3 className="font-bold text-slate-100 text-base flex items-center space-x-2">
            <span>{job.job_title}</span>
            <span className="text-xs bg-slate-800 border border-slate-700 text-slate-400 px-2 py-0.5 rounded-md font-mono">
              {job.job_id}
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-1 flex items-center space-x-1">
            <ShieldCheck size={12} className="text-brand-400" />
            <span>Rank {job.rank} best fit</span>
          </p>
        </div>
      </div>

      {/* Scores breakdown */}
      <div className="flex items-center space-x-6">
        <div className="text-center">
          <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Semantic Match</p>
          <p className="text-sm font-semibold text-slate-300">{job.semantic_score}%</p>
        </div>
        
        <div className="text-center pl-6 border-l border-slate-800">
          <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Skill Match</p>
          <p className="text-sm font-semibold text-slate-300">{job.skill_match}%</p>
        </div>
        
        <div className="text-center pl-6 border-l border-slate-800 bg-brand-500/5 px-4 py-1.5 rounded-xl border border-brand-500/10">
          <p className="text-[10px] text-brand-400 uppercase font-bold tracking-wider">Final Match</p>
          <p className="text-lg font-black text-brand-400">{job.final_score}%</p>
        </div>
      </div>
    </div>
  );
};
