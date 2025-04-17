import re
import os
import numpy as np
import pandas as pd


class InvalidPANError(Exception):
    def __init__(self):
        super().__init__("Invalid PAN format. It must be a 10-character alphanumeric string.")


class InvalidIncomeError(Exception):
    def __init__(self):
        super().__init__("Invalid income amount. Please enter a valid number greater than zero.")


class InvalidCategoryError(Exception):
    def __init__(self):
        super().__init__("Invalid category. Choose from 'individual', 'senior', or 'super_senior'.")


class TDSCalculator:
    SLABS = np.array([
        (0, 3_00_000, 0.00),
        (3_00_001, 6_00_000, 0.05),
        (6_00_001, 9_00_000, 0.10),
        (9_00_001, 12_00_000, 0.15),
        (12_00_001, 15_00_000, 0.20),
        (15_00_001, np.inf, 0.30)
    ])

    def __init__(self, pan, annual_income, category="individual"):
        self.pan = pan.upper()
        self.annual_income = annual_income
        self.category = category.lower()
        self.validate_inputs()

        self.tax = 0
        self.rebate = 0
        self.tds = 0

    def validate_inputs(self):
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', self.pan):
            raise InvalidPANError()
        if not isinstance(self.annual_income, (int, float)) or self.annual_income <= 0:
            raise InvalidIncomeError()
        if self.category not in ['individual', 'senior', 'super_senior']:
            raise InvalidCategoryError()

    def calculate_tax_under_new_regime(self):
        tax = 0
        income = self.annual_income

        for lower, upper, rate in self.SLABS:
            if income > lower:
                taxable = min(upper, income) - lower
                tax += taxable * rate

        self.tax = tax
        self.rebate = min(tax, 25000) if income <= 7_00_000 else 0
        self.tds = max(self.tax - self.rebate, 0)
        cess = 0.04 * self.tds
        self.tds += cess
        return round(self.tds, 2)

    def generate_tds_report(self):
        category_title = self.category.replace("_", " ").title()
        cess_amount = 0.04 * max(self.tax - self.rebate, 0)
        return (
            f"\n{'='*40}\n"
            f"TDS CALCULATION REPORT (New Regime)\n"
            f"{'='*40}\n"
            f"PAN: {self.pan}\n"
            f"Category: {category_title}\n"
            f"Annual Income: ₹{self.annual_income:,.2f}\n"
            f"Calculated Tax: ₹{self.tax:,.2f}\n"
            f"Rebate u/s 87A: ₹{self.rebate:,.2f}\n"
            f"Health & Education Cess (4%): ₹{cess_amount:,.2f}\n"
            f"{'-'*40}\n"
            f"TOTAL TDS DUE: ₹{self.tds:,.2f}\n"
            f"{'='*40}"
        )


def run_tds_calculator_cli():
    print("\nTDS Calculator (India - New Regime)")
    print("=" * 40)
    try:
        pan = input("Enter PAN (e.g., ABCDE1234F): ").strip()
        income_input = input("Enter Annual Income (₹): ").strip()
        annual_income = float(income_input)
        category = input("Enter category (Individual/Senior/Super_Senior): ").strip().lower()

        calc = TDSCalculator(pan, annual_income, category)
        calc.calculate_tax_under_new_regime()
        report = calc.generate_tds_report()
        print(report)

        # Save to Excel
        df = pd.DataFrame([{
            'PAN': pan,
            'Category': category.title(),
            'Annual_Income': annual_income,
            'TDS': calc.tds,
            'Tax': calc.tax,
            'Rebate': calc.rebate
        }])
        df.to_excel("tds_output.xlsx", index=False)
        print("\nSaved to tds_output.xlsx")

    except Exception as e:
        print(f" Error: {e}")


def process_bulk_tds_from_excel(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f" File not found: {filepath}")

    df = pd.read_excel(filepath)
    results = []

    for index, row in df.iterrows():
        try:
            pan = str(row['PAN']).strip().upper()
            income = float(row['Annual_Income'])
            category = str(row.get('Category', 'individual')).lower()

            calc = TDSCalculator(pan, income, category)
            tds_amount = calc.calculate_tax_under_new_regime()

            results.append({
                'PAN': pan,
                'Category': category.title(),
                'Annual_Income': income,
                'TDS': tds_amount,
                'Tax': calc.tax,
                'Rebate': calc.rebate
            })
        except Exception as e:
            results.append({
                'PAN': row.get('PAN'),
                'Category': row.get('Category'),
                'Annual_Income': row.get('Annual_Income'),
                'TDS': 'Error',
                'Error': str(e)
            })

    return pd.DataFrame(results)


def main_menu():
    print("\n========== TDS Calculator ==========")
    print("1. Manual Entry Mode")
    print("2. Bulk Excel Mode")
    print("3. Exit")
    choice = input("Select an option (1/2/3): ").strip()

    if choice == "1":
        run_tds_calculator_cli()

    elif choice == "2":
        filepath = input("Enter Excel file path (e.g., tds_input.xlsx): ").strip()
        try:
            df_result = process_bulk_tds_from_excel(filepath)
            df_result.to_excel("tds_output.xlsx", index=False)
            print("Results written to tds_output.xlsx")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "3":
        print("Exiting... 👋")
    else:
        print("Invalid choice. Please select 1, 2, or 3.")


# Entry point
if __name__ == "__main__":
    main_menu()