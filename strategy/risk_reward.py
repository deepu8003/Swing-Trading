class RiskReward:

    def calculate(
        self,
        entry,
        stop_loss,
        target
    ):

        risk = entry - stop_loss

        reward = target - entry

        if risk <= 0:
            rr = 0
        else:
            rr = round(
                reward / risk,
                2
            )

        return {
            "risk": round(risk, 2),
            "reward": round(reward, 2),
            "risk_reward": rr
        }