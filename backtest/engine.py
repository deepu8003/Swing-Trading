from indicators.technical import calculate_indicators
from scoring.stock_score import StockScorer


class BacktestEngine:

    def run_backtest(self, df):

        df = calculate_indicators(df)

        scorer = StockScorer()

        trades = []
        position_open = False
        entry_price = 0

        for i in range(60, len(df)):

            current_df = df.iloc[: i + 1]

            score_data = scorer.calculate_score(
                current_df
            )

            close = current_df.iloc[-1]["Close"]

            if (
                score_data["recommendation"]
                in ["BUY", "STRONG BUY"]
                and not position_open
            ):

                entry_price = close
                position_open = True

            elif (
                score_data["recommendation"]
                in ["SELL", "HOLD"]
                and position_open
            ):

                exit_price = close

                profit = (
                    (exit_price - entry_price)
                    / entry_price
                ) * 100

                trades.append(profit)

                position_open = False

        return self.generate_report(
            trades
        )

    def generate_report(self, trades):

        total_trades = len(trades)

        if total_trades == 0:

            return {
                "total_trades": 0,
                "win_rate": 0,
                "total_return": 0,
                "profit_factor": 0
            }

        wins = [
            x for x in trades
            if x > 0
        ]

        losses = [
            x for x in trades
            if x < 0
        ]

        win_rate = (
            len(wins)
            / total_trades
        ) * 100

        total_return = sum(trades)

        gross_profit = sum(wins)

        gross_loss = abs(
            sum(losses)
        )

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else gross_profit
        )

        return {
            "total_trades": total_trades,
            "win_rate": round(win_rate, 2),
            "total_return": round(total_return, 2),
            "profit_factor": round(
                profit_factor,
                2
            )
        }