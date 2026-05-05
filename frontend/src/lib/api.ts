/**
 * API client for Law Analyse backend
 */

const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

export interface Law {
  id: string;
  title: string;
  document_number?: string;
  publication_date?: string;
  issuing_body?: string;
  processing_status: string;
  created_at: string;
}

export interface Article {
  id: string;
  law_id: string;
  article_number: string;
  title?: string;
  full_text: string;
  hierarchy_path?: string[];
  norms: Norm[];
}

export interface Norm {
  id: string;
  article_id: string;
  norm_text: string;
  subject: string;
  simplified_explanation: string;
  confidence_score: number;
  needs_human_review: boolean;
}

export interface LawDetail extends Law {
  articles: Article[];
}

export const api = {
  async getLaws(): Promise<Law[]> {
    const response = await fetch(`${API_URL}/laws/`);
    if (!response.ok) throw new Error('Failed to fetch laws');
    return response.json();
  },

  async getLaw(id: string): Promise<LawDetail> {
    const response = await fetch(`${API_URL}/laws/${id}`);
    if (!response.ok) throw new Error('Failed to fetch law');
    return response.json();
  },

  async getArticles(lawId: string): Promise<Article[]> {
    const response = await fetch(`${API_URL}/articles/law/${lawId}`);
    if (!response.ok) throw new Error('Failed to fetch articles');
    return response.json();
  },

  async getArticle(id: string): Promise<Article> {
    const response = await fetch(`${API_URL}/articles/${id}`);
    if (!response.ok) throw new Error('Failed to fetch article');
    return response.json();
  },

  async getProcessingStatus(lawId: string) {
    const response = await fetch(`${API_URL}/process/${lawId}/status`);
    if (!response.ok) throw new Error('Failed to fetch status');
    return response.json();
  }
};
