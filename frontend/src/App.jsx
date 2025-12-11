import React, { useState } from 'react';
import {
  Upload,
  FileText,
  Briefcase,
  CheckCircle,
  XCircle,
  AlertCircle,
  TrendingUp,
  Award,
  Target,
  Zap,
  Brain,
  Sparkles,
} from 'lucide-react';

function App() {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [useAI, setUseAI] = useState(true);

  const handleFileUpload = async (e, type) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type === 'text/plain') {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (type === 'resume') {
          setResume(event.target.result);
        } else {
          setJobDescription(event.target.result);
        }
      };
      reader.readAsText(file);
    } else if (file.type === 'application/pdf') {
      alert('PDF support coming soon! Please use .txt files for now.');
    } else {
      alert('Please upload a .txt or .pdf file');
    }
  };

  const analyzeWithAI = async (resumeText, jdText) => {
    const response = await fetch('http://localhost:8001/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        resume: resumeText,
        job_description: jdText,
      }),
    });

    if (!response.ok) {
      throw new Error('AI analysis failed');
    }

    return response.json();
  };

  const analyzeResume = async () => {
    if (!resume.trim() || !jobDescription.trim()) {
      alert('Please provide both resume and job description');
      return;
    }

    setLoading(true);

    try {
      if (useAI) {
        const result = await analyzeWithAI(resume, jobDescription);
        setAnalysis(result);
      } else {
        alert('Basic analysis mode not available. Please enable AI mode.');
      }
    } catch (error) {
      console.error('AI Analysis Error:', error);
      alert(
        'AI analysis failed. Make sure the backend server is running at http://localhost:8000'
      );
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'border-red-500 bg-red-50';
      case 'medium':
        return 'border-yellow-500 bg-yellow-50';
      case 'low':
        return 'border-blue-500 bg-blue-50';
      case 'info':
        return 'border-green-500 bg-green-50';
      default:
        return 'border-gray-500 bg-gray-50';
    }
  };

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <AlertCircle className="text-red-600" size={20} />;
      case 'medium':
        return <AlertCircle className="text-yellow-600" size={20} />;
      case 'low':
        return <AlertCircle className="text-blue-600" size={20} />;
      case 'info':
        return <CheckCircle className="text-green-600" size={20} />;
      default:
        return <AlertCircle className="text-gray-600" size={20} />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Brain className="text-indigo-600" size={48} />
            <h1 className="text-5xl font-bold text-gray-800">
              AI-Powered ATS Analyzer
            </h1>
          </div>
          <p className="text-gray-600 mb-4 text-lg">
            Advanced Resume Analysis using Transformer Models & NLP
          </p>
          <div className="flex items-center justify-center gap-4 text-sm flex-wrap">
            <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm">
              <Sparkles className="text-purple-500" size={16} />
              <span className="text-gray-700">
                Sentence-Transformers (all-MiniLM-L6-v2)
              </span>
            </div>
            <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm">
              <Zap className="text-yellow-500" size={16} />
              <span className="text-gray-700">
                Spacy NLP • TF-IDF • Semantic Embeddings
              </span>
            </div>
          </div>
        </div>

        {/* AI Mode Toggle */}
        <div className="bg-white rounded-xl shadow-lg p-5 mb-6 border-2 border-indigo-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-indigo-100 p-3 rounded-lg">
                <Brain className="text-indigo-600" size={28} />
              </div>
              <div>
                <p className="font-bold text-gray-800 text-lg">
                  AI Analysis Mode
                </p>
                <p className="text-sm text-gray-600">
                  Advanced semantic similarity using transformer models
                </p>
              </div>
            </div>
            <label className="flex items-center gap-3 cursor-pointer">
              <span className="text-sm font-medium text-gray-700">
                Enable AI
              </span>
              <div className="relative">
                <input
                  type="checkbox"
                  checked={useAI}
                  onChange={(e) => setUseAI(e.target.checked)}
                  className="sr-only"
                />
                <div
                  className={`block w-16 h-9 rounded-full transition-all duration-300 ${
                    useAI ? 'bg-indigo-600' : 'bg-gray-300'
                  }`}
                ></div>
                <div
                  className={`absolute left-1 top-1 bg-white w-7 h-7 rounded-full transition-transform duration-300 shadow-md ${
                    useAI ? 'translate-x-7' : ''
                  }`}
                ></div>
              </div>
            </label>
          </div>
        </div>

        {/* Input Section */}
        <div className="grid lg:grid-cols-2 gap-6 mb-6">
          {/* Resume Input */}
          <div className="bg-white rounded-xl shadow-xl p-6 border-2 border-blue-200">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="bg-blue-100 p-2 rounded-lg">
                  <FileText className="text-blue-600" size={24} />
                </div>
                <h2 className="text-xl font-bold text-gray-800">Your Resume</h2>
              </div>
              <label className="cursor-pointer text-sm text-blue-600 hover:text-blue-700 flex items-center gap-2 bg-blue-50 px-4 py-2 rounded-lg font-medium transition-colors">
                <Upload size={18} />
                Upload File
                <input
                  type="file"
                  accept=".txt"
                  onChange={(e) => handleFileUpload(e, 'resume')}
                  className="hidden"
                />
              </label>
            </div>
            <textarea
              value={resume}
              onChange={(e) => setResume(e.target.value)}
              placeholder={`Paste your resume here or upload a .txt file...

Example:
Senior Software Engineer with 8+ years in Python, React, AWS...
Machine learning expertise with TensorFlow and PyTorch...`}
              className="w-full h-80 p-4 border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm"
            />
            <p className="text-xs text-gray-500 mt-2">
              {resume.length} characters •{' '}
              {resume.split(/\s+/).filter(Boolean).length} words
            </p>
          </div>

          {/* Job Description Input */}
          <div className="bg-white rounded-xl shadow-xl p-6 border-2 border-purple-200">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="bg-purple-100 p-2 rounded-lg">
                  <Briefcase className="text-purple-600" size={24} />
                </div>
                <h2 className="text-xl font-bold text-gray-800">
                  Job Description
                </h2>
              </div>
              <label className="cursor-pointer text-sm text-purple-600 hover:text-purple-700 flex items-center gap-2 bg-purple-50 px-4 py-2 rounded-lg font-medium transition-colors">
                <Upload size={18} />
                Upload File
                <input
                  type="file"
                  accept=".txt"
                  onChange={(e) => handleFileUpload(e, 'jd')}
                  className="hidden"
                />
              </label>
            </div>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder={`Paste the job description here or upload a .txt file...

Example:
Looking for Senior ML Engineer with 5+ years experience.
Required: Python, TensorFlow, AWS, Docker, Kubernetes...`}
              className="w-full h-80 p-4 border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none text-sm"
            />
            <p className="text-xs text-gray-500 mt-2">
              {jobDescription.length} characters •{' '}
              {jobDescription.split(/\s+/).filter(Boolean).length} words
            </p>
          </div>
        </div>

        {/* Analyze Button */}
        <div className="text-center mb-8">
          <button
            onClick={analyzeResume}
            disabled={loading || !resume.trim() || !jobDescription.trim()}
            className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white px-12 py-4 rounded-xl font-bold text-lg hover:from-indigo-700 hover:via-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg flex items-center gap-3 mx-auto"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                Analyzing with AI Models...
              </>
            ) : (
              <>
                <Brain size={24} />
                Analyze with AI
                <Sparkles size={20} />
              </>
            )}
          </button>
          {(!resume.trim() || !jobDescription.trim()) && (
            <p className="text-sm text-red-500 mt-2">
              Please provide both resume and job description
            </p>
          )}
        </div>

        {/* Results Section */}
        {analysis && (
          <div className="space-y-6">
            {/* Main Score Card */}
            <div className="bg-white rounded-xl shadow-2xl p-8 border-2 border-indigo-200">
              {analysis.ai_powered !== false && (
                <div className="bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50 rounded-lg p-4 mb-6 border-2 border-indigo-200">
                  <div className="flex items-center gap-3 text-indigo-700">
                    <Brain size={24} />
                    <div>
                      <span className="font-bold text-lg">
                        AI-Powered Deep Analysis Complete
                      </span>
                      <p className="text-sm text-indigo-600 mt-1">
                        Results generated using sentence-transformer embeddings,
                        Spacy NLP, and TF-IDF analysis
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <div className="text-center mb-8">
                <div className="inline-block">
                  <div className="relative w-48 h-48 mx-auto mb-4">
                    <svg className="transform -rotate-90 w-48 h-48">
                      <circle
                        cx="96"
                        cy="96"
                        r="85"
                        stroke="#e5e7eb"
                        strokeWidth="14"
                        fill="none"
                      />
                      <circle
                        cx="96"
                        cy="96"
                        r="85"
                        stroke={
                          analysis.overall_score >= 80
                            ? '#10b981'
                            : analysis.overall_score >= 65
                            ? '#3b82f6'
                            : analysis.overall_score >= 50
                            ? '#f59e0b'
                            : '#ef4444'
                        }
                        strokeWidth="14"
                        fill="none"
                        strokeDasharray={`${2 * Math.PI * 85}`}
                        strokeDashoffset={`${
                          2 * Math.PI * 85 * (1 - analysis.overall_score / 100)
                        }`}
                        className="transition-all duration-1000"
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center flex-col">
                      <span className="text-5xl font-bold text-gray-800">
                        {analysis.overall_score}%
                      </span>
                      <span className="text-sm text-gray-500">Match Score</span>
                    </div>
                  </div>
                  <p className={`text-3xl font-bold ${analysis.verdictColor} mb-2`}>
                    {analysis.verdict}
                  </p>
                  <p className="text-gray-600">
                    Based on AI semantic analysis
                  </p>
                </div>
              </div>

              {/* Key Metrics */}
              <div className="grid md:grid-cols-3 gap-4 mb-6">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-5 border-2 border-blue-200 transform hover:scale-105 transition-transform">
                  <div className="flex items-center gap-3 mb-3">
                    <Brain className="text-blue-600" size={24} />
                    <h3 className="font-bold text-gray-800">
                      Semantic Similarity
                    </h3>
                  </div>
                  <p className="text-4xl font-bold text-blue-600 mb-1">
                    {(analysis.semantic_similarity * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs text-gray-600">
                    Transformer-based contextual match
                  </p>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-5 border-2 border-green-200 transform hover:scale-105 transition-transform">
                  <div className="flex items-center gap-3 mb-3">
                    <CheckCircle className="text-green-600" size={24} />
                    <h3 className="font-bold text-gray-800">Matched Skills</h3>
                  </div>
                  <p className="text-4xl font-bold text-green-600 mb-1">
                    {analysis.skill_matches?.matched?.length || 0}
                  </p>
                  <p className="text-xs text-gray-600">
                    Required skills found in resume
                  </p>
                </div>

                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-5 border-2 border-purple-200 transform hover:scale-105 transition-transform">
                  <div className="flex items-center gap-3 mb-3">
                    <Award className="text-purple-600" size={24} />
                    <h3 className="font-bold text-gray-800">Key Phrases</h3>
                  </div>
                  <p className="text-4xl font-bold text-purple-600 mb-1">
                    {analysis.key_phrases?.matched?.length || 0}/
                    {analysis.key_phrases?.total || 0}
                  </p>
                  <p className="text-xs text-gray-600">
                    Important phrases aligned
                  </p>
                </div>
              </div>

              {/* Category Analysis */}
              {analysis.category_analysis &&
                Object.keys(analysis.category_analysis).length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-bold text-gray-800 mb-4 text-xl flex items-center gap-2">
                      <TrendingUp className="text-indigo-600" size={24} />
                      Skills Analysis by Category
                    </h3>
                    <div className="space-y-3">
                      {Object.entries(analysis.category_analysis).map(
                        ([category, data]) => (
                          <div
                            key={category}
                            className="bg-gray-50 rounded-lg p-4 border border-gray-200"
                          >
                            <div className="flex justify-between items-center mb-3">
                              <span className="font-semibold text-gray-700 capitalize text-lg">
                                {category.replace(/_/g, ' ')}
                              </span>
                              <span
                                className={`font-bold text-xl ${
                                  data.percentage >= 80
                                    ? 'text-green-600'
                                    : data.percentage >= 50
                                    ? 'text-yellow-600'
                                    : 'text-red-600'
                                }`}
                              >
                                {data.percentage}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
                              <div
                                className={`h-3 rounded-full transition-all duration-500 ${
                                  data.percentage >= 80
                                    ? 'bg-green-500'
                                    : data.percentage >= 50
                                    ? 'bg-yellow-500'
                                    : 'bg-red-500'
                                }`}
                                style={{ width: `${data.percentage}%` }}
                              ></div>
                            </div>
                            {data.matched && data.matched.length > 0 && (
                              <div className="flex flex-wrap gap-2 mt-2">
                                {data.matched.map((skill, idx) => (
                                  <span
                                    key={idx}
                                    className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium"
                                  >
                                    ✓ {skill}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}

              {/* Skills Match/Missing */}
              {analysis.skill_matches && (
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="bg-green-50 rounded-xl p-5 border-2 border-green-200">
                    <div className="flex items-center gap-3 mb-4">
                      <CheckCircle className="text-green-600" size={24} />
                      <h3 className="font-bold text-gray-800 text-lg">
                        Matched Skills
                      </h3>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {analysis.skill_matches.matched
                        ?.slice(0, 20)
                        .map((skill, idx) => (
                          <span
                            key={idx}
                            className="bg-green-100 text-green-700 px-3 py-1.5 rounded-full text-sm font-medium shadow-sm"
                          >
                            {skill}
                          </span>
                        ))}
                      {analysis.skill_matches.matched?.length === 0 && (
                        <p className="text-sm text-gray-500 italic">
                          No matched skills detected
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="bg-red-50 rounded-xl p-5 border-2 border-red-200">
                    <div className="flex items-center gap-3 mb-4">
                      <XCircle className="text-red-600" size={24} />
                      <h3 className="font-bold text-gray-800 text-lg">
                        Missing Skills
                      </h3>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {analysis.skill_matches.missing
                        ?.slice(0, 20)
                        .map((skill, idx) => (
                          <span
                            key={idx}
                            className="bg-red-100 text-red-700 px-3 py-1.5 rounded-full text-sm font-medium shadow-sm"
                          >
                            {skill}
                          </span>
                        ))}
                      {analysis.skill_matches.missing?.length === 0 && (
                        <p className="text-sm text-green-600 font-medium">
                          ✓ All required skills present!
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Recommendations */}
            {analysis.recommendations &&
              analysis.recommendations.length > 0 && (
                <div className="bg-white rounded-xl shadow-2xl p-8 border-2 border-purple-200">
                  <h3 className="text-2xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                    <Target className="text-indigo-600" size={32} />
                    AI-Generated Recommendations
                  </h3>
                  <p className="text-gray-600 mb-6">
                    Based on deep transformer analysis and NLP processing of
                    your resume vs. job requirements
                  </p>

                  <div className="space-y-4">
                    {analysis.recommendations.map((rec, idx) => (
                      <div
                        key={idx}
                        className={`border-l-4 rounded-xl p-5 ${getPriorityColor(
                          rec.priority
                        )} shadow-md hover:shadow-lg transition-shadow`}
                      >
                        <div className="flex items-start gap-4">
                          <div className="mt-1">{getPriorityIcon(rec.priority)}</div>
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2 flex-wrap">
                              <span className="text-xs font-bold uppercase tracking-wider text-gray-600 bg-white px-3 py-1 rounded-full">
                                {rec.category}
                              </span>
                              <span className="text-xs text-gray-500">•</span>
                              <span className="text-xs text-gray-600 font-medium">
                                {rec.impact}
                              </span>
                            </div>
                            <h4 className="font-bold text-gray-800 mb-2 text-lg">
                              {rec.title}
                            </h4>
                            <p className="text-sm text-gray-700 leading-relaxed">
                              {rec.description}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
