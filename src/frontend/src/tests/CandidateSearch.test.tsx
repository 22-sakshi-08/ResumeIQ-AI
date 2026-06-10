import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { CandidateSearch } from '../pages/CandidateSearch';

describe('CandidateSearch Component', () => {
  it('renders initial setup text and submit controls', () => {
    render(<CandidateSearch />);
    expect(screen.getByText('Candidate Search')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Paste job description text here...')).toBeInTheDocument();
  });

  it('retrieves and ranks candidate cards when job description is analyzed', async () => {
    render(<CandidateSearch />);
    
    const textarea = screen.getByPlaceholderText('Paste job description text here...');
    const submitBtn = screen.getByRole('button', { name: 'Search Candidates' });
    
    fireEvent.change(textarea, { target: { value: 'Required: Python, PyTorch, machine learning. 5 years experience.' } });
    fireEvent.click(submitBtn);
    
    await waitFor(() => {
      expect(screen.getByText('Ranked Candidate Matches')).toBeInTheDocument();
      // Should find first match (e.g. CAND_002)
      expect(screen.getByText('Candidate CAND_002')).toBeInTheDocument();
      // Should find second match (e.g. CAND_001)
      expect(screen.getByText('Candidate CAND_001')).toBeInTheDocument();
    });
  });
});
