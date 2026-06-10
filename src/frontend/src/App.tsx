import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';

// Pages
import { Dashboard } from './pages/Dashboard';
import { ResumeAnalyzer } from './pages/ResumeAnalyzer';
import { JobMatching } from './pages/JobMatching';
import { CandidateSearch } from './pages/CandidateSearch';
import { Analytics } from './pages/Analytics';

export const App: React.FC = () => {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-950 text-slate-100">
      {/* Sidebar navigation */}
      <Sidebar />

      {/* Main Content Pane */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Navbar */}
        <Navbar title="ResumeIQ AI" />

        {/* Dynamic page routes container */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 bg-slate-950">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyze" element={<ResumeAnalyzer />} />
            <Route path="/job-match" element={<JobMatching />} />
            <Route path="/candidate-search" element={<CandidateSearch />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="*" element={<Dashboard />} />
          </Routes>
        </main>

        {/* Footer */}
        <Footer />
      </div>
    </div>
  );
};
