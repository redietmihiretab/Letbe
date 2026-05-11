# Project Plan: Letbe - AI Football Prediction Web App

**Letbe** is a premium AI-powered football prediction platform designed to provide high-accuracy insights across multiple markets using machine learning and real-time data.

---

## 1. Technical Stack (Finalized)

### Frontend: Next.js (React)
- **Styling**: Vanilla CSS with a focus on Glassmorphism and Dark Mode.
- **State Management**: React Context or Zustand for lightweight global state.
- **Visuals**: Chart.js or Recharts for probability distributions and historical trends.
- **Components**: Radix UI for accessible, premium-feeling primitives.

### Backend: FastAPI (Python)
- **ML Engine**: Scikit-learn, XGBoost, and Poisson distribution models.
- **Data Orchestration**: GitHub Actions for daily data fetching and model retraining.
- **LLM Integration**: Gemini API for generating natural language match analysis.

### Database & Auth: Supabase
- **Postgres**: For structured data storage (matches, stats, predictions).
- **Real-time**: To push live score updates or prediction changes.
- **Storage**: For caching processed features and model weights.

---

## 2. Supported Prediction Markets

- **1X2 (Match Outcome)**: Home Win / Draw / Away Win probabilities + confidence score.
- **BTTS (Both Teams To Score)**: Binary Yes/No probability.
- **Over/Under Goals**: Predictions for 0.5, 1.5, 2.5, and 3.5 lines.
- **Team Goal Ranges**: Probability of a team scoring 0, 1-2, or 3+ goals.
- **Corners & Cards**: Predicted totals and Over/Under lines (e.g., 9.5 corners, 4.5 yellows).

---

## 3. Data Strategy & Sources

### Primary Data Pipeline
1. **Historical Data (Training)**: Bulk download of CSVs from [Football-Data.co.uk](https://www.football-data.co.uk/) (last 10 seasons).
2. **Real-time Data (Production)**: [API-Football](https://www.api-football.com/) via RapidAPI (Free Tier).
3. **Metadata**: [TheSportsDB](https://www.thesportsdb.com/) for team logos, stadium info, and player details.

### Caching Strategy
- **Fixture Cache**: Fetched every 12 hours.
- **Prediction Cache**: Generated once daily or when line-ups are announced (1 hour before kickoff).
- **Rate Limiting**: Aggressive use of Supabase to store all fetched data to minimize API calls.

---

## 4. Machine Learning Architecture

### Feature Engineering
- **Rolling Averages**: Last 5/10 match performance (Goals, xG, Corners, Cards).
- **Relative Strength**: ELO-based ratings or Points-Per-Game (PPG) splits.
- **H2H (Head-to-Head)**: Historical dominance between specific teams.
- **Venue Factor**: Home/Away performance variance.

### Model Ensemble
- **Classifier (XGBoost)**: For 1X2 and BTTS (Probabilistic output).
- **Regressor (XGBoost/Poisson)**: For Goals, Corners, and Cards totals.
- **Validation**: Walk-forward cross-validation to ensure model stability over the season.

---

## 5. UI/UX Design System

- **Aesthetic**: "Futuristic Dashboard" — Dark slate background (#0f172a), neon accents (Emerald for wins, Rose for losses), and semi-transparent glass cards.
- **Responsive Layout**: Mobile-first design for users checking stats on the go.
- **Interactive Elements**:
    - Animated progress bars for win probabilities.
    - Expandable "Deep Dive" sections for LLM-generated analysis.
    - Interactive line charts for team form trends.

---

## 6. Development Roadmap

### Phase 1: Foundation (Current)
- [ ] Initialize Supabase project and schema.
- [ ] Set up Python environment for FastAPI and ML experiments.
- [ ] Create data ingestion scripts for historical CSVs.

### Phase 2: ML Development
- [ ] Feature engineering pipeline construction.
- [ ] Model training (1X2 & Over/Under 2.5).
- [ ] Implementation of Poisson distribution for goal range probabilities.

### Phase 3: Backend & API
- [ ] FastAPI endpoints for match listings and predictions.
- [ ] Integration with Gemini for "Letbe Insights" (AI commentary).
- [ ] GitHub Actions for automated daily updates.

### Phase 4: Frontend Implementation
- [ ] Next.js project setup with CSS modules.
- [ ] Match Card component with interactive probability bars.
- [ ] Dashboard view with league filtering and "Top Picks" section.

### Phase 5: Polish & Deployment
- [ ] Performance optimization and caching verification.
- [ ] Mobile responsiveness audit.
- [ ] Final deployment to Vercel (Frontend) and Render/Fly.io (Backend).

---

## 7. Success Metrics & Disclaimer

- **Target Accuracy**: >55% for 1X2 outcomes in top 5 European leagues.
- **Performance**: <200ms API response time (cached).
- **Disclaimer**: Letbe is an educational/entertainment tool. We do not provide financial or gambling advice.
