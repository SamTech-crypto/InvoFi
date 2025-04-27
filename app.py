import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ----- Background & Button Styling -----
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            background-attachment: fixed;
            background-size: cover;
            color: #000000;
        }

        /* Glowing animated button */
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

# ----- Mock blockchain interaction -----
class MockBlockchain:
    def __init__(self):
        self.invoices = []

    def create_invoice(self, issuer, amount, due_date):
        invoice = {
            "id": len(self.invoices) + 1,
            "issuer": issuer,
            "amount": amount,
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

# ----- Initialize mock blockchain -----
blockchain = MockBlockchain()

# ----- Streamlit App -----
st.title("Blockchain Supply Chain Finance")

# Create Invoice
st.header("Create Invoice")
issuer = st.text_input("Issuer Name")
amount = st.number_input("Invoice Amount (USD)", min_value=0.0, step=100.0)
due_date = st.date_input("Due Date", min_value=datetime.today())

if st.button("Create Invoice"):
    if issuer and amount and due_date:
        invoice = blockchain.create_invoice(issuer, amount, due_date.strftime("%Y-%m-%d"))
        st.success(f"Invoice #{invoice['id']} created successfully!")
    else:
        st.error("Please fill in all fields.")

# View Invoices
st.header("Invoice List")
if blockchain.invoices:
    df = pd.DataFrame(blockchain.invoices)
    st.dataframe(df)

    # Finance Invoice
    invoice_id = st.selectbox("Select Invoice to Finance", [inv["id"] for inv in blockchain.invoices])
    if st.button("Finance Invoice"):
        financed_invoice = blockchain.finance_invoice(invoice_id)
        if financed_invoice:
            st.success(f"Invoice #{invoice_id} financed successfully!")
        else:
            st.error("Invoice not found.")
else:
    st.write("No invoices created yet.")
