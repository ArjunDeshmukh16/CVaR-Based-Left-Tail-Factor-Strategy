# Is Tail Risk a New Factor?

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://cvar-tail-risk-factor.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![USC Quant Research](https://img.shields.io/badge/USC-Quant_Research-CC0000?style=for-the-badge)](https://usc.edu)
[![Period](https://img.shields.io/badge/Period-Aug_–_Nov_2025-138808?style=for-the-badge)](https://github.com/ArjunDeshmukh16)

### CVaR-Based Left-Tail Factor Strategy with Robustness and Bias Control

Testing whether a CVaR-based tail-risk factor offers returns beyond the low-volatility premium.

> **Key Results:** 15-year CRSP backtest · Long-only: 9.57% ann. return, 0.70 Sharpe · Beta-neutralized long-short with Fama-MacBeth cross-sectional validation

---

## Overview

Traditional volatility treats upside and downside equally, but investors care far more about large losses than equally sized gains. This project investigates whether **Conditional Value-at-Risk (CVaR)**, a measure that captures the average loss in the worst 5% of outcomes, contains information beyond standard volatility for predicting equity returns.

We build a systematic long-short equity strategy that ranks stocks by left-tail risk severity (TailScore), go long stocks with the mildest tails and short stocks with the most severe crash exposure, and test whether this captures a distinct risk premium.

## Strategy in One Line

Buy stocks with mild left-tail losses (safer CVaR) and short stocks with severe left-tail crashes (heavy CVaR).

## Methodology

**Data:** CRSP daily returns (2015-2024), monthly returns, Fama-French 5 factors + Momentum

**Signal Construction:**
- Rolling 252-day CVaR at the 5% level for each stock
- TailScore = -CVaR (higher TailScore = more severe downside tail)
- Parallel Low-Volatility benchmark using rolling standard deviation

**Portfolio Construction:**
- 20/20 quintile long-short (value-weighted)
- Beta-neutralized using 12-month rolling beta with 1-month lag
- Monthly rebalancing

**Testing Framework:**
- Performance metrics (Sharpe, annualized return, max drawdown)
- Fama-French 5-factor + Momentum time-series regressions
- Fama-MacBeth cross-sectional regressions
- Robustness: lookback windows (63, 126, 252 days), tail thresholds (1%, 5%, 10%), portfolio cutoffs (10/10, 20/20, 30/30)
- Transaction cost and short-borrow fee adjustments
- Regime analysis across bull and crisis periods

## Key Results

| Metric | CVaR Long-Short | CVaR Long-Only | Volatility Long-Short |
|--------|----------------|----------------|----------------------|
| Ann. Return | 6.49% | 9.57% | 5.71% |
| Ann. StdDev | 29.89% | 13.65% | 30.62% |
| Sharpe Ratio | 0.22 | 0.70 | 0.19 |
| Cum. Return | 16.65% | 116.74% | 5.86% |

**Key Findings:**
- CVaR (TailScore) and LowVol load on the same underlying defensive risk dimension
- Long-only CVaR portfolios perform consistently well; short leg is unstable
- TailScore is not a separately priced characteristic in Fama-MacBeth tests
- Beta-hedged strategy significantly improves performance over unhedged
- Results are robust across lookback windows, tail thresholds, and after transaction costs
- Practical implication: more complex downside-tail measures do not outperform simpler volatility-based strategies

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cvar-tail-risk-factor.streamlit.app/)

Interactive walkthrough of the entire project: motivation, methodology, backtesting results, regression analysis, robustness tests, and key findings.

## Repository Structure

```
├── README.md
├── streamlit_app.py                 # Interactive Streamlit dashboard
├── requirements.txt                 # Streamlit dependencies
├── final_project.ipynb              # Full implementation notebook (primary)
├── Final_Project_Code.ipynb         # Additional code notebook
├── Final_Project_Paper.pdf          # 15-page research paper
├── Final_Project_Slides.pdf         # Presentation slides (11 slides)
├── Final_Project_Details.pdf        # Project brief and requirements
├── data/
│   ├── fama_french_5_factor.csv     # FF5 factor data (public)
│   └── fama_french_mom_factor.csv   # Momentum factor data (public)
├── images/                          # Strategy performance charts
│   ├── cvar_vs_volatility_long_only.png
│   ├── cvar_vs_volatility_long_short.png
│   ├── cvar_vs_volatility_short_only.png
│   ├── hedged_vs_unhedged_cvar.png
│   ├── hedged_vs_unhedged_volatility.png
│   ├── cvar_sensitivity_lookback_window.png
│   ├── cvar_sensitivity_tail_threshold.png
│   ├── cvar_sensitivity_portfolio_cutoff.png
│   ├── cvar_vs_volatility_turnover_rate.png
│   └── cvar_vs_volatility_transaction_cost.png
└── results/                         # Pre-computed performance summaries
    ├── performance_summary_2016_2024.txt
    ├── performance_summary_2016_2019.txt
    ├── performance_summary_2020_2022.txt
    ├── performance_summary_2023_2024.txt
    ├── ff_regression_summary_2016_2024.txt
    └── fmb_regression_summary_2016_2024.txt
```

## Selected Figures

### Strategy Performance

| Long-Only (CVaR vs Volatility) | Long-Short (CVaR vs Volatility) |
|---|---|
| ![Long-Only](images/cvar_vs_volatility_long_only.png) | ![Long-Short](images/cvar_vs_volatility_long_short.png) |

### Beta Hedging Impact

| CVaR: Hedged vs Unhedged | Volatility: Hedged vs Unhedged |
|---|---|
| ![CVaR Hedging](images/hedged_vs_unhedged_cvar.png) | ![Vol Hedging](images/hedged_vs_unhedged_volatility.png) |

### Robustness Tests

| Lookback Window Sensitivity | Tail Threshold Sensitivity | Portfolio Cutoff Sensitivity |
|---|---|---|
| ![Lookback](images/cvar_sensitivity_lookback_window.png) | ![Threshold](images/cvar_sensitivity_tail_threshold.png) | ![Cutoff](images/cvar_sensitivity_portfolio_cutoff.png) |

### Turnover and Transaction Costs

| Monthly Turnover | Transaction Cost Impact |
|---|---|
| ![Turnover](images/cvar_vs_volatility_turnover_rate.png) | ![Costs](images/cvar_vs_volatility_transaction_cost.png) |

## How to Run

**Interactive Dashboard (no data required):**
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Full Notebook Replication (requires CRSP access):**
1. Clone the repository
2. Obtain CRSP daily/monthly data via [WRDS](https://wrds-www.wharton.upenn.edu/) and place `.feather` files in `data/`
3. Open `final_project.ipynb` in Jupyter Notebook
4. Run cells sequentially; markdown cells describe each step

> **Note:** CRSP data is proprietary and cannot be redistributed. The Streamlit dashboard and pre-computed results allow full exploration without CRSP access.

## Tools and Libraries

`Python` `NumPy` `Pandas` `Statsmodels` `Matplotlib` `CRSP/WRDS`

---


**→ [View Portfolio](https://arjundeshmukh16.github.io) · [LinkedIn](https://linkedin.com/in/arjun-deshmukh1609) · [GitHub](https://github.com/ArjunDeshmukh16)**
