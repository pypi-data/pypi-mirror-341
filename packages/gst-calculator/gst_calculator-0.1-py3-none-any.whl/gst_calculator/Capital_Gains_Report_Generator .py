import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class CapitalGainsReportGenerator:
    def __init__(self, real_estate_indexation=False):
        self.transactions = []
        self.fifo_inventory = []
        self.report_data = []
        self.buy_data = []
        self.real_estate_indexation = real_estate_indexation

    def input_transactions(self):
        print("🔹 Enter your transactions one by one. Type 'done' to finish.\n")
        while True:
            tx_type = input("Type (BUY/SELL or 'done' to finish): ").strip().upper()
            if tx_type == 'DONE':
                break
            if tx_type not in ['BUY', 'SELL']:
                print("❌ Invalid type. Use 'BUY' or 'SELL'.")
                continue

            try:
                date_str = input("Date (YYYY-MM-DD): ").strip()
                tx_date = datetime.strptime(date_str, "%Y-%m-%d")
                quantity = float(input("Quantity: ").strip())
                price = float(input("Price per unit: ").strip())
                asset_type = input("Asset Type (EQUITY/PROPERTY/BONDS/UNLISTED SHARES): ").strip().upper()

                transaction = {
                    'Date': tx_date,
                    'Type': tx_type,
                    'Quantity': quantity,
                    'Price': price,
                    'AssetType': asset_type
                }

                self.transactions.append(transaction)
                if tx_type == 'BUY':
                    self.buy_data.append({
                        'Date': tx_date.date(),
                        'Price': price,
                        'Quantity': quantity,
                        'AssetType': asset_type
                    })

            except Exception as e:
                print(f"⚠️ Error: {e}. Please re-enter this transaction.\n")

        self.transactions.sort(key=lambda x: x['Date'])

    def generate_report(self):
        asset_tax_rules = {
            'EQUITY': {'LTCG_days': 365, 'STCG_tax': 0.15, 'LTCG_tax': 0.10},
            'PROPERTY': {
                'LTCG_days': 730,
                'STCG_tax': 0.20,
                'LTCG_tax': 0.20 if self.real_estate_indexation else 0.125
            },
            'BONDS': {'LTCG_days': 1095, 'STCG_tax': 0.20, 'LTCG_tax': 0.10},
            'UNLISTED SHARES': {'LTCG_days': 730, 'STCG_tax': 0.20, 'LTCG_tax': 0.20}
        }

        for tx in self.transactions:
            if tx['Type'] == 'BUY':
                self.fifo_inventory.append(tx.copy())
            elif tx['Type'] == 'SELL':
                qty_to_sell = tx['Quantity']
                asset_type = tx['AssetType']

                while qty_to_sell > 0 and self.fifo_inventory:
                    buy_tx = self.fifo_inventory.pop(0)
                    used_qty = min(qty_to_sell, buy_tx['Quantity'])
                    holding_days = (tx['Date'] - buy_tx['Date']).days

                    if asset_type in asset_tax_rules:
                        rules = asset_tax_rules[asset_type]
                        if holding_days > rules['LTCG_days']:
                            gain_type = 'LTCG'
                            tax_rate = rules['LTCG_tax']
                        else:
                            gain_type = 'STCG'
                            tax_rate = rules['STCG_tax']
                    else:
                        continue

                    gain = (tx['Price'] - buy_tx['Price']) * used_qty
                    tax = gain * tax_rate
                    self.report_data.append({
                        'AssetType': asset_type,
                        'BuyDate': buy_tx['Date'].date(),
                        'SellDate': tx['Date'].date(),
                        'BuyPrice': buy_tx['Price'],
                        'SellPrice': tx['Price'],
                        'Quantity': used_qty,
                        'HoldingDays': holding_days,
                        'Gain': round(gain, 2),
                        'Tax': round(tax, 2),
                        'Type': gain_type,
                        'RateApplied': f"{int(tax_rate * 100)}%"
                    })

                    if buy_tx['Quantity'] > used_qty:
                        buy_tx['Quantity'] -= used_qty
                        self.fifo_inventory.insert(0, buy_tx)
                    qty_to_sell -= used_qty

        return pd.DataFrame(self.report_data)

    def save_to_excel(self, filename="capital_gains_report.xlsx"):
        os.makedirs("capital_gains_reports", exist_ok=True)
        filepath = os.path.join("capital_gains_reports", filename)
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            pd.DataFrame(self.report_data).to_excel(writer, sheet_name='Capital Gains', index=False)
            pd.DataFrame(self.buy_data).to_excel(writer, sheet_name='All Buy Transactions', index=False)
        print(f"✅ Excel report saved to {filepath}")

    def generate_pdf(self, filename="CapitalGains_Summary.pdf"):
        output_folder = "capital_gains_pdfs"
        os.makedirs(output_folder, exist_ok=True)
        path = os.path.join(output_folder, filename)

        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4

        def draw_table(title, data, headers, start_y):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, start_y, title)
            y = start_y - 20
            c.setFont("Helvetica", 8)
            for i, header in enumerate(headers):
                c.drawString(40 + i * 60, y, header)
            y -= 15
            for row in data:
                for i, key in enumerate(headers):
                    val = str(row.get(key, ""))
                    c.drawString(40 + i * 60, y, val)
                y -= 12
                if y < 60:
                    c.showPage()
                    y = height - 60
                    c.setFont("Helvetica", 8)
            return y - 30

        y_pos = height - 50
        y_pos = draw_table(
            "Capital Gains Report (FIFO)",
            self.report_data,
            ["BuyDate", "SellDate", "BuyPrice", "SellPrice", "Quantity", "Gain", "Tax", "Type", "RateApplied"],
            y_pos
        )

        draw_table(
            "All Buy Transactions",
            self.buy_data,
            ["Date", "Price", "Quantity", "AssetType"],
            y_pos
        )

        c.save()
        print(f"📄 PDF generated at {path}")


if __name__ == "__main__":
    use_indexation = input("Use indexation for PROPERTY assets? (yes/no): ").strip().lower() == "yes"
    report_generator = CapitalGainsReportGenerator(real_estate_indexation=use_indexation)

    report_generator.input_transactions()
    report_df = report_generator.generate_report()
    print("\n📊 Final Report:")
    print(report_df)

    report_generator.save_to_excel("capital_gains_report.xlsx")
    report_generator.generate_pdf("CapitalGains_Summary.pdf")
