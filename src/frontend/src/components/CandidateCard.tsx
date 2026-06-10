import React from 'react';
import { User, CheckCircle } from 'lucide-react';
import type { MatchResult } from '../types';

interface CandidateCardProps {
  candidate: MatchResult;
}

export const CandidateCard: React.FC<CandidateCardProps> = ({ candidate }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 hover:border-slate-700 p-5 rounded-2xl transition-all shadow-md flex items-center justify-between">
      <div className="flex items-center space-x-4">
        {/* Profile Avatar */}
        <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center text-brand-400 border border-slate-700">
          <User size={20} />
        </div>
        
        <div>
          <h3 className="font-bold text-slate-100 text-base flex items-center space-x-2">
            <span>Candidate {candidate.candidate_id}</span>
            <span className="text-xs bg-brand-500/10 border border-brand-500/20 text-brand-400 px-2.5 py-0.5 rounded-full font-semibold">
              Rank {candidate.rank}
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-1 flex items-center space-x-1">
            <CheckCircle size={12} className="text-emerald-500" />
            <span>Matched {candidate.skill_match}% required skills</span>
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="flex items-center space-x-6">
        <div className="text-center">
          <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Semantic Match</p>
          <p className="text-sm font-semibold text-slate-300">{candidate.semantic_score}%</p>
        </div>
        
        <div className="text-center pl-6 border-l border-slate-800">
          <p className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">ATS Score</p>
          <p className="text-sm font-semibold text-slate-300">{candidate.ats_score}%</p>
        </div>
        
        <div className="text-center pl-6 border-l border-slate-800 bg-brand-500/5 px-4 py-1.5 rounded-xl border border-brand-500/10">
          <p className="text-[10px] text-brand-400 uppercase font-bold tracking-wider">Final Score</p>
          <p className="text-lg font-black text-brand-400">{candidate.final_score}%</p>
        </div>
      </div>
    </div>
  );
};
