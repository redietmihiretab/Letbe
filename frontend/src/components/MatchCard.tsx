import React from 'react';
import Link from 'next/link';

interface MatchCardProps {
  matchId: string | number;
  homeTeam: string;
  awayTeam: string;
  homeLogo?: string;
  awayLogo?: string;
  probabilities: {
    home: number;
    draw: number;
    away: number;
  };
  prediction: string;
  confidence: number;
  time: string;
}

const MatchCard: React.FC<MatchCardProps> = ({
  matchId,
  homeTeam,
  awayTeam,
  homeLogo,
  awayLogo,
  probabilities,
  prediction,
  confidence,
  time
}) => {
  return (
    <div className="glass glass-hover p-6 rounded-2xl w-full max-w-md">
      <div className="flex justify-between items-center mb-6">
        <span className="text-xs font-semibold text-slate-400 tracking-wider uppercase">{time}</span>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          <span className="text-xs text-emerald-500 font-bold">CONFIDENCE: {Math.round(confidence * 100)}%</span>
        </div>
      </div>

      <div className="flex justify-between items-center mb-8">
        <div className="flex flex-col items-center space-y-2 w-1/3">
          <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center p-2 border border-slate-700">
            {homeLogo ? <img src={homeLogo} alt={homeTeam} className="w-full h-full object-contain" /> : <span className="text-2xl font-bold">{homeTeam[0]}</span>}
          </div>
          <span className="text-sm font-bold text-center">{homeTeam}</span>
        </div>

        <div className="flex flex-col items-center">
          <span className="text-2xl font-black text-slate-600 italic">VS</span>
        </div>

        <div className="flex flex-col items-center space-y-2 w-1/3">
          <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center p-2 border border-slate-700">
            {awayLogo ? <img src={awayLogo} alt={awayTeam} className="w-full h-full object-contain" /> : <span className="text-2xl font-bold">{awayTeam[0]}</span>}
          </div>
          <span className="text-sm font-bold text-center">{awayTeam}</span>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex justify-between text-xs font-bold mb-1">
          <span className="text-emerald-400">HOME {Math.round(probabilities.home * 100)}%</span>
          <span className="text-sky-400">DRAW {Math.round(probabilities.draw * 100)}%</span>
          <span className="text-rose-400">AWAY {Math.round(probabilities.away * 100)}%</span>
        </div>
        
        <div className="prob-bar flex">
          <div 
            className="prob-fill bg-emerald-500" 
            style={{ width: `${probabilities.home * 100}%` }}
          ></div>
          <div 
            className="prob-fill bg-sky-500" 
            style={{ width: `${probabilities.draw * 100}%` }}
          ></div>
          <div 
            className="prob-fill bg-rose-500" 
            style={{ width: `${probabilities.away * 100}%` }}
          ></div>
        </div>

        <div className="mt-6 pt-4 border-t border-white/5 flex flex-col space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-slate-400">LETBE PICK:</span>
            <span className="text-sm font-black text-emerald-400">{prediction.toUpperCase()}</span>
          </div>
          <Link 
            href={`/analysis/${matchId}`} 
            className="w-full py-2 bg-white/5 hover:bg-white/10 rounded-xl text-center text-xs font-bold transition-colors border border-white/5"
          >
            VIEW DETAILED ANALYSIS
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MatchCard;
