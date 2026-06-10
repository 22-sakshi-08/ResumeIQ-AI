export interface Candidate {
  candidate_id: str;
  resume_text: str;
  name?: string;
  email?: string;
  title?: string;
}

export type str = string;

export interface Job {
  job_id: string;
  job_title: string;
  jd_text: string;
}

export interface ATSResult {
  ats_score: number;
  breakdown: {
    skill_score: number;
    experience_score: number;
    projects_score: number;
    education_score: number;
  };
  predicted_role?: string;
  confidence?: number;
}

export interface SkillGap {
  matched: string[];
  missing: string[];
  extra: string[];
  match_percentage: number;
}

export interface MatchResult {
  job_id?: string;
  candidate_id?: string;
  job_title?: string;
  semantic_score: number;
  ats_score: number;
  skill_match: number;
  experience_score: number;
  final_score: number;
  rank: number;
}

export interface Recommendation {
  skills: string[];
  recommendations: string[];
}
