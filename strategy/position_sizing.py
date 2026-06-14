class PositionSizing:

    def calculate(
        self,
        capital,
        risk_percent,
        entry,
        stop_loss
    ):

        risk_amount = (
            capital * risk_percent
        ) / 100

        risk_per_share = (
            entry - stop_loss
        )

        quantity = int(
            risk_amount /
            risk_per_share
        )

        return {
            "risk_amount": round(
                risk_amount,
                2
            ),
            "quantity": quantity
        }