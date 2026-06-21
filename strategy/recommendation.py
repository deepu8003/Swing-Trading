from strategy.support_resistance import SupportResistance
from strategy.risk_reward import RiskReward


class RecommendationEngine:

    def generate_trade_plan(self, df):

        latest = df.iloc[-1]

        sr = SupportResistance()
        levels = sr.calculate(df)

        entry = latest["Close"]

        atr = latest["ATR"]

        # =====================================
        # SETUP TYPE
        # =====================================

        if latest["BREAKOUT"]:

            setup_type = "BREAKOUT"

            entry = latest["Close"]

            stop_loss = (
                entry - (2 * atr)
            )

            target = (
                entry + (4 * atr)
            )

        elif latest["PULLBACK"]:

            setup_type = "PULLBACK"

            entry = latest["Close"]

            stop_loss = (
                entry - (1.5 * atr)
            )

            target = (
                entry + (3 * atr)
            )

        else:

            setup_type = "NORMAL"

            entry = latest["Close"]

            stop_loss = max(
                levels["support"],
                entry - (2 * atr)
            )

            target = max(
                levels["resistance"],
                entry + (4 * atr)
            )

        # =====================================
        # RISK REWARD
        # =====================================

        rr = RiskReward().calculate(
            entry,
            stop_loss,
            target
        )

        # =====================================
        # TRADE QUALITY
        # =====================================

        if rr["risk_reward"] >= 3:

            trade_quality = (
                "EXCELLENT"
            )

        elif rr["risk_reward"] >= 2:

            trade_quality = (
                "GOOD"
            )

        elif rr["risk_reward"] >= 1.5:

            trade_quality = (
                "AVERAGE"
            )

        else:

            trade_quality = (
                "POOR"
            )

        # =====================================
        # OUTPUT
        # =====================================

        return {

            "setup_type":
            setup_type,

            "entry":
            round(entry, 2),

            "stop_loss":
            round(stop_loss, 2),

            "target":
            round(target, 2),

            "risk":
            round(
                rr["risk"],
                2
            ),

            "reward":
            round(
                rr["reward"],
                2
            ),

            "risk_reward":
            round(
                rr["risk_reward"],
                2
            ),

            "trade_quality":
            trade_quality
        }


# from strategy.support_resistance import SupportResistance
# from strategy.risk_reward import RiskReward


# class RecommendationEngine:

#     def generate_trade_plan(self, df):

#         sr = SupportResistance()

#         levels = sr.calculate(df)

#         entry = levels["current_price"]

#         stop_loss = levels["support"]

#         target = levels["resistance"]

#         rr = RiskReward().calculate(
#             entry,
#             stop_loss,
#             target
#         )

#         return {

#             "entry": entry,

#             "stop_loss": stop_loss,

#             "target": target,

#             "risk": rr["risk"],

#             "reward": rr["reward"],

#             "risk_reward":
#             rr["risk_reward"]
#         }
