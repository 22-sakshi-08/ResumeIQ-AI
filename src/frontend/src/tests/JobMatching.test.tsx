import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { JobMatching } from '../pages/JobMatching';

describe('JobMatching Component', () => {
  it('renders initial setup instructions and textbox', () => {
    render(<JobMatching />);
    expect(screen.getByText('Job Matching')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Paste candidate resume plain text...')).toBeInTheDocument();
  });

  it('shows ranked job matched cards on resume submission', async () => {
    render(<JobMatching />);
    
    const textarea = screen.getByPlaceholderText('Paste candidate resume plain text...');
    const submitBtn = screen.getByRole('button', { name: 'Find Matching Jobs' });
    
    fireEvent.change(textarea, { target: { value: 'Python developer with PyTorch. 5 years experience.' } });
    fireEvent.click(submitBtn);
    
    await waitFor(() => {
      expect(screen.getByText('Ranked Job Matches')).toBeInTheDocument();
      // Should find first match (e.g. Machine Learning Engineer)
      expect(screen.getByText('Machine Learning Engineer')).toBeInTheDocument();
      // Should find second match (e.g. Data Engineer)
      expect(screen.getByText('Data Engineer')).toBeInTheDocument();
    });
  });
});
