import pandas as pd
from datetime import datetime

# Define applicable TDS rates and thresholds (simplified for demonstration)
TDS_RATES = {
    '194A': {'rate': 0.10, 'threshold': 40000},
    '194I': {'rate': 0.10, 'threshold': 600000},
    '194H': {'rate': 0.05, 'threshold': 15000},
    '194T': {'rate': 0.10, 'threshold': 20000},
    '194S': {'rate': 0.01, 'threshold': 10000},
}

class TDSValidator:
    def __init__(self, file):
        self.data = pd.read_csv(file)
        self.data['PaymentDate'] = pd.to_datetime(self.data['PaymentDate'])
        self.data['TDSDate'] = pd.to_datetime(self.data['TDSDate'], errors='coerce')

    def validate(self):
        report = []

        for _, row in self.data.iterrows():
            section = str(row['Section'])
            payment = row['Amount']
            tds_amount = row['TDSAmount']
            pan = str(row.get('PAN', ''))
            is_non_filer = row.get('IsNonFiler', False)

            # Check if TDS is applicable based on threshold
            threshold = TDS_RATES.get(section, {}).get('threshold', 0)
            expected_rate = TDS_RATES.get(section, {}).get('rate', 0.10)

            # PAN not available → 20%
            if not pan or pan.strip() == '':
                expected_rate = max(expected_rate, 0.20)

            # Non-filer → higher TDS under 206AB
            if is_non_filer:
                expected_rate = max(expected_rate, expected_rate * 2, 0.05)

            expected_tds = round(payment * expected_rate, 2)
            missing_tds = pd.isna(tds_amount) or tds_amount == 0
            under_deducted = not missing_tds and tds_amount < expected_tds

            delay = 0
            interest = 0
            if not pd.isna(row['TDSDate']):
                delay = (row['TDSDate'] - row['PaymentDate']).days
                if delay > 30:
                    interest = round((delay - 30) * 0.01 * tds_amount, 2)

            report.append({
                'Vendor': row['Vendor'],
                'Section': section,
                'PaymentDate': row['PaymentDate'].date(),
                'Amount': payment,
                'TDSAmount': tds_amount,
                'ExpectedTDS': expected_tds,
                'TDSDate': row['TDSDate'].date() if not pd.isna(row['TDSDate']) else '',
                'MissingTDS': missing_tds,
                'UnderDeducted': under_deducted,
                'LateByDays': delay if delay > 30 else 0,
                'InterestPayable': interest,
                'PAN': pan,
                'IsNonFiler': is_non_filer,
                'TDSRateUsed': round(tds_amount / payment, 4) if payment > 0 and not pd.isna(tds_amount) else 0,
                'ExpectedRate': expected_rate
            })

        df = pd.DataFrame(report)
        df.to_excel("tds_compliance_report.xlsx", index=False)
        print("TDS compliance report saved as 'tds_compliance_report.xlsx'.")

if __name__ == "__main__":
    validator = TDSValidator("tds_data.csv")
    validator.validate()