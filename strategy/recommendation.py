from strategy.support_resistance import SupportResistance
from strategy.risk_reward import RiskReward


class RecommendationEngine:

    def generate_trade_plan(self, df):

        sr = SupportResistance()

        levels = sr.calculate(df)

        entry = levels["current_price"]

        stop_loss = levels["support"]

        target = levels["resistance"]

        rr = RiskReward().calculate(
            entry,
            stop_loss,
            target
        )

        return {

            "entry": entry,

            "stop_loss": stop_loss,

            "target": target,

            "risk": rr["risk"],

            "reward": rr["reward"],

            "risk_reward":
            rr["risk_reward"]
        }