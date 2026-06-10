import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileSearch, Briefcase, Users, BarChart2, Cpu } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const links = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/analyze', label: 'Resume Analyzer', icon: FileSearch },
    { to: '/job-match', label: 'Job Matching', icon: Briefcase },
    { to: '/candidate-search', label: 'Candidate Search', icon: Users },
    { to: '/analytics', label: 'Analytics', icon: BarChart2 },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950 flex flex-col h-screen sticky top-0">
      {/* Brand Logo */}
      <div className="h-16 flex items-center px-6 border-b border-slate-980 space-x-2">
        <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white shadow-lg shadow-brand-500/30">
          <Cpu size={18} />
        </div>
        <div>
          <span className="font-bold text-slate-100 tracking-tight text-lg">Resume<span className="text-brand-400">IQ</span></span>
          <span className="text-[10px] block text-slate-500 font-medium -mt-1">Recruiter Panel</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-brand-600 text-white shadow-lg shadow-brand-600/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/50'
                }`
              }
            >
              <Icon size={18} />
              <span>{link.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-900 text-center">
        <p className="text-[10px] text-slate-600 font-semibold uppercase tracking-widest">Version 1.0.0</p>
      </div>
    </aside>
  );
};
