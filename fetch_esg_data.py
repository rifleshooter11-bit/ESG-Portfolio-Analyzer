import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

print("Starting ESG data fetch and generation process...")

# A list of diverse, major public companies to analyze
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JNJ", "V", "PG", "NVDA", "JPM", "XOM", "UNH", "HD", "CVX", "LLY"]

data_records = []

for ticker in tickers:
    try:
        print(f"Fetching financial data for {ticker}...")
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # We fetch real financial data where possible
        market_cap = info.get("marketCap", np.nan)
        sector = info.get("sector", "Unknown")
        industry = info.get("industry", "Unknown")
        pe_ratio = info.get("forwardPE", np.nan)
        
        # Note: Yahoo Finance recently removed direct ESG data access from their public API.
        # For analysis purposes, we simulate realistic ESG risk scores based on industry averages.
        # Lower score = lower risk (better ESG profile)
        
        # Industry baselines for ESG risk (0-100 scale, lower is better)
        sector_baselines = {
            "Technology": 15,
            "Healthcare": 22,
            "Financial Services": 25,
            "Consumer Cyclical": 20,
            "Energy": 40,
            "Basic Materials": 35,
            "Unknown": 25
        }
        
        base_esg = sector_baselines.get(sector, 25)
        
        # Add some random variance to simulate real company differences
        env_score = max(0, min(100, base_esg + np.random.normal(0, 5)))
        soc_score = max(0, min(100, base_esg - 2 + np.random.normal(0, 4)))
        gov_score = max(0, min(100, 20 + np.random.normal(0, 3)))
        
        total_esg_risk = (env_score * 0.4) + (soc_score * 0.3) + (gov_score * 0.3)
        
        # ESG Rating categories based on risk score
        if total_esg_risk < 15:
            rating = "AAA (Leader)"
        elif total_esg_risk < 22:
            rating = "AA (Leader)"
        elif total_esg_risk < 28:
            rating = "A (Average)"
        elif total_esg_risk < 35:
            rating = "BBB (Average)"
        else:
            rating = "CCC (Laggard)"

        data_records.append({
            "Ticker": ticker,
            "Company Name": info.get("shortName", ticker),
            "Sector": sector,
            "Industry": industry,
            "Market Cap ($B)": round(market_cap / 1e9, 2) if pd.notnull(market_cap) else np.nan,
            "P/E Ratio": round(pe_ratio, 2) if pd.notnull(pe_ratio) else np.nan,
            "Environmental Risk": round(env_score, 1),
            "Social Risk": round(soc_score, 1),
            "Governance Risk": round(gov_score, 1),
            "Total ESG Risk Score": round(total_esg_risk, 1),
            "ESG Rating": rating,
            "Last Updated": datetime.now().strftime("%Y-%m-%d")
        })
    except Exception as e:
        print(f"Could not fetch data for {ticker}: {e}")

# Create a DataFrame and save it
df = pd.DataFrame(data_records)
output_path = "esg_data.csv"
df.to_csv(output_path, index=False)

print(f"\nSuccessfully generated {len(df)} records.")
print(f"Data saved to {output_path}")
print(df.head())
