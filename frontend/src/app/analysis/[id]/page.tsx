'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';

export default function AnalysisPage({ params }: { params: { id: string } }) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDetails() {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/predictions`);
        const json = await res.json();
        // For demo, just pick the first one or match by id if possible
        setData(json.data[0]); 
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchDetails();
  }, [params.id]);

  if (loading) return <div className="min-h-screen flex items-center justify-center text-slate-500 font-bold">LOADING ANALYSIS...</div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center text-slate-500 font-bold">ANALYSIS NOT FOUND.</div>;

  const match = {
    homeTeam: data.matches.home_team.name,
    awayTeam: data.matches.away_team.name,
    date: new Date(data.matches.match_date).toLocaleString(),
    probabilities: { home: data.home_win_prob, draw: data.draw_prob, away: data.away_win_prob },
    btts: data.btts_yes_prob || 0.5,
    over25: data.over_25_prob || 0.5,
    under25: data.under_25_prob || 0.5,
    corners: data.predicted_corners || 10.5,
    yellowCards: data.predicted_yellow_cards || 4.2,
    aiInsight: data.ai_explanation,
    confidence: data.confidence_score
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-6 md:p-12">
      <div className="w-full max-w-4xl">
        <Link href="/" className="text-emerald-400 hover:text-emerald-300 text-sm font-bold mb-8 inline-block">
          ← BACK TO DASHBOARD
        </Link>

        {/* Header Section */}
        <div className="glass p-8 rounded-3xl mb-8 flex flex-col md:flex-row justify-between items-center text-center md:text-left">
          <div className="flex flex-col items-center md:items-start mb-6 md:mb-0">
            <h2 className="text-3xl font-black tracking-tighter uppercase mb-1">{match.homeTeam}</h2>
            <span className="text-slate-500 font-bold uppercase tracking-widest text-xs">HOME</span>
          </div>
          
          <div className="flex flex-col items-center mx-8">
            <span className="text-4xl font-black text-slate-700 italic">VS</span>
            <span className="text-xs text-slate-500 font-bold mt-2">{match.date}</span>
          </div>

          <div className="flex flex-col items-center md:items-end">
            <h2 className="text-3xl font-black tracking-tighter uppercase mb-1">{match.awayTeam}</h2>
            <span className="text-slate-500 font-bold uppercase tracking-widest text-xs">AWAY</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Main Probabilities */}
          <div className="md:col-span-2 space-y-8">
            <div className="glass p-8 rounded-3xl">
              <h3 className="text-lg font-black tracking-tighter mb-6 uppercase border-b border-white/5 pb-4">Win Probabilities</h3>
              <div className="space-y-6">
                <ProbabilityRow label="HOME WIN" prob={match.probabilities.home} color="bg-emerald-500" />
                <ProbabilityRow label="DRAW" prob={match.probabilities.draw} color="bg-sky-500" />
                <ProbabilityRow label="AWAY WIN" prob={match.probabilities.away} color="bg-rose-500" />
              </div>
            </div>

            <div className="glass p-8 rounded-3xl">
              <h3 className="text-lg font-black tracking-tighter mb-6 uppercase border-b border-white/5 pb-4">Letbe AI Insight</h3>
              <p className="text-slate-300 leading-relaxed italic text-lg">
                "{match.aiInsight}"
              </p>
            </div>
          </div>

          {/* Secondary Markets */}
          <div className="space-y-8">
            <div className="glass p-6 rounded-3xl">
              <h3 className="text-sm font-black tracking-tighter mb-4 uppercase text-slate-400">Additional Markets</h3>
              <div className="space-y-4">
                <MarketStat label="BTTS YES" value={`${Math.round(match.btts * 100)}%`} />
                <MarketStat label="OVER 2.5" value={`${Math.round(match.over25 * 100)}%`} />
                <MarketStat label="CORNERS" value={match.corners.toString()} />
                <MarketStat label="YELLOW CARDS" value={match.yellowCards.toString()} />
              </div>
            </div>

            <div className="bg-emerald-500/10 border border-emerald-500/20 p-6 rounded-3xl">
              <h3 className="text-xs font-black tracking-tighter mb-2 uppercase text-emerald-500">Confidence Score</h3>
              <span className="text-4xl font-black text-emerald-400">{Math.round(match.confidence * 100)}%</span>
              <p className="text-xs text-emerald-500/60 mt-2 font-bold">
                {match.confidence > 0.7 ? "HIGH PROBABILITY MATCH" : "MODERATE PROBABILITY MATCH"}
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

function ProbabilityRow({ label, prob, color }: { label: string, prob: number, color: string }) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-xs font-black tracking-widest">
        <span>{label}</span>
        <span>{Math.round(prob * 100)}%</span>
      </div>
      <div className="prob-bar">
        <div className={`${color} h-full`} style={{ width: `${prob * 100}%` }}></div>
      </div>
    </div>
  );
}

function MarketStat({ label, value }: { label: string, value: string }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-white/5 last:border-0">
      <span className="text-xs font-bold text-slate-500">{label}</span>
      <span className="text-sm font-black text-white">{value}</span>
    </div>
  );
}
