import React, { useState } from 'react';
import { UploadCloud, Clipboard } from 'lucide-react';
import { apiService } from '../services/api';

interface UploadBoxProps {
  onTextSubmit: (text: string) => void;
  placeholder?: string;
  submitButtonText?: string;
  loading?: boolean;
}

export const UploadBox: React.FC<UploadBoxProps> = ({
  onTextSubmit,
  placeholder = "Paste resume text or job description details here...",
  submitButtonText = "Analyze",
  loading = false
}) => {
  const [text, setText] = useState('');
  const [parsing, setParsing] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !loading && !parsing) {
      onTextSubmit(text);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setParsing(true);
      try {
        if (file.name.endsWith('.pdf')) {
          const res = await apiService.extractTextFromFile(file);
          setText(res.text);
        } else {
          const reader = new FileReader();
          reader.onload = (event) => {
            const fileContent = event.target?.result;
            if (typeof fileContent === 'string') {
              setText(fileContent.trim());
            }
          };
          reader.readAsText(file);
        }
      } catch (err) {
        console.error('Error loading file:', err);
        alert('Failed to extract text from file.');
      } finally {
        setParsing(false);
      }
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Text Area */}
        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Paste Plain Text Content
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder={placeholder}
            rows={8}
            className="w-full bg-slate-950 border border-slate-800 focus:border-brand-500 focus:ring-1 focus:ring-brand-500 rounded-xl p-4 text-slate-100 placeholder-slate-600 text-sm transition-all focus:outline-none resize-y"
            disabled={loading || parsing}
          />
        </div>

        {/* Upload and Submit Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
          {/* File Upload Trigger */}
          <div className="relative flex items-center justify-center w-full sm:w-auto">
            <label className="w-full sm:w-auto flex items-center justify-center space-x-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-750 text-slate-350 border border-slate-700 hover:border-slate-650 rounded-xl text-sm font-semibold transition-all cursor-pointer">
              <UploadCloud size={16} />
              <span>{parsing ? 'Extracting...' : 'Load Resume (.pdf, .txt)'}</span>
              <input
                type="file"
                accept=".txt,.pdf"
                onChange={handleFileUpload}
                className="hidden"
                disabled={loading || parsing}
              />
            </label>
          </div>

          {/* Submit button */}
          <button
            type="submit"
            disabled={!text.trim() || loading || parsing}
            className="w-full sm:w-auto px-6 py-2.5 bg-brand-600 hover:bg-brand-500 disabled:bg-slate-800 text-white font-bold rounded-xl text-sm transition-all flex items-center justify-center space-x-2 shadow-lg shadow-brand-500/20 disabled:shadow-none"
          >
            <Clipboard size={16} />
            <span>{loading ? 'Analyzing...' : submitButtonText}</span>
          </button>
        </div>
      </form>
    </div>
  );
};
