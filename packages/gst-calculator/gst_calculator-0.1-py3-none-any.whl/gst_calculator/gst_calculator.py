import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import numpy as np

# Custom Exceptions
class InvalidDataFormatError(Exception):
    def __init__(self):
        super().__init__("Invalid data format. Please enter a valid numeric value.")

class InvalidYesNoInputError(Exception):
    def __init__(self):
        super().__init__("Invalid input. Please enter 'yes' or 'no'.")

# GST Reconciliation Class
class GSTReconciliation:
    def __init__(self):
        self.purchases = pd.DataFrame()
        self.sales = pd.DataFrame()

    def manual_input(self):
        purchase_data = []
        print("\nEnter purchase details (Month, InvoiceNo, GST). Type 'done' to finish:")
        while True:
            month = input("Month (e.g., April, May, etc.): ")  # Example input
            if month.lower() == 'done':
                break
            invoice_no = input("InvoiceNo (e.g., 12345): ")  # Example input
            gst = input("GST (e.g., 18.00): ")  # Example input
            try:
                gst = float(gst)
            except ValueError:
                raise InvalidDataFormatError()
            purchase_data.append([month, invoice_no, gst])
        
        self.purchases = pd.DataFrame(purchase_data, columns=['Month', 'InvoiceNo', 'GST'])
        
        sales_data = []
        print("\nEnter sales details (Month, InvoiceNo, GST). Type 'done' to finish:")
        while True:
            month = input("Month (e.g., April, May, etc.): ")  # Example input
            if month.lower() == 'done':
                break
            invoice_no = input("InvoiceNo (e.g., 67890): ")  # Example input
            gst = input("GST (e.g., 18.00): ")  # Example input
            try:
                gst = float(gst)
            except ValueError:
                raise InvalidDataFormatError()
            sales_data.append([month, invoice_no, gst])
        
        self.sales = pd.DataFrame(sales_data, columns=['Month', 'InvoiceNo', 'GST'])

    def reconcile(self):
        self._validate_columns()
        
        purchase_gst = self.purchases.groupby('Month')['GST'].sum()
        sales_gst = self.sales.groupby('Month')['GST'].sum()

        comparison = pd.concat([purchase_gst, sales_gst], axis=1)
        comparison.columns = ['InputGST', 'OutputGST']
        comparison.fillna(0, inplace=True)
        comparison['NetGSTPayable'] = np.subtract(comparison['OutputGST'], comparison['InputGST'])
        comparison['ITC_Status'] = np.where(comparison['InputGST'] >= 0, 'Valid', 'Not Claimable')

        return comparison.reset_index()

    def find_mismatched_invoices(self):
        purchase_invoices = set(self.purchases['InvoiceNo'])
        sales_invoices = set(self.sales['InvoiceNo'])

        missing_in_purchases = sales_invoices - purchase_invoices
        missing_in_sales = purchase_invoices - sales_invoices

        return {
            'MissingInPurchases': list(missing_in_purchases),
            'MissingInSales': list(missing_in_sales)
        }

    def generate_pdf_report(self, reconciliation_result, mismatches):
        os.makedirs("pdf_reports", exist_ok=True)
        pdf_file = "pdf_reports/gst_reconciliation_report.pdf"
        c = canvas.Canvas(pdf_file, pagesize=A4)
        width, height = A4  # Size of the A4 page in points

        # Title
        c.setFont("Helvetica", 12)
        c.drawString(200, height - 40, "GST Reconciliation Report (2025-26)")

        # Table headers
        c.drawString(30, height - 80, "Month")
        c.drawString(100, height - 80, "InputGST")
        c.drawString(180, height - 80, "OutputGST")
        c.drawString(260, height - 80, "NetGSTPayable")
        c.drawString(360, height - 80, "ITC Status")

        # Table rows
        y_position = height - 100
        for idx, row in reconciliation_result.iterrows():
            c.drawString(30, y_position, str(row['Month']))
            c.drawString(100, y_position, f"{row['InputGST']:.2f}")
            c.drawString(180, y_position, f"{row['OutputGST']:.2f}")
            c.drawString(260, y_position, f"{row['NetGSTPayable']:.2f}")
            c.drawString(360, y_position, row['ITC_Status'])
            y_position -= 20

        # Mismatched invoices section
        y_position -= 30
        c.drawString(30, y_position, "Mismatched Invoices:")
        
        y_position -= 20
        c.drawString(30, y_position, "Missing in Purchases:")
        y_position -= 20
        for invoice in mismatches['MissingInPurchases']:
            c.drawString(30, y_position, invoice)
            y_position -= 15

        y_position -= 20
        c.drawString(30, y_position, "Missing in Sales:")
        y_position -= 20
        for invoice in mismatches['MissingInSales']:
            c.drawString(30, y_position, invoice)
            y_position -= 15

        # Save the PDF
        c.save()
        print(f"✅ GST reconciliation PDF report saved to '{pdf_file}'")

    def _validate_columns(self):
        required_columns = {'Month', 'GST', 'InvoiceNo'}
        for df_name, df in [('purchases', self.purchases), ('sales', self.sales)]:
            missing = required_columns - set(df.columns)
            if missing:
                raise ValueError(f"Missing columns in {df_name}: {missing}")

# Menu-driven CLI
def menu():
    while True:
        print("\n--- GST Reconciliation Tool ---")
        print("1. Enter data manually")
        print("2. Exit")
        choice = input("Enter your choice (1/2): ").strip()

        if choice == '1':
            gst.manual_input()
            break
        elif choice == '2':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    gst = GSTReconciliation()
    menu()

    # Reconciliation
    result = gst.reconcile()
    result.to_excel("gst_reconciliation_report.xlsx", index=False)
    print("✅ GST reconciliation report saved to 'gst_reconciliation_report.xlsx'")

    # Mismatched invoices
    mismatches = gst.find_mismatched_invoices()
    with open("gst_mismatch_report.txt", "w") as f:
        f.write("MISSING IN PURCHASES:\n")
        f.write("\n".join(mismatches['MissingInPurchases']) + "\n\n")
        f.write("MISSING IN SALES:\n")
        f.write("\n".join(mismatches['MissingInSales']))
    print("⚠️ Mismatch report saved to 'gst_mismatch_report.txt'")

    # Generate PDF Report
    gst.generate_pdf_report(result, mismatches)