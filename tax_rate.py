INVALID_CHARGEABLE_INCOME = 'Invalid Chargeable Income. Value should not be less than 0'
INVALID_CUMULATIVE_INCOME = 'Invalid Cumulative Income. Value should not be less than 0'
INVALID_TAX_RATE = 'Invalid value provided. Rate should be between 0 and 100'


class TaxRateException(Exception):
    pass


class TaxRate:
    _rate_in_percentage: float
    _chargeable_income: float
    _cumulative_income: float

    def __init__(
        self,
        rate_in_percentage: float,
        chargeable_income: float,
        cumulative_income: float,
    ):
        """
        Initialize a new instance of tax rate
        with provided rate and chargeable income
        :param rate_in_percentage: rate in percentage
        :param chargeable_income: chargeable income
        :param cumulative_income: cumulative income
        """
        # validate data
        if rate_in_percentage < 0 or rate_in_percentage > 100:
            raise TaxRateException(INVALID_TAX_RATE)

        if chargeable_income < 0:
            raise TaxRateException(INVALID_CHARGEABLE_INCOME)

        if cumulative_income < 0:
            raise TaxRateException(INVALID_CUMULATIVE_INCOME)

        self._rate_in_percentage = rate_in_percentage
        self._chargeable_income = chargeable_income
        self._cumulative_income = cumulative_income

    @property
    def rate_in_decimal(self) -> float:
        return self._rate_in_percentage / 100

    @property
    def rate_in_percentage(self) -> float:
        return self._rate_in_percentage

    @property
    def cumulative_income(self) -> float:
        return self._cumulative_income

    @property
    def chargeable_income(self) -> float:
        return self._chargeable_income

    def calculate_tax(
            self,
            taxable_income: float,
            next_tax_rate,
    ) -> float:
        """
        Calculates and returns the tax for amount provided
        :param taxable_income: taxable income to calculate tax for
        :param next_tax_rate: next tax rate income to use for comparison
        :return: tax amount
        """
        # subtract the Chargeable Income from the amount
        result = taxable_income - self._cumulative_income

        # compare the result with the chargeable income
        if next_tax_rate and result > next_tax_rate.chargeable_income:
            # if it is greater than chargeable income,
            # calculate the tax rate on the chargeable income
            return next_tax_rate.chargeable_income * next_tax_rate.rate_in_decimal

        # else, perform the tax on the result

        if next_tax_rate:
            # if next tax rate, use the rate in decimal of the next tax rate
            return result * next_tax_rate.rate_in_decimal

        # use the rate in decimal of the current tax rate
        return result * self.rate_in_decimal
