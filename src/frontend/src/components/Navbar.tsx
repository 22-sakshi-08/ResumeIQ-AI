import React from 'react';
import { User, Bell, Shield } from 'lucide-react';

interface NavbarProps {
  title: string;
}

export const Navbar: React.FC<NavbarProps> = ({ title }) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/50 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center space-x-2">
        <h1 className="text-xl font-bold text-slate-100 uppercase tracking-wider">{title}</h1>
      </div>
      
      <div className="flex items-center space-x-4">
        {/* Shield Badge */}
        <div className="flex items-center space-x-1 text-xs bg-brand-500/10 border border-brand-500/20 text-brand-400 px-2.5 py-1 rounded-full">
          <Shield size={12} />
          <span className="font-semibold">Recruiter Space</span>
        </div>

        {/* Notifications */}
        <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 rounded-lg transition-colors relative">
          <Bell size={18} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-brand-500 rounded-full"></span>
        </button>

        {/* User Info */}
        <div className="flex items-center space-x-3 pl-2 border-l border-slate-800">
          <div className="text-right hidden sm:block">
            <p className="text-xs font-semibold text-slate-200">Alex Recruiter</p>
            <p className="text-[10px] text-slate-500">Talent Acquisition</p>
          </div>
          <div className="w-8 h-8 rounded-full bg-brand-600 flex items-center justify-center text-white font-bold text-sm shadow-md shadow-brand-500/20">
            <User size={16} />
          </div>
        </div>
      </div>
    </header>
  );
};
