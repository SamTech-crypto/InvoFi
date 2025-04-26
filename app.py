import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Mock blockchain interaction (replace with Web3.py for real blockchain)
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

# Initialize mock blockchain
blockchain = MockBlockchain()

# Streamlit app
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