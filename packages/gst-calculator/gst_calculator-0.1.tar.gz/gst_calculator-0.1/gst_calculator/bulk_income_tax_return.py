import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class IncomeTaxCalculator:
    def __init__(self, name, pan, basic, hra, other, ded_80c, ded_80d, age=30, city_type="non-metro"):
        self.name = name
        self.pan = pan
        self.basic = basic
        self.hra = hra
        self.other = other
        self.ded_80c = min(ded_80c, 150000)
        self.ded_80d = min(ded_80d, 50000 if age >= 60 else 25000)
        self.age = age
        self.city_type = city_type.lower()
        self.gross_income = basic + hra + other
        self.hra_exemption = self.calculate_hra_exemption()
        self.taxable_income = max(0, self.gross_income - self.hra_exemption - self.ded_80c - self.ded_80d - 50000)  # standard deduction
        self.tax = 0
        self.surcharge = 0
        self.cess = 0
        self.total_tax = 0
        self.calculate_tax()

    def calculate_hra_exemption(self):
        rent_paid = 0.4 * self.basic  # assume rent = 40% of basic for now
        limit1 = self.hra
        limit2 = rent_paid - 0.1 * self.basic
        limit3 = 0.5 * self.basic if self.city_type == "metro" else 0.4 * self.basic
        return max(0, min(limit1, limit2, limit3))

    def calculate_tax(self):
        # ✅ New Tax Regime Slabs for FY 2025-26
        slabs = [
            (300000, 0.00),
            (600000, 0.05),
            (900000, 0.10),
            (1200000, 0.15),
            (1500000, 0.20),
            (float('inf'), 0.30)
        ]

        tax = 0
        prev = 0
        for limit, rate in slabs:
            if self.taxable_income > prev:
                tax += (min(limit, self.taxable_income) - prev) * rate
            prev = limit

        # Rebate under section 87A
        if self.taxable_income <= 700000:
            tax = 0

        self.tax = round(tax, 2)
        self.cess = round(0.04 * self.tax, 2)
        self.total_tax = round(self.tax + self.cess, 2)

    def get_summary(self):
        return {
            "Name": self.name,
            "PAN": self.pan,
            "Gross Income": self.gross_income,
            "HRA Exemption": self.hra_exemption,
            "80C Deduction": self.ded_80c,
            "80D Deduction": self.ded_80d,
            "Standard Deduction": 50000,
            "Taxable Income": self.taxable_income,
            "Tax": self.tax,
            "Cess": self.cess,
            "Total Tax Payable": self.total_tax
        }

    def generate_pdf(self):
        os.makedirs("pdf_slips", exist_ok=True)
        filename = f"pdf_slips/{self.name.replace(' ', '_')}_TaxSlip.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(180, height - 50, "Income Tax Slip (FY 2025-26)")

        c.setFont("Helvetica", 11)
        y = height - 100
        for k, v in self.get_summary().items():
            c.drawString(50, y, f"{k}: ₹{v:,.2f}" if isinstance(v, (int, float)) else f"{k}: {v}")
            y -= 20

        c.save()
        print(f"PDF generated: {filename}")

def calculate_bulk_tax_from_excel(file="salary_sheet.xlsx"):
    try:
        df = pd.read_excel(file)
    except FileNotFoundError:
        print("Excel file not found. Please ensure 'salary_sheet.xlsx' exists.")
        return

    summaries = []

    for _, row in df.iterrows():
        calc = IncomeTaxCalculator(
            name=row['Name'],
            pan=row['PAN'],
            basic=row['BasicSalary'],
            hra=row['HRA'],
            other=row['OtherAllowances'],
            ded_80c=row['Deductions_80C'],
            ded_80d=row['Deductions_80D'],
            age=row.get('Age', 30),
            city_type=row.get('CityType', 'non-metro')
        )
        summaries.append(calc.get_summary())
        calc.generate_pdf()

    result_df = pd.DataFrame(summaries)
    result_df.to_excel("tax_summary.xlsx", index=False)
    print("Bulk tax calculation completed. Output saved to tax_summary.xlsx")

def runtime_pdf_input():
    print("\nGenerate PDF Slip for Individual Employee (From Excel)")
    name = input("Name: ").strip()
    pan = input("PAN: ").strip().upper()

    file = "salary_sheet.xlsx"
    try:
        df = pd.read_excel(file)
    except FileNotFoundError:
        print("Excel file not found. Please ensure 'salary_sheet.xlsx' exists.")
        return

    match = df[(df['Name'].str.strip().str.lower() == name.lower()) & (df['PAN'].str.strip().str.upper() == pan)]

    if match.empty:
        print("No matching record found in the Excel file.")
        return

    row = match.iloc[0]

    emp = IncomeTaxCalculator(
        name=row['Name'],
        pan=row['PAN'],
        basic=row['BasicSalary'],
        hra=row['HRA'],
        other=row['OtherAllowances'],
        ded_80c=row['Deductions_80C'],
        ded_80d=row['Deductions_80D'],
        age=row.get('Age', 30),
        city_type=row.get('CityType', 'non-metro')
    )

    print("\n" + "-" * 40)
    for k, v in emp.get_summary().items():
        print(f"{k}: ₹{v:,.2f}" if isinstance(v, (int, float)) else f"{k}: {v}")
    print("-" * 40)

    emp.generate_pdf()

def main():
    print("\n" + "=" * 40)
    print("Income Tax Calculator - FY 2025-26")
    print("=" * 40)
    print("1. Bulk Tax Calculation from Excel")
    print("2. Generate PDF for One Employee (Name & PAN only)")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        calculate_bulk_tax_from_excel()
    elif choice == '2':
        runtime_pdf_input()
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
