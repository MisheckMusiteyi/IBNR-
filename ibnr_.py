# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date
import re

st.set_page_config(page_title="IBNR Calculator:Percentage Method", layout="wide")

# ---------- SIMPLE CUSTOM CSS ----------
st.markdown("""
<style>
    /* Global font */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Calisto MT', serif;
        font-size: 11pt;
    }
    
    /* Headers and text */
    h1, h2, h3, p, div, span, label {
        font-family: 'Calisto MT', serif;
    }
    
    /* Header bar */
    .header {
        background-color: #000000;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        border-bottom: 3px solid #D4AF37;
        margin-bottom: 2rem;
    }
    .nav-links a {
        color: #FFFFFF;
        margin-left: 2rem;
        text-decoration: none;
        font-weight: 500;
    }
    .nav-links a:hover {
        color: #D4AF37;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        color: #FFFFFF;
        padding: 2rem;
        text-align: center;
        border-bottom: 3px solid #D4AF37;
        margin-bottom: 2rem;
    }
    .hero h1 {
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .hero p {
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background-color: #B8960F !important;
        color: #FFFFFF !important;
    }
    
    /* Cards */
    .card {
        background-color: #F9F9F9;
        border: 1px solid #D4AF37;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .card h3 {
        color: #D4AF37;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
    }
    
    /* Footer */
    .footer {
        background-color: #000000;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem;
        border-top: 3px solid #D4AF37;
        margin-top: 3rem;
    }
    .footer a {
        color: #D4AF37;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="header">
    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">Services</a>
        <a href="#">Tools</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <h1>IBNR Percentage Method Calculator</h1>
    <p>Upload your premium data (CSV or Excel). Map the columns, select the period, and enter the IBNR percentage.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Main Content ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# User inputs
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name", value="Client").strip()
with col2:
    pass

# Date range
st.subheader("IBNR Period")
col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input("From Date", value=date(2020, 1, 1))
with col2:
    to_date = st.date_input("To Date", value=date(2024, 12, 31))

from_date = pd.to_datetime(from_date)
to_date = pd.to_datetime(to_date)

st.info(f"**Selected Period:** {from_date.date()} to {to_date.date()}")

# Percentage input
st.subheader("IBNR Percentage")
ibnr_percentage = st.number_input(
    "Percentage (%)",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=0.5
) / 100
st.caption(f"Selected: {ibnr_percentage * 100:.2f}%")

# File uploader - SIMPLE VERSION
uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        original_filename = uploaded_file.name
        base_filename = re.sub(r'\.[^.]*$', '', original_filename)

        # Read file
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == 'csv':
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='cp1252')
        else:
            df = pd.read_excel(uploaded_file)

        # Clean up
        unnamed = [c for c in df.columns if 'Unnamed' in c]
        if unnamed:
            df = df.drop(columns=unnamed)

        st.write("### Preview of your data")
        st.dataframe(df.head())

        # Column selection
        st.write("### Map Your Columns")
        all_cols = df.columns.tolist()

        col1, col2 = st.columns(2)
        with col1:
            date_col = st.selectbox("Date column (premium/claim date)", ["Select..."] + all_cols)
        with col2:
            lob_col = st.selectbox("Line of Business column", ["Select..."] + all_cols)

        if date_col == "Select..." or lob_col == "Select...":
            st.warning("Please select both columns to continue.")
            st.stop()

        # Numeric columns
        num_cols = [c for c in all_cols if c not in [date_col, lob_col]]
        if not num_cols:
            st.error("No numeric columns found.")
            st.stop()

        amount_cols = st.multiselect("Select premium/claim amount columns", num_cols)

        if not amount_cols:
            st.warning("Please select at least one amount column.")
            st.stop()

        # Data quality checks
        st.write("### Data Quality Checks")

        # Check missing values
        missing_found = False
        for col in [date_col, lob_col] + amount_cols:
            missing = df[col].isna().sum()
            if missing > 0:
                st.error(f"Column '{col}' has {missing} missing values. Please fix and re-upload.")
                missing_found = True
        if missing_found:
            st.stop()

        # Convert dates
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            if df[date_col].isna().sum() > 0:
                st.error(f"Could not parse some dates in '{date_col}'. Please check format.")
                st.stop()
        except Exception as e:
            st.error(f"Date conversion error: {e}")
            st.stop()

        # Remove duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            df = df.drop_duplicates()
            st.info(f"Removed {dup_count} duplicate rows.")

        # Filter by date range
        mask = (df[date_col] >= from_date) & (df[date_col] <= to_date)
        df_filtered = df[mask].copy()

        if df_filtered.empty:
            st.error(f"No data found for period {from_date.date()} to {to_date.date()}")
            st.stop()

        st.success(f"✅ {len(df_filtered)} records after filtering")

        # Calculate summary
        st.write("### Results")

        premium_summary = df_filtered.groupby(lob_col)[amount_cols].sum().reset_index()

        ibnr_summary = premium_summary.copy()
        for col in amount_cols:
            ibnr_summary[f"{col}_IBNR"] = ibnr_summary[col] * ibnr_percentage

        # Add total row
        total_row = {lob_col: "TOTAL"}
        for col in amount_cols:
            total_row[col] = premium_summary[col].sum()
            total_row[f"{col}_IBNR"] = total_row[col] * ibnr_percentage

        ibnr_summary = pd.concat([ibnr_summary, pd.DataFrame([total_row])], ignore_index=True)

        # Display
        st.subheader("Premium Summary")
        display_premium = premium_summary.copy()
        for col in amount_cols:
            display_premium[col] = display_premium[col].apply(lambda x: f"{x:,.2f}")
        st.dataframe(display_premium)

        st.subheader("IBNR Summary")
        display_ibnr = ibnr_summary.copy()
        for col in display_ibnr.columns:
            if col != lob_col:
                display_ibnr[col] = display_ibnr[col].apply(lambda x: f"{x:,.2f}")
        st.dataframe(display_ibnr)

        # Download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            ibnr_summary.to_excel(writer, index=False, sheet_name='IBNR_Summary')

        safe_client = re.sub(r'[\\/*?:"<>|]', "", client_name).strip() or "Client"
        safe_original = re.sub(r'[\\/*?:"<>|]', "", base_filename).strip() or "Data"
        filename = f"{safe_client}_{safe_original}_IBNR_Summary.xlsx"

        st.download_button("📥 Download IBNR Summary", data=output.getvalue(), file_name=filename)

    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
    <p>© 2026 African Actuarial Consultants. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
