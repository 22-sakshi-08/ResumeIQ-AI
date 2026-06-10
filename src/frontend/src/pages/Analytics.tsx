import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend
} from 'recharts';

export const Analytics: React.FC = () => {
  // 1. ATS Score Trends over time (monthly averages)
  const atsTrendData = [
    { month: 'Jan', avgScore: 68 },
    { month: 'Feb', avgScore: 70 },
    { month: 'Mar', avgScore: 71 },
    { month: 'Apr', avgScore: 74 },
    { month: 'May', avgScore: 73 },
    { month: 'Jun', avgScore: 75 },
  ];

  // 2. Candidate Categories distribution
  const categoryData = [
    { name: 'Software Engineer', value: 340 },
    { name: 'ML Engineer', value: 210 },
    { name: 'Data Scientist', value: 180 },
    { name: 'DevOps Engineer', value: 120 },
    { name: 'Frontend Dev', value: 174 },
  ];

  // 3. Match Scores Radar
  const radarData = [
    { subject: 'Skills Match', CandidateA: 88, CandidateB: 60, fullMark: 100 },
    { subject: 'Experience', CandidateA: 72, CandidateB: 85, fullMark: 100 },
    { subject: 'Education', CandidateA: 95, CandidateB: 70, fullMark: 100 },
    { subject: 'ATS Keywords', CandidateA: 80, CandidateB: 65, fullMark: 100 },
    { subject: 'Semantic Similarity', CandidateA: 78, CandidateB: 90, fullMark: 100 },
  ];

  // 4. Skills distribution (horizontal bar chart)
  const skillsData = [
    { name: 'Python', count: 420 },
    { name: 'React', count: 310 },
    { name: 'Docker', count: 280 },
    { name: 'AWS', count: 240 },
    { name: 'SQL', count: 210 },
    { name: 'Kubernetes', count: 180 },
  ];

  const PIE_COLORS = ['#8b5cf6', '#6366f1', '#3b82f6', '#10b981', '#f59e0b'];
  const BAR_COLORS = ['#8b5cf6', '#6366f1', '#3b82f6', '#10b981', '#f59e0b', '#ec4899'];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-black text-slate-100">Recruiting Analytics</h2>
        <p className="text-xs text-slate-400 mt-1">
          Detailed metrics showing candidate scores, category distributions, and core skill overlaps.
        </p>
      </div>

      {/* Grid: Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: ATS Score Trend */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100">Average ATS Score Trend</h3>
            <p className="text-[10px] text-slate-500">Monthly average candidate scores (0-100 scale).</p>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={atsTrendData} margin={{ left: -20, right: 10, top: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#475569" className="text-[10px]" />
                <YAxis domain={[50, 90]} stroke="#475569" className="text-[10px]" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                  labelStyle={{ color: '#94a3b8', fontWeight: 'bold' }}
                />
                <Line type="monotone" dataKey="avgScore" stroke="#8b5cf6" strokeWidth={3} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Skills Distribution */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100">Skills Frequency</h3>
            <p className="text-[10px] text-slate-500">Total counts of technical keywords identified.</p>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={skillsData} margin={{ left: -20, right: 10, top: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#475569" className="text-[10px]" />
                <YAxis stroke="#475569" className="text-[10px]" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                  labelStyle={{ color: '#94a3b8', fontWeight: 'bold' }}
                />
                <Bar dataKey="count" fill="#8b5cf6" radius={[6, 6, 0, 0]}>
                  {skillsData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={BAR_COLORS[index % BAR_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 3: Candidate Categories */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100">Candidate Role Categories</h3>
            <p className="text-[10px] text-slate-500">Breakdown of parsed candidate profiles by predicted role.</p>
          </div>
          <div className="h-64 flex items-center justify-center">
            <div className="w-full h-full flex flex-col md:flex-row items-center justify-around">
              <div className="w-48 h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={70}
                      paddingAngle={4}
                      dataKey="value"
                    >
                      {categoryData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                      labelStyle={{ color: '#94a3b8', fontWeight: 'bold' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Legend List */}
              <div className="space-y-1.5 text-xs">
                {categoryData.map((cat, index) => (
                  <div key={cat.name} className="flex items-center space-x-2">
                    <span
                      className="w-2.5 h-2.5 rounded-full inline-block"
                      style={{ backgroundColor: PIE_COLORS[index % PIE_COLORS.length] }}
                    />
                    <span className="text-slate-450">{cat.name}</span>
                    <span className="text-slate-500 font-bold">({cat.value})</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Chart 4: Radar Match Profile */}
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100">Candidate Comparison Profile</h3>
            <p className="text-[10px] text-slate-500">Radar comparison overlays for top candidate profile scores.</p>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" stroke="#64748b" className="text-[9px] font-bold" />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" className="text-[9px]" />
                <Radar name="Candidate A" dataKey="CandidateA" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.2} />
                <Radar name="Candidate B" dataKey="CandidateB" stroke="#10b981" fill="#10b981" fillOpacity={0.2} />
                <Legend className="text-[10px]" wrapperStyle={{ paddingTop: '10px' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
