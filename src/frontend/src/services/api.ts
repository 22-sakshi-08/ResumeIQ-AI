import axios from 'axios';
import type { ATSResult, SkillGap, MatchResult } from '../types';

const API_BASE = 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Mock Fallback Data (used when Backend is offline/not running)
const MOCK_STATS = {
  totalCandidates: 1024,
  averageAtsScore: 72.8,
  topSkills: [
    { name: 'Python', count: 480 },
    { name: 'JavaScript', count: 320 },
    { name: 'React', count: 290 },
    { name: 'Docker', count: 260 },
    { name: 'AWS', count: 220 },
  ],
  activeJobs: 15,
  funnel: [
    { name: 'Screening', value: 500 },
    { name: 'Interview', value: 180 },
    { name: 'Technical', value: 90 },
    { name: 'Offer', value: 25 },
  ],
};

const MOCK_JOBS = [
  {
    job_id: 'JOB_001',
    job_title: 'Machine Learning Engineer',
    jd_text: 'Required: Python, PyTorch, machine learning. 5 years experience.',
  },
  {
    job_id: 'JOB_002',
    job_title: 'Software Engineer',
    jd_text: 'Required: Python, Java, C++, SQL, Git, Docker.',
  },
  {
    job_id: 'JOB_003',
    job_title: 'Data Engineer',
    jd_text: 'Required: Python, Scala, SQL, AWS, Docker, Bash.',
  },
  {
    job_id: 'JOB_004',
    job_title: 'Frontend Developer',
    jd_text: 'Required: JavaScript, TypeScript, React, HTML, CSS, Git.',
  },
  {
    job_id: 'JOB_005',
    job_title: 'DevOps Engineer',
    jd_text: 'Required: Bash, Docker, Kubernetes, AWS, Git.',
  },
];

const MOCK_RESUMES = [
  {
    candidate_id: 'CAND_001',
    name: 'Alex Rivera',
    title: 'Lead Software Engineer',
    resume_text: 'Title: Lead Software Engineer\nSkills: python, java, sql, git, docker\nExperience: 5 years.',
  },
  {
    candidate_id: 'CAND_002',
    name: 'Morgan Patel',
    title: 'Senior Machine Learning Engineer',
    resume_text: 'Title: Senior Machine Learning Engineer\nSkills: python, pytorch, tensorflow, scikit-learn, docker, git\nExperience: 6 years.',
  },
  {
    candidate_id: 'CAND_003',
    name: 'Taylor Chen',
    title: 'Data Engineer Specialist',
    resume_text: 'Title: Data Engineer\nSkills: python, scala, sql, aws, docker, bash\nExperience: 4 years.',
  },
  {
    candidate_id: 'CAND_004',
    name: 'Jordan Smith',
    title: 'Frontend Developer Specialist',
    resume_text: 'Title: Frontend Developer\nSkills: javascript, typescript, react, html, css, git\nExperience: 3 years.',
  },
];

