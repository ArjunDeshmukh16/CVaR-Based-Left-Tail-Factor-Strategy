import streamlit as st
import pandas as pd

st.set_page_config(page_title="Is Tail Risk a New Factor?", page_icon="📉", layout="wide")

# ── Sidebar Navigation ──
st.sidebar.title("📉 Navigation")
page = st.sidebar.radio("Go to", [
    "Overview",
    "Motivation",
    "Methodology",
    "Backtesting Results",
    "Regression Analysis",
    "Robustness Tests",
    "Key Findings"
])

# ── Helper: Performance table ──
def perf_table(data, title=""):
    if title:
        st.markdown(f"**{title}**")
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════
# PAGE: OVERVIEW
# ════════════════════════════════════════
if page == "Overview":
    st.title("Is Tail Risk a New Factor?")
    st.markdown("### Testing whether a CVaR-based tail-risk factor offers returns beyond the low-volatility premium")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **The Big Question:** Does sorting stocks by their worst possible losses (left-tail risk) 
        produce a return premium that is distinct from the well-known low-volatility anomaly?

        We build a systematic long-short equity strategy using **Conditional Value-at-Risk (CVaR)** 
        at the 5% level, a measure that captures the average loss during the worst market outcomes. 
        Unlike standard volatility, CVaR focuses exclusively on downside crashes.

        **Our Strategy in One Line:**  
        Buy stocks with mild left-tail losses (safer CVaR) and short stocks with severe left-tail crashes (heavy CVaR).
        """)
    with col2:
        st.metric("Sample Period", "2016 - 2024")
        st.metric("Universe", "U.S. Equities (CRSP)")
        st.metric("Rebalancing", "Monthly")
        st.metric("Benchmark", "Low-Volatility Factor")

    st.markdown("---")
    st.markdown("### Full Sample Performance Snapshot (2016 - 2024)")

    perf_data = {
        "Metric": ["Ann. Return", "Ann. StdDev", "Sharpe Ratio", "Cum. Return", "Max Drawdown"],
        "CVaR Long-Short": ["6.49%", "29.89%", "0.22", "16.65%", "-77.19%"],
        "CVaR Long-Only": ["9.57%", "13.65%", "0.70", "116.74%", "-25.30%"],
        "Vol Long-Short": ["5.71%", "30.62%", "0.19", "5.86%", "-79.72%"],
        "Vol Long-Only": ["8.92%", "13.78%", "0.65", "104.14%", "-25.72%"],
    }
    perf_table(perf_data)

    st.info("💡 **Takeaway:** CVaR slightly outperforms volatility in both long-short and long-only, but the real story is in the details. Navigate through the sections to explore.")

# ════════════════════════════════════════
# PAGE: MOTIVATION
# ════════════════════════════════════════
elif page == "Motivation":
    st.title("Why Tail Risk?")
    st.markdown("---")

    st.markdown("""
    ### The Problem with Volatility
    Traditional risk measures like standard deviation treat upside and downside movements equally. 
    But investors don't experience them equally. A 30% gain feels good; a 30% loss is devastating 
    and takes a 43% gain just to recover.

    ### What CVaR Captures
    **Conditional Value-at-Risk (CVaR)** at the 5% level answers the question:  
    *"On the worst 5% of days, what is the average loss?"*

    This is fundamentally different from volatility, which averages all deviations equally.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Why This Might Be Priced
        - Markets are driven by **left-tail crashes**
        - Investors consistently **misprice crash risk**
        - They overpay for lottery-like upside
        - They underprice true downside stability
        - This creates a potential **tail-risk premium**
        """)
    with col2:
        st.markdown("""
        ### What We Test
        - Does CVaR capture a **distinct tail-risk premium**?
        - Does TailScore **outperform** Low-Volatility?
        - Does TailScore deliver **alpha** after FF5 + Momentum?
        - Is TailScore **priced** in the cross-section?
        """)

# ════════════════════════════════════════
# PAGE: METHODOLOGY
# ════════════════════════════════════════
elif page == "Methodology":
    st.title("Methodology")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Data", "Signal Construction", "Portfolio Design", "Testing Framework"])

    with tab1:
        st.markdown("""
        **Equity Returns:** CRSP daily stock file (Jan 2015 - Dec 2024)
        - Common stocks only (share codes 10, 11)
        - NYSE, AMEX, NASDAQ exchanges
        - Minimum 252 consecutive daily observations required

        **Factor Data:** Fama-French 5 Factors + Momentum (Ken French's Data Library)
        - Market Excess Return (MKT-RF)
        - Size (SMB), Value (HML), Profitability (RMW)
        - Momentum (UMD)
        """)

    with tab2:
        st.markdown("""
        **CVaR Signal:**
        1. For each stock, compute rolling 252-day CVaR at the 5% level
        2. CVaR = average of the worst 5% of daily returns in the lookback window
        3. TailScore = -CVaR (higher TailScore = more severe downside tail)

        **Volatility Benchmark:**
        - Same architecture, but using rolling 252-day standard deviation instead of CVaR
        """)
        st.latex(r"CVaR_{5\%} = \frac{1}{|S|} \sum_{r_t \in S} r_t \quad \text{where } S = \text{worst 5\% of daily returns}")
        st.latex(r"TailScore = -CVaR_{5\%}")

    with tab3:
        st.markdown("""
        **Portfolio Construction:**
        - **Quintile sort:** Top 20% (mildest tails) = Long leg; Bottom 20% (worst tails) = Short leg
        - **Value-weighted** within each leg
        - **Beta-neutralized** using 12-month rolling beta with 1-month lag
        - **Monthly rebalancing** at each month-end

        **Strategies Tested:**
        - Long-Short (core factor)
        - Long-Only
        - Short-Only
        """)

    with tab4:
        st.markdown("""
        - **Performance Metrics:** Sharpe ratio, annualized return/vol, max drawdown, t-statistics
        - **Fama-French Regression:** Time-series regression against FF5 + Momentum
        - **Fama-MacBeth Regression:** Cross-sectional pricing test
        - **Robustness:** Lookback windows, tail thresholds, portfolio cutoffs
        - **Cost Analysis:** Transaction costs (10-100 bps), short-borrow fees (25-200 bps)
        - **Regime Analysis:** Pre-COVID (2016-2019), Crisis (2020-2022), Recovery (2023-2024)
        """)

# ════════════════════════════════════════
# PAGE: BACKTESTING RESULTS
# ════════════════════════════════════════
elif page == "Backtesting Results":
    st.title("Backtesting Results")
    st.markdown("---")

    # Strategy selector
    strategy = st.selectbox("Select Strategy View", ["Long-Only", "Long-Short", "Short-Only", "Beta Hedging"])

    if strategy == "Long-Only":
        st.image("images/cvar_vs_volatility_long_only.png", caption="Cumulative Return: Long-Only Strategy (CVaR vs Volatility)", use_container_width=True)
        st.markdown("""
        **Long-only CVaR consistently outperforms volatility.** The strategy earned 116.74% cumulative return 
        with a Sharpe of 0.70, compared to 104.14% and 0.65 for the volatility benchmark. 
        This is the strongest result in the study.
        """)

    elif strategy == "Long-Short":
        st.image("images/cvar_vs_volatility_long_short.png", caption="Cumulative Return: Long-Short Strategy (CVaR vs Volatility)", use_container_width=True)
        st.markdown("""
        **Both strategies struggle after 2020.** The long-short factor earned positive returns pre-COVID 
        but suffered massive drawdowns during the crisis. CVaR slightly outperforms volatility 
        (16.65% vs 5.86% cumulative), but both have low Sharpe ratios.
        """)

    elif strategy == "Short-Only":
        st.image("images/cvar_vs_volatility_short_only.png", caption="Cumulative Return: Short-Only Strategy (CVaR vs Volatility)", use_container_width=True)
        st.markdown("""
        **The short leg is consistently destructive.** Both CVaR and volatility short-only portfolios 
        lose roughly 60% over the full sample. This confirms that CVaR and volatility factors 
        work much better on the long side.
        """)

    elif strategy == "Beta Hedging":
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/hedged_vs_unhedged_cvar.png", caption="CVaR: Hedged vs Unhedged", use_container_width=True)
        with col2:
            st.image("images/hedged_vs_unhedged_volatility.png", caption="Volatility: Hedged vs Unhedged", use_container_width=True)
        st.markdown("""
        **Beta hedging transforms the strategy.** The hedged long-short portfolio dramatically 
        outperforms both the unhedged version and the market itself. This confirms that isolating 
        the tail-risk signal from market beta exposure is critical.
        """)

    st.markdown("---")
    st.markdown("### Regime Performance Comparison")

    regime = st.radio("Select Regime", ["Full Sample (2016-2024)", "Pre-COVID (2016-2019)", "Crisis (2020-2022)", "Recovery (2023-2024)"], horizontal=True)

    regime_data = {
        "Full Sample (2016-2024)": {
            "Metric": ["Ann. Return", "Ann. StdDev", "Sharpe", "Cum. Return", "Max DD"],
            "CVaR L/S": ["6.49%", "29.89%", "0.22", "16.65%", "-77.19%"],
            "CVaR L-Only": ["9.57%", "13.65%", "0.70", "116.74%", "-25.30%"],
            "Vol L/S": ["5.71%", "30.62%", "0.19", "5.86%", "-79.72%"],
            "Vol L-Only": ["8.92%", "13.78%", "0.65", "104.14%", "-25.72%"],
        },
        "Pre-COVID (2016-2019)": {
            "Metric": ["Ann. Return", "Ann. StdDev", "Sharpe", "Cum. Return", "Max DD"],
            "CVaR L/S": ["9.50%", "20.57%", "0.46", "34.21%", "-22.85%"],
            "CVaR L-Only": ["12.03%", "10.71%", "1.12", "57.84%", "-14.35%"],
            "Vol L/S": ["10.19%", "20.17%", "0.51", "38.48%", "-20.89%"],
            "Vol L-Only": ["11.96%", "11.02%", "1.09", "57.19%", "-14.54%"],
        },
        "Crisis (2020-2022)": {
            "Metric": ["Ann. Return", "Ann. StdDev", "Sharpe", "Cum. Return", "Max DD"],
            "CVaR L/S": ["-3.03%", "38.70%", "-0.08", "-28.10%", "-74.30%"],
            "CVaR L-Only": ["7.46%", "17.49%", "0.43", "19.38%", "-24.37%"],
            "Vol L/S": ["-6.35%", "40.86%", "-0.16", "-37.21%", "-76.75%"],
            "Vol L-Only": ["6.61%", "17.67%", "0.37", "16.26%", "-24.56%"],
        },
        "Recovery (2023-2024)": {
            "Metric": ["Ann. Return", "Ann. StdDev", "Sharpe", "Cum. Return", "Max DD"],
            "CVaR L/S": ["14.74%", "31.53%", "0.47", "20.89%", "-12.22%"],
            "CVaR L-Only": ["7.81%", "12.86%", "0.61", "15.03%", "-10.48%"],
            "Vol L/S": ["14.84%", "30.98%", "0.48", "21.76%", "-12.88%"],
            "Vol L-Only": ["6.30%", "12.55%", "0.50", "11.70%", "-11.38%"],
        },
    }
    perf_table(regime_data[regime])

# ════════════════════════════════════════
# PAGE: REGRESSION ANALYSIS
# ════════════════════════════════════════
elif page == "Regression Analysis":
    st.title("Regression Analysis")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Fama-French Time-Series", "Fama-MacBeth Cross-Sectional"])

    with tab1:
        st.markdown("### Fama-French 5-Factor + Momentum Regression (2016-2024)")
        st.markdown("*Does the CVaR factor earn alpha after controlling for known risk factors?*")

        st.markdown("#### CVaR Long-Short Factor")
        ff_cvar = {
            "Factor": ["const (alpha)", "Mkt-RF", "SMB", "HML", "RMW", "MOM"],
            "Coefficient": [0.0034, -0.5497, -0.9053, 0.6227, 1.3438, 0.4967],
            "t-stat": [0.605, -4.221, -3.719, 4.048, 4.680, 3.002],
            "Significant?": ["❌ No", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes"],
        }
        st.dataframe(pd.DataFrame(ff_cvar), use_container_width=True, hide_index=True)

        st.warning("""
        **Alpha is NOT significant** (t = 0.605). The CVaR factor's returns are explained by strong loadings on:
        - **HML** (value) and **RMW** (profitability) — positive
        - **Mkt-RF** (market) and **SMB** (size) — negative  
        
        This means the CVaR strategy behaves like a high-value, high-profitability, large-cap, low-beta portfolio with momentum tilt.
        """)

        st.markdown("#### Volatility Long-Short Factor")
        ff_vol = {
            "Factor": ["const (alpha)", "Mkt-RF", "SMB", "HML", "RMW", "MOM"],
            "Coefficient": [0.0019, -0.5398, -0.9594, 0.5827, 1.4851, 0.3755],
            "t-stat": [0.328, -3.923, -3.730, 3.585, 4.895, 2.147],
            "Significant?": ["❌ No", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes"],
        }
        st.dataframe(pd.DataFrame(ff_vol), use_container_width=True, hide_index=True)
        st.info("Both factors show nearly identical factor loadings, confirming they capture the **same underlying defensive risk dimension**.")

    with tab2:
        st.markdown("### Fama-MacBeth Cross-Sectional Regression (2016-2024)")
        st.markdown("*Is TailScore a priced characteristic? Do stocks with safer tails earn higher returns?*")

        fmb = {
            "Variable": ["LOG_MCAP", "BM", "OP", "MOM", "TAIL_SCORE", "VOL", "CONST"],
            "Estimate": [-0.001161, 0.001464, 0.000063, 0.001216, 0.004273, -0.002268, 0.011146],
            "t-stat": [-0.965, 1.284, 0.271, 1.023, 1.172, -0.989, 1.951],
            "Significant?": ["❌", "❌", "❌", "❌", "❌", "❌", "⚠️ Marginal"],
        }
        st.dataframe(pd.DataFrame(fmb), use_container_width=True, hide_index=True)

        st.error("""
        **TailScore is NOT a separately priced characteristic** (t = 1.17, below the 2.0 threshold). 
        While the coefficient is positive (suggesting safer tails earn slightly higher returns), 
        it is not statistically distinguishable from zero. 
        Adding volatility as a control further weakens the CVaR signal.
        """)

# ════════════════════════════════════════
# PAGE: ROBUSTNESS TESTS
# ════════════════════════════════════════
elif page == "Robustness Tests":
    st.title("Robustness Tests")
    st.markdown("---")

    test = st.selectbox("Select Test", [
        "Lookback Window Sensitivity",
        "Tail Threshold Sensitivity",
        "Portfolio Cutoff Sensitivity",
        "Turnover Analysis",
        "Transaction Cost Impact"
    ])

    if test == "Lookback Window Sensitivity":
        st.image("images/cvar_sensitivity_lookback_window.png", use_container_width=True)
        rob_data = {
            "Window": ["63 days", "126 days", "252 days (baseline)"],
            "Ann. Return": ["10.5%", "7.6%", "6.5%"],
            "Ann. Volatility": ["28.5%", "30.5%", "29.9%"],
            "Sharpe": ["0.37", "0.25", "0.22"],
        }
        perf_table(rob_data)
        st.markdown("Shorter windows are more reactive and deliver higher Sharpe ratios. All windows produce positive Sharpe ratios, confirming the signal is not driven by a single parameter choice.")

    elif test == "Tail Threshold Sensitivity":
        st.image("images/cvar_sensitivity_tail_threshold.png", use_container_width=True)
        rob_data = {
            "Threshold (α)": ["1% (extreme tail)", "5% (baseline)", "10% (broader tail)"],
            "Ann. Return": ["7.8%", "6.5%", "5.9%"],
            "Ann. Volatility": ["26.0%", "29.9%", "31.3%"],
            "Sharpe": ["0.30", "0.22", "0.19"],
        }
        perf_table(rob_data)
        st.markdown("More extreme tail thresholds produce higher Sharpe ratios. Performance does not collapse as the threshold changes, confirming robustness.")

    elif test == "Portfolio Cutoff Sensitivity":
        st.image("images/cvar_sensitivity_portfolio_cutoff.png", use_container_width=True)
        rob_data = {
            "Cutoff": ["10/10 (concentrated)", "20/20 (baseline)", "30/30 (diversified)"],
            "Ann. Return": ["9.7%", "6.5%", "4.8%"],
            "Ann. Volatility": ["35.1%", "29.9%", "25.8%"],
            "Sharpe": ["0.28", "0.22", "0.19"],
        }
        perf_table(rob_data)
        st.markdown("More concentrated portfolios deliver higher returns but with more volatility. Clear concentration vs diversification tradeoff.")

    elif test == "Turnover Analysis":
        st.image("images/cvar_vs_volatility_turnover_rate.png", use_container_width=True)
        turn_data = {
            "Strategy": ["TailScore L/S", "Volatility L/S"],
            "Avg Monthly Turnover": ["7.73%", "6.20%"],
            "Long Leg Turnover": ["8.04%", "6.00%"],
            "Short Leg Turnover": ["7.42%", "6.39%"],
        }
        perf_table(turn_data)
        st.markdown("TailScore has slightly higher turnover (~8% vs ~6% monthly), implying ~75-100% annualized turnover. Active but not extreme for a long-short equity strategy.")

    elif test == "Transaction Cost Impact":
        st.image("images/cvar_vs_volatility_transaction_cost.png", use_container_width=True)
        cost_data = {
            "Cost (bps)": ["10", "25", "50", "100"],
            "CVaR Return": ["7.6%", "7.4%", "7.2%", "6.7%"],
            "CVaR Sharpe": ["0.25", "0.25", "0.24", "0.23"],
            "Vol Return": ["6.8%", "6.6%", "6.5%", "6.1%"],
            "Vol Sharpe": ["0.22", "0.22", "0.21", "0.20"],
        }
        perf_table(cost_data)
        st.markdown("TailScore maintains a small edge over volatility even after realistic transaction costs. Sharpe stays positive across all cost scenarios.")

# ════════════════════════════════════════
# PAGE: KEY FINDINGS
# ════════════════════════════════════════
elif page == "Key Findings":
    st.title("Key Findings & Conclusion")
    st.markdown("---")

    st.success("### What We Found")
    st.markdown("""
    1. **CVaR (TailScore) and LowVol load on the same underlying defensive risk dimension.** The two strategies are highly correlated in realized returns and show nearly identical factor exposures.

    2. **Long-short CVaR portfolios do not generate statistically significant alpha** after controlling for FF5 + Momentum. The strategy's returns can be explained by known risk premia.

    3. **Long-only CVaR portfolios perform consistently well** (Sharpe 0.70, 116% cumulative return) but behave very similarly to low-volatility strategies.

    4. **TailScore is not a separately priced characteristic** in Fama-MacBeth cross-sectional tests. Stocks with safer tails do not earn reliably higher returns after controls.

    5. **The short leg is unstable and destroys value**, confirming these are better used as defensive long-only characteristics.

    6. **Beta hedging dramatically improves performance**, isolating the signal from market direction.

    7. **Results are robust** across lookback windows, tail thresholds, and after transaction costs.
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.error("""
        ### Practical Implication
        More complex downside-tail measures do not outperform simpler volatility-based strategies. 
        For most investors, a standard low-volatility approach captures the same defensive premium 
        with less complexity.
        """)
    with col2:
        st.info("""
        ### Theoretical Implication
        Defensive risk premia appear unified within standard multifactor models. Markets do not 
        separately price "tail-risk safety" versus "low-volatility safety" as distinct sources 
        of compensation.
        """)

# ── Footer ──
st.sidebar.markdown("---")
st.sidebar.markdown("[GitHub Repository](https://github.com/ArjunDeshmukh16/CVaR-Left-Tail-Factor-Strategy)")
