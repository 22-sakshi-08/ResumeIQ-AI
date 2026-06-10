import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ResumeAnalyzer } from '../pages/ResumeAnalyzer';

describe('ResumeAnalyzer Component', () => {
  it('renders paste textbox and instructions', () => {
    render(<ResumeAnalyzer />);
    expect(screen.getByText('Resume Analyzer')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Paste plain text resume content...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Analyze Resume' })).toBeInTheDocument();
  });

  it('performs parsing and shows results when text is submitted', async () => {
    render(<ResumeAnalyzer />);
    
    const textarea = screen.getByPlaceholderText('Paste plain text resume content...');
    const submitBtn = screen.getByRole('button', { name: 'Analyze Resume' });
    
    // Simulate paste
    fireEvent.change(textarea, { target: { value: 'Jane Developer. Python, React, Git, Docker, Kubernetes. 5 years experience.' } });
    
    // Click submit
    fireEvent.click(submitBtn);
    
    // Check loading indicator or results
    await waitFor(() => {
      // Role prediction fallback matches
      expect(screen.getByText('Classification Outcome')).toBeInTheDocument();
      expect(screen.getByText('Overall ATS Score')).toBeInTheDocument();
      // Should show ATS Score (e.g. 75%)
      expect(screen.getByText('75%')).toBeInTheDocument();
    });
  });
});
