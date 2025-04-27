import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import io

# ---------- Styling ----------
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            background-attachment: fixed;
            background-size: cover;
            color: #000000;
        }

        .floating-header {
            position: sticky;
            top: 0;
            background-color: rgba(255,255,255,0.85);
            padding: 10px;
            z-index: 999;
            backdrop-filter: blur(10px);
            border-bottom: 2px solid #0066cc;
        }

        .card {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .stButton > button {
            color: white;
            background-color: #0066cc;
            border: none;
            padding: 0.5em 1.2em;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 102, 204, 0.6);
            transition: all 0.4s ease-in-out;
            animation: glow 1.8s infinite alternate;
        }

        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 102, 204, 1);
            cursor: pointer;
        }

        @keyframes glow {
            from {
                box-shadow: 0 0 10px rgba(0, 102, 204, 0.6);
            }
            to {
                box-shadow: 0 0 20px rgba(0, 102, 204, 1);
            }
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Mock Blockchain ----------
class MockBlockchain:
    def __init__(self):
        self.invoices = []

    def create_invoice(self, issuer, amount, currency, due_date):
        invoice = {
            "id": len(self.invoices) + 1,
            "issuer": issuer,
            "amount": amount,
            "currency": currency,
            "due_date": due_date,
            "status": "Pending",
            "financed": False
        }
        self.invoices.append(invoice)
        return invoice

    def finance_invoice(self, invoice_id):
        for invoice in self.invoices:
            if invoice["id"] == invoice_id:
                invoice["financed"] = True
                invoice["status"] = "Financed"
                return invoice
        return None

# ---------- Helper: Exchange Rate ----------
def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate.host/latest?base={from_currency}&symbols={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data['rates'].get(to_currency, 1)

# ---------- Helper: CSV Export ----------
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ---------- Smart Contract Simulation ----------
class SmartContract:
    def __init__(self, invoice_id, amount, terms):
        self.invoice_id = invoice_id
        self.amount = amount
        self.terms = terms
        self.status = "Pending"

    def execute(self):
        if self.terms == "30 days":
            self.status = "Executed"
            return f"✅ Contract for Invoice #{self.invoice_id} executed."
        else:
            return f"⚠️ Contract for Invoice #{self.invoice_id} not executed due to terms."

# ---------- Supplier Profiles ----------
suppliers = {
    1: {"name": "Supplier A", "contact": "123-456-7890", "payment_terms": "30 days"},
    2: {"name": "Supplier B", "contact": "987-654-3210", "payment_terms": "45 days"}
}

# ---------- App Start ----------
blockchain = MockBlockchain()
st.markdown('<div class="floating-header"><h2> Blockchain Supply Chain Finance</h2></div>', unsafe_allow_html=True)

# ---------- Create Invoice ----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧾 Create Invoice")

    issuer = st.text_input("Issuer Name")
    amount = st.number_input("Invoice Amount", min_value=0.0, step=100.0)
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "KES", "NGN"])
    due_date = st.date_input("Due Date", min_value=datetime.today())

    if st.button("Create Invoice"):
        if issuer and amount and due_date:
            invoice = blockchain.create_invoice(issuer, amount, currency, due_date.strftime("%Y-%m-%d"))
            st.success(f"✅ Invoice #{invoice['id']} created in {currency}!")
        else:
            st.error("❌ Please fill in all fields.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- View Invoices ----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📄 Invoice List")

    if blockchain.invoices:
        df = pd.DataFrame(blockchain.invoices)
        st.dataframe(df)

        # Finance Invoice
        invoice_id = st.selectbox("Select Invoice to Finance", [inv["id"] for inv in blockchain.invoices])
        if st.button("Finance Invoice"):
            financed_invoice = blockchain.finance_invoice(invoice_id)
            if financed_invoice:
                st.success(f"💰 Invoice #{invoice_id} financed!")
            else:
                st.error("❌ Invoice not found.")

        # Currency Conversion
        st.markdown("### 💱 Convert Currency")
        base = st.selectbox("From", ["USD", "EUR", "GBP", "KES", "NGN"])
        target = st.selectbox("To", ["USD", "EUR", "GBP", "KES", "NGN"])
        amount_to_convert = st.number_input("Amount to Convert", min_value=0.0, step=10.0)
        if st.button("Convert"):
            rate = get_exchange_rate(base, target)
            st.success(f"🔁 {amount_to_convert} {base} ≈ {amount_to_convert * rate:.2f} {target}")

        # Export to CSV
        st.markdown("### 📤 Export Data")
        csv = convert_df_to_csv(df)
        st.download_button(
            label="Download Invoices as CSV",
            data=csv,
            file_name='invoices.csv',
            mime='text/csv'
        )
    else:
        st.info("ℹ️ No invoices created yet.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Supplier & Smart Contract ----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏭 Supplier Info & Smart Contract")

    selected_supplier = st.selectbox("Select Supplier", list(suppliers.keys()))
    supplier = suppliers[selected_supplier]
    st.write(f"**Name**: {supplier['name']}")
    st.write(f"**Contact**: {supplier['contact']}")
    st.write(f"**Terms**: {supplier['payment_terms']}")

    # Simulate Smart Contract
    if st.button("Execute Contract"):
        simulated = SmartContract(invoice_id=selected_supplier, amount=1000, terms=supplier['payment_terms'])
        result = simulated.execute()
        st.write(result)
    st.markdown("</div>", unsafe_allow_html=True)
