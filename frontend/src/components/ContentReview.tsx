import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ContentReview.css';

interface ContentReviewProps {
  companyId: number;
}

interface ContentData {
  id?: number;
  topic: string;
  platform: string;
  prompt?: string;
  caption?: string;
  referenceImages?: string[];
}

function ContentReview({ companyId }: ContentReviewProps) {
  const navigate = useNavigate();
  const [contentData, setContentData] = useState<ContentData | null>(null);
  const [editingPrompt, setEditingPrompt] = useState(false);
  const [editingCaption, setEditingCaption] = useState(false);
  const [prompt, setPrompt] = useState('');
  const [caption, setCaption] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    // Load content data from session storage or fetch from API
    const stored = sessionStorage.getItem('pendingContent');
    if (stored) {
      const data = JSON.parse(stored);
      setContentData(data);
      setPrompt(data.prompt || '');
      setCaption(data.caption || '');
    } else {
      // If no stored data, fetch from API
      fetchContentData();
    }
  }, []);

  const fetchContentData = async () => {
    try {
      const response = await fetch(`/api/content/latest?companyId=${companyId}`);
      if (response.ok) {
        const data = await response.json();
        setContentData(data);
        setPrompt(data.prompt || '');
        setCaption(data.caption || '');
      }
    } catch (error) {
      console.error('Error fetching content:', error);
    }
  };

  const handleSave = async () => {
    if (!contentData) return;

    try {
      setSaving(true);
      const response = await fetch('/api/content/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: contentData.id,
          companyId,
          topic: contentData.topic,
          platform: contentData.platform,
          prompt,
          caption,
        }),
      });

      if (response.ok) {
        alert('Content saved successfully!');
        sessionStorage.removeItem('pendingContent');
        navigate('/content');
      } else {
        alert('Failed to save content');
      }
    } catch (error) {
      console.error('Error saving content:', error);
      alert('Error saving content');
    } finally {
      setSaving(false);
    }
  };

  const handleCopyPrompt = async () => {
    if (!prompt) return;
    try {
      await navigator.clipboard.writeText(prompt);
    } catch (error) {
      console.error('Error copying prompt to clipboard:', error);
    }
  };

  const handleCopyCaption = async () => {
    if (!caption) return;
    try {
      await navigator.clipboard.writeText(caption);
    } catch (error) {
      console.error('Error copying caption to clipboard:', error);
    }
  };

  if (!contentData) {
    return (
      <div className="cr-wrapper">
        <div className="loading">Loading content...</div>
      </div>
    );
  }

  return (
    <div className="cr-wrapper">
      <h1>Review Generated Content</h1>

      <div className="cr-review-section">
        <div className="cr-content-info">
          <div className="cr-info-item">
            <span className="cr-info-label">Topic:</span>
            <span className="cr-info-value">{contentData.topic}</span>
          </div>
          <div className="cr-info-item">
            <span className="cr-info-label">Platform:</span>
            <span className="cr-info-value">
              {contentData.platform.charAt(0).toUpperCase() + contentData.platform.slice(1)}
            </span>
          </div>
        </div>

        <div className="cr-content-editor">
          <div className="cr-editor-section">
            <div className="cr-editor-header">
              <h3>Content Prompt</h3>
              <div className="cr-editor-actions">
                <button
                  className="btn btn-secondary btn-small"
                  onClick={() => setEditingPrompt(!editingPrompt)}
                >
                  {editingPrompt ? 'Cancel' : 'Edit'}
                </button>
                <button
                  className="btn btn-secondary btn-small"
                  type="button"
                  onClick={handleCopyPrompt}
                  disabled={!prompt}
                >
                  Copy
                </button>
              </div>
            </div>
            {editingPrompt ? (
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="cr-editor-textarea"
                rows={8}
                placeholder="Enter content prompt..."
              />
            ) : (
              <div className="cr-content-display" style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f9f9f9', padding: '12px', borderRadius: '4px', minHeight: '100px', lineHeight: '1.6' }}>
                {prompt || <span className="cr-placeholder">No prompt generated</span>}
              </div>
            )}
          </div>

          <div className="cr-editor-section">
            <div className="cr-editor-header">
              <h3>Caption</h3>
              <div className="cr-editor-actions">
                <button
                  className="btn btn-secondary btn-small"
                  onClick={() => setEditingCaption(!editingCaption)}
                >
                  {editingCaption ? 'Cancel' : 'Edit'}
                </button>
                <button
                  className="btn btn-secondary btn-small"
                  type="button"
                  onClick={handleCopyCaption}
                  disabled={!caption}
                >
                  Copy
                </button>
              </div>
            </div>
            {editingCaption ? (
              <textarea
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                className="cr-editor-textarea"
                rows={6}
                placeholder="Enter caption..."
              />
            ) : (
              <div className="cr-content-display" style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f9f9f9', padding: '12px', borderRadius: '4px', minHeight: '80px', lineHeight: '1.6' }}>
                {caption || <span className="cr-placeholder">No caption generated</span>}
              </div>
            )}
          </div>
        </div>

        <div className="cr-action-buttons">
          <button
            className="btn btn-secondary"
            onClick={() => navigate('/content')}
          >
            Back to Create
          </button>
          <button
            className="btn btn-primary"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Confirm & Save'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ContentReview;
