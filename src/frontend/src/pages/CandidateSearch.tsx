import React, { useState } from 'react';
import { Users, AlertCircle } from 'lucide-react';
import { UploadBox } from '../components/UploadBox';
import { CandidateCard } from '../components/CandidateCard';
import { apiService } from '../services/api';
import type { MatchResult } from '../types';

export const CandidateSearch: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matches, setMatches] = useState<MatchResult[]>([]);

  const handleMatch = async (text: string) => {
    setLoading(true);
    setError(null);
    try {
      // Get resumes list for matching
      const resumes = apiService.getMockResumesList();
      
      const res = await apiService.matchCandidates(text, resumes, 5);
      setMatches(res.top_candidates);
    } catch (err: any) {
      console.error(err);
      setError('An error occurred during candidate matching. Check API server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-black text-slate-100">Candidate Search</h2>
        <p className="text-xs text-slate-400 mt-1">
          Search candidate databases semantically using a job description.
        </p>
      </div>

      {error && (
        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-450 p-4 rounded-xl flex items-center space-x-2 text-sm">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Upload box */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
            <h3 className="text-sm font-bold text-slate-200 mb-2">Input Job Details</h3>
            <p className="text-[11px] text-slate-500 mb-4">
              Enter target requirements to find candidate matches using semantic FAISS vectors.
            </p>
            <UploadBox
              onTextSubmit={handleMatch}
              placeholder="Paste job description text here..."
              submitButtonText="Search Candidates"
              loading={loading}
            />
          </div>
        </div>

        {/* Results */}
        <div className="lg:col-span-2 space-y-4">
          {loading ? (
            <div className="bg-slate-900 border border-slate-800 p-12 rounded-2xl shadow-xl flex flex-col items-center justify-center space-y-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-500"></div>
              <p className="text-xs text-slate-400 font-semibold tracking-wider uppercase animate-pulse">
                Running semantic search and scoring candidates...
              </p>
            </div>
          ) : matches.length > 0 ? (
            <div className="space-y-4">
              <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Ranked Candidate Matches</h3>
              <div className="space-y-4">
                {matches.map((cand) => (
                  <CandidateCard key={cand.candidate_id} candidate={cand} />
                ))}
              </div>
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 p-12 rounded-2xl shadow-xl flex flex-col items-center justify-center text-center space-y-3">
              <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center text-slate-500 border border-slate-700">
                <Users size={28} />
              </div>
              <h3 className="font-bold text-slate-200">No Candidates Found</h3>
              <p className="text-xs text-slate-500 max-w-sm">
                Enter target job details to perform recruiter-style candidate matches against indexed profiles.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
