import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Custom Exceptions
class InvalidEntityTypeError(Exception):
    def __init__(self):
        super().__init__("Invalid entity type. Choose from 'private limited', 'public limited', 'partnership', 'llp', or 'proprietorship'.")

class InvalidDataFormatError(Exception):
    def __init__(self):
        super().__init__("Invalid data format. Please enter a valid numeric value.")

class InvalidNumberEntryError(Exception):
    def __init__(self):
        super().__init__("Invalid profit amount. Profit must be greater than zero.")

class InvalidYesNoInputError(Exception):
    def __init__(self):
        super().__init__("Invalid input. Please enter 'yes' or 'no'.")

# Tax Calculator Class
class TaxCalculator:
    def __init__(self, company_type, profit, is_foreign=False):
        self.company_type = company_type.lower()
        self.profit = profit
        self.is_foreign = is_foreign

        self.tax = 0
        self.surcharge = 0
        self.health_edu_cess = 0
        self.total_tax = 0

    def calculate_corporate_tax(self):
        if self.is_foreign:
            tax_rate = 40
        else:
            tax_rate = 25 if self.profit <= 400_00_00_000 else 30
        self.tax = (tax_rate / 100) * self.profit
        self.apply_surcharge_and_cess()
        return self.total_tax

    def calculate_partnership_or_llp_tax(self):
        self.tax = 30 / 100 * self.profit
        self.apply_surcharge_and_cess()
        return self.total_tax

    def calculate_proprietorship_tax(self):
        p = self.profit
        if p <= 2_50_000:
            self.tax = 0
        elif p <= 5_00_000:
            self.tax = 5 / 100 * (p - 2_50_000)
        elif p <= 10_00_000:
            self.tax = (5 / 100 * 2_50_000) + (20 / 100 * (p - 5_00_000))
        else:
            self.tax = (5 / 100 * 2_50_000) + (20 / 100 * 5_00_000) + (30 / 100 * (p - 10_00_000))
        self.apply_surcharge_and_cess()
        return self.total_tax

    def apply_surcharge_and_cess(self):
        if self.is_foreign:
            self.surcharge = (5 / 100) * self.tax if self.profit > 10_00_00_000 else (2 / 100) * self.tax if self.profit > 1_00_00_000 else 0
        else:
            self.surcharge = (12 / 100) * self.tax if self.profit > 10_00_00_000 else (7 / 100) * self.tax if self.profit > 1_00_00_000 else 0
        self.health_edu_cess = 4 / 100 * (self.tax + self.surcharge)
        self.total_tax = self.tax + self.surcharge + self.health_edu_cess

    def compute_tax(self):
        if self.company_type in ["private limited", "public limited"]:
            return self.calculate_corporate_tax()
        elif self.company_type in ["partnership", "llp"]:
            return self.calculate_partnership_or_llp_tax()
        elif self.company_type == "proprietorship":
            return self.calculate_proprietorship_tax()
        else:
            raise InvalidEntityTypeError()

    def generate_tax_report(self):
        details = self.company_type.title()
        if self.is_foreign:
            details += " (Foreign)"

        return {
            "Company Type": details,
            "Profit (₹)": self.profit,
            "Base Tax (₹)": round(self.tax, 2),
            "Surcharge (₹)": round(self.surcharge, 2),
            "Cess (₹)": round(self.health_edu_cess, 2),
            "Total Tax (₹)": round(self.total_tax, 2)
        }

    def generate_pdf(self, company_name="Business_Entity"):
        os.makedirs("pdf_reports", exist_ok=True)
        # Sanitize company name for filename
        safe_name = company_name.strip().replace(' ', '_').replace('/', '_').replace('\\', '_')
        if not safe_name or safe_name.upper() == "N/A":
            safe_name = "Business_Entity"

        filename = f"pdf_reports/{safe_name}_TaxReport.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 14)
        c.drawString(160, height - 50, "Corporate Tax Report")

        y = height - 100
        for k, v in self.generate_tax_report().items():
            value = f"₹{v:,.2f}" if isinstance(v, (int, float)) else v
            c.drawString(50, y, f"{k}: {value}")
            y -= 20

        c.save()
        print(f"PDF generated: {filename}")

# Manual Input
def manual_tax_calculator():
    print("\nManual Tax Entry")
    print("=" * 30)
    company_type_map = {
        "private": "private limited",
        "public": "public limited",
        "partnership": "partnership",
        "llp": "llp",
        "proprietorship": "proprietorship"
    }

    try:
        name = input("Enter Business Name: ").strip()
        company_input = input("Enter company type (Private/Public/Partnership/LLP/Proprietorship): ").strip().lower()
        company_type = company_type_map.get(company_input, company_input)
        if company_type not in company_type_map.values():
            raise InvalidEntityTypeError()

        profit_input = input("Enter profit amount (₹): ").strip()
        if not profit_input.replace('.', '', 1).isdigit():
            raise InvalidDataFormatError()

        profit = float(profit_input)
        if profit <= 0:
            raise InvalidNumberEntryError()

        is_foreign = False
        if company_type in ["private limited", "public limited"]:
            foreign_input = input("Is this a foreign company? (yes/no): ").strip().lower()
            if foreign_input not in ["yes", "no", "y", "n"]:
                raise InvalidYesNoInputError()
            is_foreign = foreign_input in ["yes", "y"]

        calc = TaxCalculator(company_type, profit, is_foreign)
        calc.compute_tax()
        report = calc.generate_tax_report()

        print("\n" + "=" * 40)
        for k, v in report.items():
            print(f"{k}: ₹{v:,.2f}" if isinstance(v, (int, float)) else f"{k}: {v}")
        print("=" * 40)

        calc.generate_pdf(company_name=name)

    except Exception as e:
        print(f"Error: {e}")

# Bulk from Excel
def bulk_tax_from_excel(file="business_tax.xlsx"):
    try:
        df = pd.read_excel(file)
    except FileNotFoundError:
        print("Excel file not found.")
        return

    results = []
    for idx, row in df.iterrows():
        try:
            business_name = row.get('BusinessName')
            if pd.isna(business_name) or not str(business_name).strip():
                business_name = f"Entity_{idx+1}"

            calc = TaxCalculator(
                company_type=row['CompanyType'],
                profit=row['Profit'],
                is_foreign=row.get('IsForeign', False)
            )
            calc.compute_tax()
            report = calc.generate_tax_report()
            report["Business Name"] = business_name
            calc.generate_pdf(company_name=business_name)
            results.append(report)
        except Exception as e:
            print(f"Skipping entry due to error: {e}")

    pd.DataFrame(results).to_excel("bulk_tax_summary.xlsx", index=False)
    print("Bulk tax report saved as 'bulk_tax_summary.xlsx'.")

# Menu-driven CLI
def menu():
    while True:
        print("\n--- Indian Corporate Tax Calculator ---")
        print("1. Bulk Input from Excel")
        print("2. Manual Entry")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            filename = input("Enter Excel filename [default: business_tax.xlsx]: ").strip()
            if not filename:
                filename = "business_tax.xlsx"
            bulk_tax_from_excel(filename)
        elif choice == '2':
            manual_tax_calculator()
        elif choice == '3':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    menu()