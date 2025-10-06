import { useState } from "react";
import { Home, Search, Compass, Cpu, Info } from "lucide-react";

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [summary, setSummary] = useState("");
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [nerResult, setNerResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Use VITE_API_URL if provided, otherwise default to backend FastAPI port 8000
  const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setError(null);

    try {
      // Call search endpoint
      const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(data.results || []);

      // Call describe endpoint for AI summary
      const describeRes = await fetch(
        `${API_BASE}/describe?q=${encodeURIComponent(query)}`
      );
      const describeData = await describeRes.json();
      setSummary(describeData.summary || "");
    } catch (err) {
      console.error("Error fetching:", err);
      setError(String(err));
    }

    setLoading(false);
  };

  const handleRecommend = async () => {
    if (!query) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/recommend?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setRecommendations(data.results || []);
    } catch (err) {
      console.error('Recommend error', err);
      setError(String(err));
    }
    setLoading(false);
  };

  const handleNer = async () => {
    if (!query) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/scibert/ner`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: query })
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`NER error: ${res.status} ${text}`);
      }
      const data = await res.json();
      setNerResult(data);
    } catch (err) {
      console.error('NER error', err);
      setError(String(err));
      setNerResult(null);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black text-white flex">
      {/* Sidebar */}
      <aside className="w-64 bg-gradient-to-b from-gray-900 to-black border-r border-gray-800 p-6 flex flex-col">
        <div className="mb-8">
          <h1 className="text-xl font-bold">Mandel's Descendants</h1>
        </div>

        <nav className="space-y-2">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-cyan-500 text-white font-medium">
            <Home size={20} />
            <span>Home</span>
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition-colors">
            <Search size={20} />
            <span>Research</span>
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition-colors">
            <Compass size={20} />
            <span>Discoveries</span>
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition-colors">
            <Cpu size={20} />
            <span>AI Query</span>
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:bg-gray-800 transition-colors">
            <Info size={20} />
            <span>About</span>
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 relative overflow-hidden">
        {/* Background Image */}
        <div
          className="absolute inset-0 bg-cover bg-center opacity-40"
          style={{ backgroundImage: `url(${import.meta.env.BASE_URL}earth.png)` }}
        />

        {/* Content Overlay */}
        <div className="relative z-10 px-16 py-12">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-6xl font-bold mb-4">
              Unlocking the Secrets of Space Biology
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Search. Learn. Discover the unknown.
            </p>

            {/* Search Bar */}
            <div className="max-w-3xl mx-auto flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSearch(); // Trigger search on Enter
                }}
                placeholder="Search for space biology research"
                className="flex-1 px-6 py-4 rounded-full bg-gray-900/80 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500 transition-colors backdrop-blur-sm"
              />
              <button
                onClick={handleSearch}
                className="px-8 py-4 rounded-full bg-cyan-500 text-white font-semibold hover:bg-cyan-600 transition-colors"
              >
                {loading ? "Loading..." : "Search"}
              </button>
              <button
                onClick={handleRecommend}
                className="px-6 py-4 rounded-full bg-indigo-500 text-white font-semibold hover:bg-indigo-600 transition-colors"
              >
                Recommend
              </button>
              <button
                onClick={handleNer}
                className="px-6 py-4 rounded-full bg-rose-500 text-white font-semibold hover:bg-rose-600 transition-colors"
              >
                NER
              </button>
            </div>
          </div>

          {/* AI Results Section */}
          <div className="mt-16">
            <h2 className="text-3xl font-bold mb-8">AI Results</h2>

            {/* AI Summary */}
            {summary && (
              <div className="bg-gray-900/60 backdrop-blur-md rounded-2xl p-6 border border-gray-800 mb-8">
                <h3 className="text-xl font-bold mb-2">AI Summary</h3>
                <p className="text-gray-300">{summary}</p>
              </div>
            )}

            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div className="mt-6 bg-gray-900/60 backdrop-blur-md rounded-2xl p-6 border border-gray-800 mb-8">
                <h3 className="text-xl font-bold mb-2">Recommendations</h3>
                {recommendations.map((r, i) => (
                  <div key={i} className="text-gray-300">
                    <h4 className="font-semibold">{r.title}</h4>
                    <p className="text-gray-400">{r.description}</p>
                  </div>
                ))}
              </div>
            )}

            {/* NER Result */}
            {nerResult && (
              <div className="mt-6 bg-gray-900/60 backdrop-blur-md rounded-2xl p-6 border border-gray-800 mb-8">
                <h3 className="text-xl font-bold mb-2">NER Result</h3>
                <pre className="text-sm text-gray-300">{JSON.stringify(nerResult, null, 2)}</pre>
              </div>
            )}

            {error && (
              <div className="mt-6 text-rose-400">Error: {error}</div>
            )}

            {/* Search Results */}
            <div className="space-y-6 max-w-7xl">
              {results.map((r, i) => (
                <div
                  key={i}
                  className="bg-gray-900/60 backdrop-blur-md rounded-2xl p-6 border border-gray-800 hover:border-gray-700 transition-colors"
                >
                  <h3 className="text-xl font-bold mb-2">{r.title}</h3>
                  <p className="text-gray-400">{r.description}</p>
                </div>
              ))}

              {/* If nothing searched yet, show your placeholder cards */}
              {results.length === 0 && !summary && !loading && (
                <>
                  <div className="bg-gray-900/60 backdrop-blur-md rounded-2xl p-6 border border-gray-800">
                    <h3 className="text-xl font-bold mb-2">
                      AI-Powered Space Biology Search Engine
                    </h3>
                    <p className="text-gray-400">
                      Explore the vast universe of space biology with our AI-driven search engine.
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-teal-600/40 to-teal-800/40 backdrop-blur-md rounded-2xl p-6 border border-teal-700/50">
                    <h3 className="text-xl font-bold mb-2">
                      Uncover the Mysteries of Space Biology
                    </h3>
                    <p className="text-gray-200">
                      Delve into the fascinating world of space biology and uncover the secrets of life beyond Earth.
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Footer */}
          <footer className="mt-16 py-6 text-center text-gray-400 border-t border-gray-800">
            <p>© 2025 Mandel's Descendants. All rights reserved.</p>
          </footer>
        </div>
      </main>
    </div>
  );
}




