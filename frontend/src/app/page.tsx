'use client';
import { useEffect, useState } from 'react';
import MatchCard from '@/components/MatchCard';

export default function Home() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredMatches = matches.filter((pred: any) => 
    pred.matches.home_team.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    pred.matches.away_team.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  useEffect(() => {
    async function fetchPredictions() {
      try {
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
        const res = await fetch(`${backendUrl}/api/v1/predictions`);
        const json = await res.json();
        setMatches(json.data || []);
      } catch (err) {
        console.error("Failed to fetch predictions:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchPredictions();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm flex mb-12">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-white/10 bg-slate-900/50 pb-6 pt-8 backdrop-blur-2xl lg:static lg:w-auto lg:rounded-xl lg:border lg:p-4">
          LETBE AI&nbsp;
          <code className="font-bold text-emerald-400">v1.0.0-beta</code>
        </p>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-slate-950 via-slate-950 lg:static lg:h-auto lg:w-auto lg:bg-none">
          <a
            className="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0 font-bold tracking-tighter"
            href="#"
          >
            POWERED BY GEMINI
          </a>
        </div>
      </div>

      <div className="flex flex-col items-center mb-16">
        <div className="glass px-4 py-2 rounded-full mb-6 border border-white/10">
          <span className="text-[10px] font-black tracking-[0.2em] text-emerald-400 uppercase">LETBE AI v1.0.0-beta</span>
        </div>
        <h1 className="text-7xl md:text-9xl font-black tracking-tighter text-center leading-[0.8] mb-12">
          BEAT THE<br />ODDS.
        </h1>
        
        {/* Search Bar */}
        <div className="w-full max-w-xl relative">
          <input 
            type="text" 
            placeholder="SEARCH TEAM OR LEAGUE..." 
            className="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-sm font-bold tracking-widest focus:outline-none focus:border-emerald-500/50 transition-colors uppercase placeholder:text-slate-600"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <div className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-500 font-black text-xs">
            {filteredMatches.length} RESULTS
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-7xl">
        {loading ? (
          <div className="col-span-full text-center py-12">
            <span className="text-slate-500 font-bold animate-pulse">ANALYZING UPCOMING FIXTURES...</span>
          </div>
        ) : filteredMatches.length > 0 ? (
          filteredMatches.map((pred: any) => (
            <MatchCard 
              key={pred.id} 
              matchId={pred.match_id}
              homeTeam={pred.matches.home_team.name}
              awayTeam={pred.matches.away_team.name}
              homeLogo={pred.matches.home_team.logo_url}
              awayLogo={pred.matches.away_team.logo_url}
              probabilities={{
                home: pred.home_win_prob,
                draw: pred.draw_prob,
                away: pred.away_win_prob
              }}
              prediction={pred.home_win_prob > pred.away_win_prob ? "Home Win" : "Away Win"}
              confidence={pred.confidence_score}
              time={new Date(pred.matches.match_date).toLocaleString()}
            />
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <span className="text-slate-500 font-bold">NO PREDICTIONS GENERATED YET.</span>
          </div>
        )}
      </div>

      <footer className="mt-24 text-slate-500 text-xs font-medium tracking-widest uppercase">
        © 2026 LETBE AI PREDICTION PLATFORM
      </footer>
    </main>
  );
}
