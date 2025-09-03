import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan EMI Calculator", page_icon="💰")

st.title("💰 Loan EMI & Total Payment Calculator")

# --- User Inputs ---
loan_amount = st.number_input("Enter Loan Amount (₹)", min_value=10000, value=3000000, step=10000, format="%i")
annual_rate = st.number_input("Enter Annual Interest Rate (%)", min_value=0.1, max_value=100.0, value=11.5, step=0.1)
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

# --- Chart ---
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

# ============================
# SECTION 2: Dynamic EMI
# ============================

st.header("📈 Custom / Dynamic EMI Simulator")

custom_emi = st.number_input("Enter Your Custom Monthly EMI (₹)", min_value=1000, value=int(emi), step=1000, format="%i")

remaining_principal = loan_amount
total_paid_dynamic = 0
months_dynamic = 0

while remaining_principal > 0:
    # Interest for the current month
    interest_for_month = remaining_principal * monthly_rate
    principal_payment = custom_emi - interest_for_month

    if principal_payment <= 0:
        st.error("❌ EMI too small! Loan will never close. Increase custom EMI.")
        break

    if principal_payment > remaining_principal:
        principal_payment = remaining_principal
        custom_payment = interest_for_month + principal_payment
    else:
        custom_payment = custom_emi

    remaining_principal -= principal_payment
    total_paid_dynamic += custom_payment
    months_dynamic += 1

if remaining_principal <= 0:
    st.subheader("📊 Dynamic EMI Results")
    st.write(f"**Custom EMI Entered:** ₹{custom_emi:,.2f}")
    st.write(f"**Total Payment (Principal + Interest):** ₹{total_paid_dynamic:,.2f}")
    st.write(f"**Total Interest Paid:** ₹{total_paid_dynamic - loan_amount:,.2f}")
    st.write(f"**Loan Closure Time:** {months_dynamic} months ({months_dynamic//12} years {months_dynamic%12} months)")
