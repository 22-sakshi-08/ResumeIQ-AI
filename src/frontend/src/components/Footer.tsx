import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="py-4 px-6 border-t border-slate-800/60 bg-slate-950/20 text-center text-xs text-slate-500">
      <p>&copy; {new Date().getFullYear()} ResumeIQ AI. All rights reserved. Designed for Advanced Recruiter Analytics.</p>
    </footer>
  );
};
