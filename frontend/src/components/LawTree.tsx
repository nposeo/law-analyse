import { useState } from 'react';
import type { Article } from '../lib/api';

interface LawTreeProps {
  articles: Article[];
  onArticleSelect: (article: Article) => void;
}

export default function LawTree({ articles, onArticleSelect }: LawTreeProps) {
  const [expandedArticles, setExpandedArticles] = useState<Set<string>>(new Set());
  const [selectedArticleId, setSelectedArticleId] = useState<string | null>(null);

  const toggleArticle = (articleId: string) => {
    const newExpanded = new Set(expandedArticles);
    if (newExpanded.has(articleId)) {
      newExpanded.delete(articleId);
    } else {
      newExpanded.add(articleId);
    }
    setExpandedArticles(newExpanded);
  };

  const handleArticleClick = (article: Article) => {
    setSelectedArticleId(article.id);
    onArticleSelect(article);
    if (!expandedArticles.has(article.id)) {
      toggleArticle(article.id);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-4 py-3 bg-gray-50 border-b">
        <h3 className="font-semibold text-gray-900">Статті закону</h3>
      </div>
      <div className="divide-y max-h-[600px] overflow-y-auto">
        {articles.map((article) => {
          const isExpanded = expandedArticles.has(article.id);
          const isSelected = selectedArticleId === article.id;
          const hasLowConfidence = article.norms.some(n => n.needs_human_review);

          return (
            <div key={article.id}>
              <button
                onClick={() => handleArticleClick(article)}
                className={`w-full px-4 py-3 text-left hover:bg-gray-50 transition flex items-center justify-between ${
                  isSelected ? 'bg-blue-50' : ''
                }`}
              >
                <div className="flex items-center gap-2 flex-1">
                  <svg
                    className={`w-4 h-4 text-gray-400 transition-transform ${
                      isExpanded ? 'rotate-90' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                  <span className="font-medium text-sm">
                    Стаття {article.article_number}
                  </span>
                  {article.title && (
                    <span className="text-sm text-gray-600 truncate">
                      {article.title}
                    </span>
                  )}
                </div>
                {hasLowConfidence && (
                  <span
                    className="text-yellow-600 text-lg"
                    title="Потребує перевірки"
                  >
                    ⚠️
                  </span>
                )}
              </button>

              {isExpanded && article.norms.length > 0 && (
                <div className="bg-gray-50 px-4 py-2 text-sm text-gray-600">
                  <div className="pl-6 space-y-1">
                    {article.norms.map((norm) => (
                      <div key={norm.id} className="flex items-start gap-2">
                        <span className="text-xs text-gray-400 mt-0.5">•</span>
                        <span className="flex-1">
                          {norm.norm_text.substring(0, 100)}
                          {norm.norm_text.length > 100 ? '...' : ''}
                        </span>
                        {norm.needs_human_review && (
                          <span className="text-yellow-600">⚠️</span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
