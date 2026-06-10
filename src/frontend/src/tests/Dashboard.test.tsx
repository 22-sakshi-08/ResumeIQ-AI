import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Dashboard } from '../pages/Dashboard';

// Mock Recharts ResponsiveContainer to render simply
vi.mock('recharts', () => ({
  ResponsiveContainer: ({ children }: any) => <div>{children}</div>,
  BarChart: ({ children }: any) => <div>{children}</div>,
  Bar: () => <div>Bar</div>,
  XAxis: () => <div>XAxis</div>,
  YAxis: () => <div>YAxis</div>,
  Tooltip: () => <div>Tooltip</div>,
  Cell: () => <div>Cell</div>,
}));

describe('Dashboard Component', () => {
  it('renders stats loading state initially', () => {
    render(<Dashboard />);
    // Loading indicator is present
    expect(document.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('renders KPI cards and funnel metrics after load', async () => {
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Total Candidates')).toBeInTheDocument();
      expect(screen.getByText('Active Jobs')).toBeInTheDocument();
      expect(screen.getByText('Average ATS Score')).toBeInTheDocument();
    });
    
    // Check mocked stats values from apiService
    expect(screen.getByText('1024')).toBeInTheDocument();
    expect(screen.getByText('72.8%')).toBeInTheDocument();
    expect(screen.getByText('15')).toBeInTheDocument();
  });
});
