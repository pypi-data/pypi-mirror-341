class InvalidInvestmentError(Exception):
    def __init__(self):
        super().__init__("Invalid investment amount. It must be a positive number.")

class InvestmentTaxBenefitCalculator:
    def __init__(self, section_80c=0, section_80d=0, nps=0):
        if section_80c < 0 or section_80d < 0 or nps < 0:
            raise InvalidInvestmentError()
        self.section_80c = section_80c
        self.section_80d = section_80d
        self.nps = nps

        self.max_80c_limit = 150_000
        self.max_80d_limit = 25_000
        self.max_nps_limit = 50_000
        self.total_deduction = 0

    def calculate_tax_benefits(self):
        allowed_80c = min(self.section_80c, self.max_80c_limit)
        allowed_80d = min(self.section_80d, self.max_80d_limit)
        allowed_nps = min(self.nps, self.max_nps_limit)
        self.total_deduction = allowed_80c + allowed_80d + allowed_nps
        return self.total_deduction

    def generate_investment_benefit_report(self):
        report = (
            f"\n{'='*40}\n"
            f"INVESTMENT TAX BENEFITS REPORT\n"
            f"{'='*40}\n"
            f"Section 80C Investment: ₹{self.section_80c:,.2f} (Max Allowed: ₹{self.max_80c_limit:,.2f})\n"
            f"Section 80D Investment: ₹{self.section_80d:,.2f} (Max Allowed: ₹{self.max_80d_limit:,.2f})\n"
            f"NPS Contribution: ₹{self.nps:,.2f} (Max Allowed: ₹{self.max_nps_limit:,.2f})\n"
            f"{'-'*40}\n"
            f"Total Deduction: ₹{self.total_deduction:,.2f}\n"
            f"{'='*40}"
        )
        return report

try:
    c80 = float(input("Enter amount invested under Section 80C: ₹"))
    d80 = float(input("Enter amount invested under Section 80D (Health Insurance): ₹"))
    nps = float(input("Enter amount contributed to NPS: ₹"))

    calculator = InvestmentTaxBenefitCalculator(c80, d80, nps)
    calculator.calculate_tax_benefits()
    print(calculator.generate_investment_benefit_report())

except ValueError:
    print("Error: Please enter valid numeric values for investments.")
except InvalidInvestmentError as e:
    print(f"Error: {e}")
