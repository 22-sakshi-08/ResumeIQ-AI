import React, { useState } from 'react';
import { ShieldCheck, Award, AlertCircle, Bookmark } from 'lucide-react';
import { UploadBox } from '../components/UploadBox';
import { ScoreCard } from '../components/ScoreCard';
import { SkillBadge } from '../components/SkillBadge';
import { apiService } from '../services/api';
import type { ATSResult } from '../types';

export const ResumeAnalyzer: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [roleResult, setRoleResult] = useState<{ predicted_role: string; confidence: number } | null>(null);
  const [atsResult, setAtsResult] = useState<ATSResult | null>(null);
  const [extractedSkills, setExtractedSkills] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<string[]>([]);

  const handleAnalyze = async (text: string) => {
    setLoading(true);
    setError(null);
    try {
      // 1. Predict role category
      const role = await apiService.predictRole(text);
      setRoleResult(role);

      // 2. Extract skills
      const skillsRes = await apiService.extractSkills(text);
      setExtractedSkills(skillsRes.skills);

      // 3. Score ATS relative to extracted skills (using them as baseline required ones for matching)
      const ats = await apiService.predictAtsScore(text, skillsRes.skills);
      setAtsResult(ats);

      // 4. Generate recommendations (matching against a generic senior role baseline skills)
      const targetSkills = ['python', 'aws', 'docker', 'kubernetes', 'pytorch', 'git'];
      const recs = await apiService.getRecommendations(skillsRes.skills, targetSkills);
      setRecommendations(recs.recommendations);
    } catch (err: any) {
      console.error(err);
      setError('An error occurred during analysis. Please check the backend connectivity.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-black text-slate-100">Resume Analyzer</h2>
        <p className="text-xs text-slate-400 mt-1">
          Perform statistical role classification, parse skills, and predict ATS scores.
        </p>
      </div>

      {error && (
        <div className="bg-rose-500/10 border border-rose-500/20 text-rose-450 p-4 rounded-xl flex items-center space-x-2 text-sm">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {/* Main content grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Upload box col */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
            <h3 className="text-sm font-bold text-slate-200 mb-2">Input Candidate Resume</h3>
            <p className="text-[11px] text-slate-500 mb-4">
              Paste the text content or load a .txt file to run intelligence parsing.
            </p>
            <UploadBox
              onTextSubmit={handleAnalyze}
              placeholder="Paste plain text resume content..."
              submitButtonText="Analyze Resume"
              loading={loading}
            />
          </div>
        </div>

        {/* Results col */}
        <div className="lg:col-span-2 space-y-6">
          {loading ? (
            <div className="bg-slate-900 border border-slate-800 p-12 rounded-2xl shadow-xl flex flex-col items-center justify-center space-y-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-500"></div>
              <p className="text-xs text-slate-400 font-semibold tracking-wider uppercase animate-pulse">
                Parsing resume text and predicting scores...
              </p>
            </div>
          ) : roleResult && atsResult ? (
            <div className="space-y-6">
              {/* ATS Scores and Predicted Category */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* predicted role */}
                <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl flex flex-col justify-between shadow-xl">
                  <div>
                    <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Classification Outcome</h4>
                    <p className="text-xl font-black text-brand-400 mt-4 leading-tight">{roleResult.predicted_role}</p>
                  </div>
                  <div className="mt-4 flex items-center space-x-2 text-xs text-slate-400">
                    <ShieldCheck size={14} className="text-emerald-500" />
                    <span>Confidence: {(roleResult.confidence * 100).toFixed(2)}%</span>
                  </div>
                </div>

                {/* ATS Circle */}
                <div className="md:col-span-2 bg-slate-900 border border-slate-800 p-6 rounded-2xl flex items-center justify-around shadow-xl">
                  <ScoreCard score={atsResult.ats_score} label="Overall ATS Score" />
                  
                  {/* Breakdown details */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-3">ATS Score Breakdown</h4>
                    <div className="grid grid-cols-2 gap-4 text-xs">
                      <div>
                        <span className="block text-slate-500">Skills Score</span>
                        <span className="font-semibold text-slate-200">{atsResult.breakdown.skill_score} / 40</span>
                      </div>
                      <div>
                        <span className="block text-slate-500">Experience Score</span>
                        <span className="font-semibold text-slate-200">{atsResult.breakdown.experience_score} / 25</span>
                      </div>
                      <div>
                        <span className="block text-slate-500">Projects Score</span>
                        <span className="font-semibold text-slate-200">{atsResult.breakdown.projects_score} / 20</span>
                      </div>
                      <div>
                        <span className="block text-slate-500">Education Score</span>
                        <span className="font-semibold text-slate-200">{atsResult.breakdown.education_score} / 15</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Extracted Skills */}
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Extracted Candidate Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {extractedSkills.map(skill => (
                    <SkillBadge key={skill} name={skill} type="matched" />
                  ))}
                  {extractedSkills.length === 0 && (
                    <p className="text-xs text-slate-600">No skills parsed from this text.</p>
                  )}
                </div>
              </div>

              {/* Learning Recommendations */}
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Dynamic Learning Tracks</h4>
                <div className="space-y-2">
                  {recommendations.map((rec, idx) => (
                    <div key={idx} className="flex items-start space-x-3 text-xs bg-slate-950 p-3.5 rounded-xl border border-slate-850">
                      <Bookmark size={14} className="text-brand-400 mt-0.5 flex-shrink-0" />
                      <p className="text-slate-350">{rec}</p>
                    </div>
                  ))}
                  {recommendations.length === 0 && (
                    <div className="flex items-center space-x-2 text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-3 rounded-xl">
                      <Award size={14} />
                      <span>This resume is optimized! No major gaps detected against senior skill profiles.</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 p-12 rounded-2xl shadow-xl flex flex-col items-center justify-center text-center space-y-3">
              <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center text-slate-500 border border-slate-700">
                <ShieldCheck size={28} />
              </div>
              <h3 className="font-bold text-slate-200">No Report Generated</h3>
              <p className="text-xs text-slate-500 max-w-sm">
                Analyze a resume to generate an interactive profile classification and scoring report.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
