import React, { useState } from 'react';
import { Briefcase, AlertCircle } from 'lucide-react';
import { UploadBox } from '../components/UploadBox';
import { JobCard } from '../components/JobCard';
import { apiService } from '../services/api';
import type { MatchResult } from '../types';

export const JobMatching: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [matches, setMatches] = useState<MatchResult[]>([]);

  const handleMatch = async (text: string) => {
    setLoading(true);
    setError(null);
    try {
      // Fetch mock jobs from services to pass for matching
      const jobs = apiService.getMockJobsList();
      
      const res = await apiService.matchJobs(text, jobs, 5);
      setMatches(res.top_jobs);
    } catch (err: any) {
      console.error(err);
      setError('An error occurred while matching jobs. Please verify API status.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-black text-slate-100">Job Matching</h2>
        <p className="text-xs text-slate-400 mt-1">
          Paste a resume to search, score, and rank matching jobs across active positions.
        </p>
      </div>

      {error && (
        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl flex items-center space-x-2 text-sm">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Upload box */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
            <h3 className="text-sm font-bold text-slate-200 mb-2">Input Resume text</h3>
            <p className="text-[11px] text-slate-500 mb-4">
              Enter details of the resume to find the best job opening matches.
            </p>
            <UploadBox
              onTextSubmit={handleMatch}
              placeholder="Paste candidate resume plain text..."
              submitButtonText="Find Matching Jobs"
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
                Running vector search and scoring JDs...
              </p>
            </div>
          ) : matches.length > 0 ? (
            <div className="space-y-4">
              <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Ranked Job Matches</h3>
              <div className="space-y-4">
                {matches.map((job) => (
                  <JobCard key={job.job_id} job={job} />
                ))}
              </div>
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 p-12 rounded-2xl shadow-xl flex flex-col items-center justify-center text-center space-y-3">
              <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center text-slate-500 border border-slate-700">
                <Briefcase size={28} />
              </div>
              <h3 className="font-bold text-slate-200">No Job Results</h3>
              <p className="text-xs text-slate-500 max-w-sm">
                Paste a resume to index jobs and find the best-matched open titles using vector cosine similarity.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
