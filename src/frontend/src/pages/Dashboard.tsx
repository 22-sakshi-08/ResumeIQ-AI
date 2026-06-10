import React, { useEffect, useState } from 'react';
import { Users, FileText, Cpu, Star } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import { apiService } from '../services/api';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await apiService.getDashboardStats();
        setStats(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center min-h-[500px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-500"></div>
      </div>
    );
  }

  const kpis = [
    { label: 'Total Candidates', value: stats.totalCandidates, icon: Users, color: 'text-indigo-400 bg-indigo-500/10' },
    { label: 'Average ATS Score', value: `${stats.averageAtsScore}%`, icon: Star, color: 'text-amber-400 bg-amber-500/10' },
    { label: 'Active Jobs', value: stats.activeJobs, icon: FileText, color: 'text-emerald-400 bg-emerald-500/10' },
    { label: 'Hiring Pipeline', value: 'Active', icon: Cpu, color: 'text-brand-400 bg-brand-500/10' }
  ];

  const colors = ['#8b5cf6', '#6366f1', '#3b82f6', '#10b981', '#f59e0b'];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-black text-slate-100">Recruiter Dashboard</h2>
        <p className="text-xs text-slate-400 mt-1">Overview of parsed candidates, ATS scores, and talent matches.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div key={idx} className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest">{kpi.label}</p>
                <p className="text-3xl font-black text-slate-100 mt-2">{kpi.value}</p>
              </div>
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${kpi.color}`}>
                <Icon size={22} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Funnel chart card */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
          <div>
            <h3 className="text-base font-bold text-slate-100">Hiring Funnel</h3>
            <p className="text-[11px] text-slate-500">Distribution of candidates through review phases.</p>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.funnel} layout="vertical" margin={{ left: 10, right: 30, top: 10, bottom: 10 }}>
                <XAxis type="number" stroke="#475569" className="text-[10px]" />
                <YAxis dataKey="name" type="category" stroke="#475569" className="text-[10px]" width={80} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                  labelStyle={{ color: '#94a3b8', fontWeight: 'bold' }}
                />
                <Bar dataKey="value" fill="#8b5cf6" radius={[0, 8, 8, 0]}>
                  {stats.funnel.map((_: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top skills chart card */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
          <div>
            <h3 className="text-base font-bold text-slate-100">Top Candidate Skills</h3>
            <p className="text-[11px] text-slate-500">Most common canonical skills discovered in resume sets.</p>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.topSkills} margin={{ top: 10, bottom: 10, left: 0, right: 10 }}>
                <XAxis dataKey="name" stroke="#475569" className="text-[10px]" />
                <YAxis stroke="#475569" className="text-[10px]" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                  labelStyle={{ color: '#94a3b8', fontWeight: 'bold' }}
                />
                <Bar dataKey="count" fill="#8b5cf6" radius={[8, 8, 0, 0]}>
                  {stats.topSkills.map((_: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