export const apiService = {
  // 1. Predict Role Category
  predictRole: async (resumeText: string): Promise<{ predicted_role: string; confidence: number }> => {
    try {
      const res = await client.post('/predict-role', { resume_text: resumeText });
      return res.data;
    } catch (err) {
      console.warn('API /predict-role offline. Returning mock fallback.', err);
      // Fallback
      if (resumeText.toLowerCase().includes('pytorch') || resumeText.toLowerCase().includes('learning')) {
        return { predicted_role: 'Machine Learning Engineer', confidence: 0.9412 };
      }
      return { predicted_role: 'Software Engineer', confidence: 0.8876 };
    }
  },

  // 2. Predict ATS Score
  predictAtsScore: async (resumeText: string, requiredSkills: string[]): Promise<ATSResult> => {
    try {
      const res = await client.post('/ats-score', {
        resume_text: resumeText,
        required_skills: requiredSkills,
      });
      return res.data;
    } catch (err) {
      console.warn('API /ats-score offline. Returning mock fallback.', err);
      // Fallback
      return {
        ats_score: 74.5,
        breakdown: {
          skill_score: 28.5,
          experience_score: 16.0,
          projects_score: 15.0,
          education_score: 15.0,
        },
      };
    }
  },

  // 3. Extract Skills
  extractSkills: async (text: string): Promise<{ skills: string[] }> => {
    try {
      const res = await client.post('/extract-skills', { text });
      return res.data;
    } catch (err) {
      console.warn('API /extract-skills offline. Returning mock fallback.', err);
      // Fallback matching
      const words = text.toLowerCase();
      const detected = ['python', 'pytorch', 'tensorflow', 'scikit-learn', 'docker', 'git', 'aws', 'kubernetes', 'react', 'javascript']
        .filter(skill => words.includes(skill));
      return { skills: detected.length ? detected : ['python', 'git'] };
    }
  },

  // 4. Job Match
  matchJobs: async (resumeText: string, jobsList?: any[], topK: number = 5): Promise<{ top_jobs: MatchResult[] }> => {
    try {
      const targetJobs = jobsList || MOCK_JOBS;
      const res = await client.post('/job-match', {
        resume_text: resumeText,
        jobs: targetJobs,
        top_k: topK,
      });
      return res.data;
    } catch (err) {
      console.warn('API /job-match offline. Returning mock fallback.', err);
      return {
        top_jobs: [
          {
            job_id: 'JOB_001',
            job_title: 'Machine Learning Engineer',
            semantic_score: 67.2,
            ats_score: 76.0,
            skill_match: 100.0,
            experience_score: 60.0,
            final_score: 75.7,
            rank: 1,
          },
          {
            job_id: 'JOB_003',
            job_title: 'Data Engineer',
            semantic_score: 42.4,
            ats_score: 55.0,
            skill_match: 50.0,
            experience_score: 40.0,
            final_score: 48.5,
            rank: 2,
          },
        ],
      };
    }
  },

  // 5. Candidate Match
  matchCandidates: async (jobDescription: string, resumesList?: any[], topK: number = 5): Promise<{ top_candidates: MatchResult[] }> => {
    try {
      const targetResumes = resumesList || MOCK_RESUMES;
      const res = await client.post('/candidate-match', {
        job_description: jobDescription,
        resumes: targetResumes,
        top_k: topK,
      });
      return res.data;
    } catch (err) {
      console.warn('API /candidate-match offline. Returning mock fallback.', err);
      return {
        top_candidates: [
          {
            candidate_id: 'CAND_002',
            semantic_score: 68.3,
            ats_score: 69.3,
            skill_match: 100.0,
            experience_score: 60.0,
            final_score: 74.1,
            rank: 1,
          },
          {
            candidate_id: 'CAND_001',
            semantic_score: 52.4,
            ats_score: 58.0,
            skill_match: 60.0,
            experience_score: 48.0,
            final_score: 55.2,
            rank: 2,
          },
        ],
      };
    }
  },

  // 6. Skill Gap & Recommendations
  getRecommendations: async (resumeSkills: string[], jdSkills: string[]): Promise<SkillGap & { recommendations: string[] }> => {
    try {
      const res = await client.post('/recommendations', {
        resume_skills: resumeSkills,
        jd_skills: jdSkills,
      });
      return res.data;
    } catch (err) {
      console.warn('API /recommendations offline. Returning mock fallback.', err);
      const matched = resumeSkills.filter(s => jdSkills.includes(s));
      const missing = jdSkills.filter(s => !resumeSkills.includes(s));
      const extra = resumeSkills.filter(s => !jdSkills.includes(s));
      const matchPct = jdSkills.length ? (matched.length / jdSkills.length) * 100 : 0;
      
      const recommendations: string[] = missing.map(skill => {
        if (skill === 'pytorch' || skill === 'tensorflow') return 'Master deep learning platforms: Build CNNs or Transformers.';
        if (skill === 'docker') return 'Learn containerization: Create custom Dockerfiles and build multi-stage images.';
        if (skill === 'kubernetes') return 'Understand orchestration: Set up local k8s pods and ingress controllers.';
        if (skill === 'aws') return 'Gain cloud experience: Complete AWS certifications or deploy EC2/ECS microservices.';
        return `Enhance skills in ${skill}: Complete hands-on tutorials and build portfolio projects.`;
      });

      return {
        matched,
        missing,
        extra,
        match_percentage: round(matchPct, 2),
        recommendations,
      };
    }
  },

  // 6.5. Extract Text from PDF/TXT Upload
  extractTextFromFile: async (file: File): Promise<{ text: string }> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await client.post('/extract-text', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return res.data;
    } catch (err) {
      console.warn('API /extract-text offline. Returning mock fallback.', err);
      if (file.name.endsWith('.pdf')) {
        return {
          text: `Title: Senior Machine Learning Engineer\nSkills: python, pytorch, tensorflow, scikit-learn, docker, git, aws, kubernetes\nExperience: 6 years. Worked on deep learning model architectures, training CNN and Transformer models, and deploying microservices on AWS and Kubernetes.`
        };
      }
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
          const fileContent = event.target?.result;
          if (typeof fileContent === 'string') {
            resolve({ text: fileContent.trim() });
          } else {
            reject(new Error('Failed to read file.'));
          }
        };
        reader.onerror = () => reject(new Error('Failed to read file.'));
        reader.readAsText(file);
      });
    }
  },

  // 7. Dashboard Stats Summary
  getDashboardStats: async () => {
    return MOCK_STATS;
  },

  // 8. Helper to load mock raw JDs/resumes in UI selectors
  getMockJobsList: () => MOCK_JOBS,
  getMockResumesList: () => MOCK_RESUMES,
};

function round(val: number, precision: number): number {
  const factor = Math.pow(10, precision);
  return Math.round(val * factor) / factor;
}
