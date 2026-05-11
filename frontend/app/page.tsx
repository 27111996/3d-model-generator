'use client';
import { useState } from 'react';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [image, setImage] = useState('');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const generate = async () => {
    setLoading(true);
    setError('');
    setImage('');
    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });
      const data = await res.json();
      if (data.status === 'success') {
        setImage('data:image/png;base64,' + data.image);
        setCode(data.scad_code);
      } else {
        setError('Render failed: ' + data.scad_code);
        setCode(data.scad_code);
      }
    } catch (e) {
      setError('Backend error!');
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      <h1 className="text-3xl font-bold text-center mb-8">
        🧊 LLM-Based 3D Model Generator
      </h1>
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-900 rounded-2xl p-6">
          <h2 className="text-xl font-semibold mb-4">💬 Describe your 3D object</h2>
          <textarea
            className="w-full bg-gray-800 rounded-xl p-4 text-white resize-none h-32 mb-4"
            placeholder="e.g. a chair with 4 legs..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button
            onClick={generate}
            disabled={loading || !prompt}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-xl py-3 font-semibold transition"
          >
            {loading ? '⏳ Generating...' : '🚀 Generate 3D Model'}
          </button>
          {error && (
            <div className="mt-4 bg-red-900 rounded-xl p-4 text-sm text-red-200">
              {error}
            </div>
          )}
          {code && (
            <div className="mt-4">
              <h3 className="text-sm font-semibold text-gray-400 mb-2">OpenSCAD Code:</h3>
              <pre className="bg-gray-800 rounded-xl p-4 text-sm overflow-auto max-h-48 text-green-400">
                {code}
              </pre>
            </div>
          )}
        </div>
        <div className="bg-gray-900 rounded-2xl p-6 flex flex-col items-center justify-center min-h-64">
          <h2 className="text-xl font-semibold mb-4">🧊 3D Preview</h2>
          {loading && (
            <div className="text-center">
              <p className="text-4xl mb-4 animate-pulse">⚙️</p>
              <p className="text-gray-400">Generating 3D model...</p>
            </div>
          )}
          {image && !loading && (
            <img
              src={image}
              alt="3D Model"
              className="rounded-xl w-full"
            />
          )}
          {!image && !loading && (
            <div className="text-gray-500 text-center">
              <p className="text-6xl mb-4">🧊</p>
              <p>Your 3D model will appear here</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
