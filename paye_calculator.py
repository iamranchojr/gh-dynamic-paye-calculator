import typing

from tax_rate import TaxRate


EMPTY_TAX_RATES = 'Tax rates cannot be empty. It should contain at least one item'


class PAYECalculatorException(Exception):
    pass


class PAYECalculator:
    """
    This class is used to calculate the PAYE/Income tax of an employee in Ghana
    https://gra.gov.gh/domestic-tax/tax-types/paye/
    """
    _tax_rates: typing.List[TaxRate]

    def __init__(self, tax_rates: typing.List[TaxRate]):
        """
        Initializes a new instance of PAYECalculator with the tax rates provided
        :param tax_rates: tax rates to use for calculating PAYE
        """
        if len(tax_rates) == 0:
            raise PAYECalculatorException(EMPTY_TAX_RATES)

        self._tax_rates = tax_rates
        self._sort_tax_rates()

    @property
    def tax_rates(self) -> typing.List[TaxRate]:
        return self._tax_rates

    def add_tax_rate(self, tax_rate: TaxRate):
        """
        Adds a new tax rate
        :param tax_rate: tax rate to add
        """
        self._tax_rates.append(tax_rate)
        self._sort_tax_rates()

    def remove_tax_rate(self, tax_rate: TaxRate):
        """
        Remove tax rate
        :param tax_rate: tax rate to remove
        """
        self._tax_rates.remove(tax_rate)
        self._sort_tax_rates()

    def _sort_tax_rates(self):
        """
        Sorts tax rates in ascending order using the chargeable income
        """
        def sort_key(tax_rate: TaxRate) -> float:
            return tax_rate.rate_in_percentage

        self._tax_rates.sort(key=sort_key)

    def _validate(self):
        """
        Performs validation to make sure tax rates are not empty.
        This function raises an exception if tax rates are empty
        :return:
        """
        if len(self._tax_rates) == 0:
            raise PAYECalculatorException(EMPTY_TAX_RATES)

    def calculate_paye(self, taxable_income: float) -> float:
        """
        Uses the tax rates provided to calculate the PAYE
        This method calls a private validate method which throws
        an exception of type PAYECalculatorException if tax rates are empty
        :param taxable_income: taxable income to calculate tax for
        :return: calculated tax
        """
        # first, we validate to be on the safer side
        self._validate()

        # create variable to store calculated tax
        paye = 0.0

        # loop through tax rates and calculate tax for each
        for i in range(len(self.tax_rates)):
            # get next tax rate
            next_tax_rate = (
                self.tax_rates[i + 1]
                if i < len(self.tax_rates) - 1
                else None
            )

            current_tax_rate = self.tax_rates[i]
            if not next_tax_rate or taxable_income <= current_tax_rate.cumulative_income:
                # tax no further
                break

            # calculate tax and add it to paye
            tax = current_tax_rate.calculate_tax(
                taxable_income=taxable_income,
                next_tax_rate=next_tax_rate
            )
            paye += tax

        # return calculated PAYE in 2 decimal places
        return round(number=paye, ndigits=2)
