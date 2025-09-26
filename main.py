from dotenv import load_dotenv
import ast
import os
import pandas as pd
from tools import finnhub_client,historicals,web_scrapper,custom_financial_calc as cfc,general,llms

# Load .env file only if not running in production (e.g., GitHub Actions)
if not os.getenv("GITHUB_ACTIONS"):  # This var is auto-set in GitHub Actions
    load_dotenv()

def main():

    symbol_list = ast.literal_eval(os.environ.get("SYMBOLS_INTEREST_LIST", "[]"))
    
    top_losers_data = finnhub_client.analyze_market_losers_from_interest_list(symbol_list)

    trading_advisor_df = pd.DataFrame(top_losers_data)

    for loser in top_losers_data:

        symbol=loser['symbol']
        current_price=loser['current_price']
        # get historical data        
        hist_data = historicals.get_historical_data(symbol)
        
        # get interest metrics
        metrics = cfc.evaluate_buy_interest(symbol,hist_data,current_price)

        # get trading view opinion
        td_opinion = web_scrapper.get_trading_view_opinion(symbol)

        # add opinions
        general.add_opinion(symbol,trading_advisor_df,"manual_financial_analysis",metrics["evaluation"])
        general.add_opinion(symbol,trading_advisor_df,"trading_view_opinion",td_opinion)

        if "failed" not in metrics["evaluation"]:
            general.add_opinion(symbol,trading_advisor_df,"llm_opinion",llms.get_llm_signals_analysis( metrics["signals"],symbol,current_price))
        else:
            general.add_opinion(symbol,trading_advisor_df,"llm_opinion","error: metrics not provided")
    
    trading_advisor_df = general.generate_decision_column(trading_advisor_df)    
    trading_advisor_df.to_csv("resources/report.csv", index=False)

    # TODO: review transactions
    # TODO: filtrar por 'BUY' en decisiones
    # TODO: send email
    
if __name__ == "__main__":
    main()
