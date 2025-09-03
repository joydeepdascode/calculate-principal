import streamlit as st

st.set_page_config(page_title="Loan EMI Calculator", page_icon="💰")

st.title("💰 Loan EMI & Total Payment Calculator")

# --- User Inputs ---
loan_amount = st.number_input("Enter Loan Amount (₹)", min_value=10000, value=3000000, step=10000, format="%i")
annual_rate = st.number_input("Enter Annual Interest Rate (%)", min_value=0.1, max_value=100.0, value=11.75, step=0.1)
months = st.number_input("Enter Tenure (in Months)", min_value=1, max_value=600, value=120, step=1)

# --- EMI Calculation ---
monthly_rate = annual_rate / 1200  # (divide by 12 months and by 100 for %)
n = months

if monthly_rate > 0:
    emi = (loan_amount * monthly_rate * (1 + monthly_rate)**n) / ((1 + monthly_rate)**n - 1)
else:
    emi = loan_amount / n

total_payment = emi * n
total_interest = total_payment - loan_amount

# --- Results ---
st.subheader("📊 Loan Summary")
st.write(f"**Monthly EMI:** ₹{emi:,.2f}")
st.write(f"**Total Payment (Principal + Interest):** ₹{total_payment:,.2f}")
st.write(f"**Total Interest Paid:** ₹{total_interest:,.2f}")

# --- Optional Chart ---
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.pie(
    [loan_amount, total_interest],
    labels=["Principal", "Interest"],
    autopct="%1.1f%%",
    startangle=90,
    colors=["#4CAF50", "#FF7043"]
)
ax.set_title("Principal vs Interest Breakdown")
st.pyplot(fig)
