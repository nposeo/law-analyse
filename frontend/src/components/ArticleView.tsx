import { useState } from 'react';
import type { Article } from '../lib/api';

interface ArticleViewProps {
  article: Article | null;
}

export default function ArticleView({ article }: ArticleViewProps) {
  const [showPlainLanguage, setShowPlainLanguage] = useState(false);

  if (!article) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
        <p>Оберіть статтю зі списку ліворуч</p>
      </div>
    );
  }

  const norm = article.norms[0]; // For MVP, assume one norm per article

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Стаття {article.article_number}
            </h2>
            {article.title && (
              <p className="text-sm text-gray-600 mt-1">{article.title}</p>
            )}
          </div>
          {norm && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">
                Впевненість: {(norm.confidence_score * 100).toFixed(0)}%
              </span>
              {norm.needs_human_review && (
                <span
                  className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded"
                  title="Потребує перевірки людиною"
                >
                  ⚠️ Перевірити
                </span>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Plain Language Toggle */}
        {norm && (
          <div className="flex items-center gap-3 pb-4 border-b">
            <button
              onClick={() => setShowPlainLanguage(false)}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                !showPlainLanguage
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Юридична мова
            </button>
            <button
              onClick={() => setShowPlainLanguage(true)}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                showPlainLanguage
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              💬 Проста мова
            </button>
          </div>
        )}

        {/* Content */}
        {!showPlainLanguage ? (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">
              Текст статті
            </h3>
            <div className="prose prose-sm max-w-none">
              <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
                {article.full_text}
              </p>
            </div>
          </div>
        ) : norm ? (
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">
                Що регулюється
              </h3>
              <p className="text-gray-800">{norm.norm_text}</p>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">
                На кого поширюється
              </h3>
              <p className="text-gray-800">{norm.subject}</p>
            </div>

            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-900 mb-2">
                💬 Пояснення простою мовою
              </h3>
              <p className="text-blue-800">{norm.simplified_explanation}</p>
            </div>

            {norm.needs_human_review && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-sm text-yellow-800">
                  ⚠️ <strong>Увага:</strong> AI не впевнений у цій інтерпретації
                  (впевненість {(norm.confidence_score * 100).toFixed(0)}%).
                  Рекомендується перевірка юристом.
                </p>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            <p>Норми ще не екстраговані для цієї статті</p>
          </div>
        )}
      </div>
    </div>
  );
}
