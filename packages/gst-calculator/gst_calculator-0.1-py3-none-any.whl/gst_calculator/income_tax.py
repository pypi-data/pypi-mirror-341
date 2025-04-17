import os
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

class InvalidIncomeError(Exception):
    def __init__(self):
        super().__init__("Invalid income amount. It must be greater than zero.")

class InvalidSalariedStatusError(Exception):
    def __init__(self):
        super().__init__("Invalid input for salaried status. Choose 'yes' or 'no'.")

class IncomeTaxCalculator:
    def __init__(self, name, annual_income, is_salaried):
        self.name = name
        self.annual_income = annual_income
        self.is_salaried = is_salaried
        self.standard_deduction = 75000 if is_salaried else 50000
        self.taxable_income = max(0, annual_income - self.standard_deduction)
        self.tax = 0
        self.surcharge = 0
        self.health_edu_cess = 0
        self.total_tax = 0
        self.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    def calculate_tax(self):
        slabs = [
            (300000, 0.00),
            (600000, 0.05),
            (900000, 0.10),
            (1200000, 0.15),
            (1500000, 0.20),
            (float('inf'), 0.30)
        ]
        
        tax = 0
        prev_limit = 0
        
        for limit, rate in slabs:
            if self.taxable_income > prev_limit:
                taxable_at_this_slab = min(self.taxable_income, limit) - prev_limit
                tax += taxable_at_this_slab * rate
            prev_limit = limit
        
        self.tax = round(tax, 2)
    
    def calculate_surcharge(self):
        if self.taxable_income > 5000000:
            if self.taxable_income <= 10000000:
                self.surcharge = round(self.tax * 0.10, 2)
            elif self.taxable_income <= 20000000:
                self.surcharge = round(self.tax * 0.15, 2)
            elif self.taxable_income <= 50000000:
                self.surcharge = round(self.tax * 0.25, 2)
            else:
                self.surcharge = round(self.tax * 0.37, 2)
    
    def calculate_health_edu_cess(self):
        self.health_edu_cess = round(0.04 * (self.tax + self.surcharge), 2)
    
    def apply_rebate(self):
        rebate_limit = 1200000
        max_rebate = 25000
        
        if self.taxable_income <= rebate_limit and self.tax <= max_rebate:
            self.total_tax = 0
        else:
            self.total_tax = self.tax + self.surcharge + self.health_edu_cess

    def get_report_text(self):
        return (
            f"\n{'='*40}\n"
            f"INCOME TAX CALCULATION REPORT (FY 2024-25)\n"
            f"{'='*40}\n"
            f"Name: {self.name}\n"
            f"Date & Time of Generation: {self.timestamp}\n"
            f"Annual Income: ₹{self.annual_income:,.2f}\n"
            f"Salaried: {'Yes' if self.is_salaried else 'No'}\n"
            f"Standard Deduction: ₹{self.standard_deduction:,.2f}\n"
            f"Taxable Income: ₹{self.taxable_income:,.2f}\n"
            f"Base Tax: ₹{self.tax:,.2f}\n"
            f"Surcharge: ₹{self.surcharge:,.2f}\n"
            f"Health & Education Cess (4%): ₹{self.health_edu_cess:,.2f}\n"
            f"{'-'*40}\n"
            f"TOTAL TAX DUE: ₹{self.total_tax:,.2f}\n"
            f"{'='*40}\n"
        )

    def generate_tax_report_pdf(self):
        folder = "tax_slips"
        os.makedirs(folder, exist_ok=True)

        filename = f"{self.name.replace(' ', '_')}.pdf"
        filepath = os.path.join(folder, filename)

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 40, "INCOME TAX CALCULATION REPORT (FY 2024-25)")

        c.setFont("Helvetica", 12)
        y = height - 80
        line_height = 18

        details = [
            f"Name: {self.name}",
            f"Date & Time of Generation: {self.timestamp}",
            f"Annual Income: ₹{self.annual_income:,.2f}",
            f"Salaried: {'Yes' if self.is_salaried else 'No'}",
            f"Standard Deduction: ₹{self.standard_deduction:,.2f}",
            f"Taxable Income: ₹{self.taxable_income:,.2f}",
            f"Base Tax: ₹{self.tax:,.2f}",
            f"Surcharge: ₹{self.surcharge:,.2f}",
            f"Health & Education Cess (4%): ₹{self.health_edu_cess:,.2f}",
            "-" * 40,
            f"TOTAL TAX DUE: ₹{self.total_tax:,.2f}"
        ]

        for detail in details:
            c.drawString(40, y, detail)
            y -= line_height

        c.setFont("Helvetica-Oblique", 10)
        c.drawRightString(width - 40, 20 * mm, f"Generated on: {self.timestamp}")
        c.save()

        print(f"\n✅ Tax slip saved as: {filepath}")

def run_tax_calculator():
    print("Income Tax Calculator (New Regime 2024-25)")
    print("=" * 40)
    
    try:
        name = input("Enter your full name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")

        income_input = input("Enter your annual income (₹): ").strip()
        if not income_input.replace('.', '', 1).isdigit():
            raise InvalidIncomeError()
        
        annual_income = float(income_input)
        if annual_income <= 0:
            raise InvalidIncomeError()
        
        is_salaried = input("Are you a salaried individual? (yes/no): ").strip().lower()
        if is_salaried not in ["yes", "no"]:
            raise InvalidSalariedStatusError()
        
        is_salaried = is_salaried == "yes"
        
        calculator = IncomeTaxCalculator(name, annual_income, is_salaried)
        calculator.calculate_tax()
        calculator.calculate_surcharge()
        calculator.calculate_health_edu_cess()
        calculator.apply_rebate()

        # CLI output
        print(calculator.get_report_text())

        # PDF output
        calculator.generate_tax_report_pdf()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tax_calculator()