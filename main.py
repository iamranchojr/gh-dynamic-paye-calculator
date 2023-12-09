from paye_calculator import PAYECalculator
from tax_rate import TaxRate

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create tax rates
    tax_rate_to_remove = TaxRate(
        rate_in_percentage=100,
        chargeable_income=100000,
        cumulative_income=100000,
    )

    tax_rates = [
        tax_rate_to_remove,
        TaxRate(
            rate_in_percentage=0,
            chargeable_income=402,
            cumulative_income=402,
        ),
        TaxRate(
            rate_in_percentage=5,
            chargeable_income=110,
            cumulative_income=512,
        ),
        TaxRate(
            rate_in_percentage=10,
            chargeable_income=130,
            cumulative_income=642,
        ),
        TaxRate(
            rate_in_percentage=17.5,
            chargeable_income=3000,
            cumulative_income=3642,
        ),
        TaxRate(
            rate_in_percentage=30,
            chargeable_income=29963,
            cumulative_income=50000,
        ),
    ]

    # create an instance of the PAYECalculator with the tax rates
    # NOTE: The initializer will throw an exception if tax rates is empty
    paye_calculator = PAYECalculator(tax_rates=tax_rates)

    # add a new tax rate using the method
    paye_calculator.add_tax_rate(
        tax_rate=TaxRate(
            rate_in_percentage=25,
            chargeable_income=16395,
            cumulative_income=20037,
        )
    )
    paye_calculator.add_tax_rate(
        tax_rate=TaxRate(
            rate_in_percentage=35,
            chargeable_income=50000,
            cumulative_income=50000
        )
    )

    # remove a tax rate using the remove method
    paye_calculator.remove_tax_rate(
        tax_rate=tax_rate_to_remove
    )

    taxable_income = 4231.29
    paye = paye_calculator.calculate_paye(taxable_income)
    print(f'PAYE of Taxable Income {taxable_income} is {paye}')
