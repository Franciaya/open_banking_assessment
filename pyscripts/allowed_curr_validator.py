class AllowedCurrencyValidator:
    def __init__(self, allowed_currencies):
        self.allowed_currencies = allowed_currencies

    def validate(self, currency):
        return currency in self.allowed_currencies