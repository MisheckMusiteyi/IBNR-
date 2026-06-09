# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date
import re

st.set_page_config(page_title="IBNR Calculator:Percentage Method", layout="wide")

# ---------- CUSTOM CSS (African Actuarial Consultants theme) ----------
st.markdown("""
<style>
    /* Global */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Calisto MT', serif;
        font-size: 11pt;
    }

    /* Apply Calisto MT to all text elements */
    body, p, h1, h2, h3, h4, h5, h6, div, span, label, .stMarkdown,
    .stTextInput label, .stDateInput label, .stSelectbox label, .stMultiSelect label,
    .stButton button, .stDownloadButton button, .stFileUploader label,
    .stAlert, .stInfo, .stWarning, .stError, .stSuccess, .stSpinner,
    .stProgress, .stToast, .stSidebar, .stMetric, .stExpander {
        font-family: 'Calisto MT', serif !important;
    }

    /* Header / Navigation */
    .header {
        background-color: #000000;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        border-bottom: 3px solid #D4AF37;
    }
    .nav-links a {
        color: #FFFFFF;
        margin-left: 2rem;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
        font-family: 'Calisto MT', serif;
    }
    .nav-links a:hover {
        color: #D4AF37;
    }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        color: #FFFFFF;
        padding: 2rem 2rem;
        text-align: center;
        border-bottom: 3px solid #D4AF37;
    }
    .hero h1 {
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-family: 'Calisto MT', serif;
    }
    .hero p {
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
        font-family: 'Calisto MT', serif;
    }

    /* Main container */
    .main-container {
        max-width: 1400px;
        margin: 2rem auto;
        padding: 0 2rem;
    }

    /* Required Column Containers */
    .required-container {
        background-color: #F9F9F9;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        min-height: 120px;
        height: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
        margin-bottom: 1rem;
    }
    .required-container h3 {
        color: #D4AF37;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .required-container p {
        color: #666666;
        font-size: 0.85rem;
        margin-bottom: 0;
        line-height: 1.3;
    }

    /* Date Range Container */
    .date-range-container {
        background-color: #F9F9F9;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .date-range-container h3 {
        color: #D4AF37;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .date-range-container p {
        color: #666666;
        font-size: 0.85rem;
        margin-bottom: 0;
    }

    /* Percentage Input Container */
    .percentage-container {
        background-color: #F9F9F9;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .percentage-container h3 {
        color: #D4AF37;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: bold;
    }

    /* Data Check Containers */
    .data-check-container {
        background-color: #E3F2FD;
        border: 2px solid #2196F3;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .data-check-warning {
        background-color: #FFF3E0;
        border: 2px solid #FF9800;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .data-check-error {
        background-color: #FFEBEE;
        border: 2px solid #F44336;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
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
        margin-top: 0;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
        font-family: 'Calisto MT', serif;
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
        font-family: 'Calisto MT', serif;
    }

    /* Streamlit element overrides */
    .stButton > button, .stDownloadButton > button {
        background-color: #D4AF37;
        color: #000000;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
        font-family: 'Calisto MT', serif !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #B8960F;
        color: #FFFFFF;
    }

    /* FILE UPLOADER FIX - Hide duplicate text */
    .stFileUploader {
        border: 2px dashed #D4AF37;
        border-radius: 5px;
        padding: 1rem;
    }
    .stFileUploader .e1ewe7hr3 {
        display: none !important;
    }
    .stFileUploader .st-b7 {
        display: none !important;
    }
    .stFileUploader .st-c0 {
        display: none !important;
    }
    .stFileUploader .st-ae {
        display: none !important;
    }
    .stFileUploader label {
        display: none !important;
    }
    .stFileUploader button {
        background-color: #D4AF37 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
    }
    .stFileUploader button:hover {
        background-color: #B8960F !important;
        color: #FFFFFF !important;
    }

    .stMultiSelect [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] {
        border: 1px solid #D4AF37;
        border-radius: 4px;
    }

    .dataframe {
        border: 1px solid #D4AF37;
        border-radius: 8px;
        overflow: hidden;
    }

    /* Fix for select box container */
    .stSelectbox div[data-baseweb="select"] {
        width: 100%;
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
    <p>Upload your premium data (CSV or Excel). Map the columns, select the period, and enter the IBNR percentage. The app calculates IBNR as a percentage of premiums by line of business.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Main Container ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- User inputs ---
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name (for file name)", value="Client").strip()
with col2:
    pass

# --- IBNR Period Selection ---
st.markdown("""
<div class="date-range-container">
    <h3>IBNR Period</h3>
    <p>Select the date range for premiums/Claims to be included in the IBNR calculation (based on Premium/Claim Payment Date)</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input("From Date (Start of IBNR Period)", value=date(2020, 1, 1))
    st.caption("Premiums/Claims with Payment Date on or after this date")
with col2:
    to_date = st.date_input("To Date (End of IBNR Period)", value=date(2024, 12, 31))
    st.caption("Premiums/Claims with Payment Date on or before this date")

from_date = pd.to_datetime(from_date)
to_date = pd.to_datetime(to_date)

st.info(f"**Selected IBNR Period:** {from_date.date()} to {to_date.date()}")

# --- IBNR Percentage Input ---
st.markdown("""
<div class="percentage-container">
    <h3>IBNR Percentage</h3>
    <p>Enter the percentage of premiums/claims to be reserved as IBNR</p>
</div>
""", unsafe_allow_html=True)

ibnr_percentage = st.number_input(
    "IBNR Percentage (%)",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=0.5,
    help="Enter the percentage of premiums/claims that will be reserved as IBNR (e.g., 10% = 0.10)"
) / 100

st.caption(f"Selected IBNR Percentage: {ibnr_percentage * 100:.2f}%")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        original_filename = uploaded_file.name
        base_filename = re.sub(r'\.[^.]*$', '', original_filename)

        # Read file based on extension
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension == 'csv':
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='cp1252')
                st.info("File read with Windows-1252 encoding.")
        else:
            df = pd.read_excel(uploaded_file)

        # Drop unnamed columns
        unnamed = [c for c in df.columns if c.startswith('Unnamed:')]
        if unnamed:
            df = df.drop(columns=unnamed)
            st.info(f"Dropped {len(unnamed)} unnamed column(s).")

        # Preview
        with st.expander("Preview of uploaded data"):
            st.dataframe(df.head())

        # --- Column Mapping Section ---
        st.markdown("### Map Your Columns to Required Fields")
        st.markdown("The calculator requires the following columns. For each required column, select the corresponding column from your uploaded data:")

        all_columns = df.columns.tolist()

        req_col1, req_col2 = st.columns(2)

        with req_col1:
            st.markdown("""
            <div class="required-container">
                <h3>Premium_Date</h3>
                <p>The date when the premium/claim was paid (period for IBNR calculation)</p>
            </div>
            """, unsafe_allow_html=True)
            premium_date_col = st.selectbox(
                "Select your Premium/Claim Date column",
                options=[""] + all_columns,
                key="premium_date"
            )
            if premium_date_col == "":
                premium_date_col = None

        with req_col2:
            st.markdown("""
            <div class="required-container">
                <h3>Line_of_Business</h3>
                <p>The category/segment for grouping results (e.g., Motor, Property, Agriculture)</p>
            </div>
            """, unsafe_allow_html=True)
            lob_col = st.selectbox(
                "Select the Line of Business column",
                options=[""] + all_columns,
                key="lob"
            )
            if lob_col == "":
                lob_col = None

        st.markdown("---")

        if not premium_date_col or not lob_col:
            st.error("Please map all required columns (Premium/Claim_Date, Line_of_Business).")
            st.stop()

        # --- Identify numeric columns for selection ---
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        exclude_cols = [premium_date_col, lob_col]
        for col in exclude_cols:
            if col in numeric_cols:
                numeric_cols.remove(col)

        if not numeric_cols:
            st.error("No numeric columns found in the data. Please ensure you have numeric columns for premium/Claim amounts.")
            st.stop()

        st.markdown("### Select Premium Columns")
        selected_columns = st.multiselect(
            "Choose the columns that contain premium amounts (these will be used to calculate IBNR):",
            options=numeric_cols,
            default=numeric_cols[:min(3, len(numeric_cols))]
        )

        if not selected_columns:
            st.warning("Please select at least one premium/claim column to proceed.")
            st.stop()

        # ============================================================
        # DATA QUALITY CHECKS
        # ============================================================
        st.markdown("### Data Quality Checks")

        all_selected_cols = [premium_date_col, lob_col] + selected_columns
        df_original_len = len(df)
        errors_found = False

        # 1. Missing Values Check
        st.markdown("#### 1. Missing Values Check")
        missing_cols = []
        for col in all_selected_cols:
            if col in df.columns:
                missing_count = df[col].isna().sum()
                if missing_count > 0:
                    missing_cols.append(f"{col} ({missing_count} missing)")
                    errors_found = True

        if missing_cols:
            st.markdown(f"""
            <div class="data-check-error">
                <b>Missing values found in:</b> {', '.join(missing_cols)}<br>
                Please fix missing values and re-upload.
            </div>
            """, unsafe_allow_html=True)
            st.stop()
        else:
            st.markdown('<div class="data-check-container">✅ No missing values found in selected columns.</div>', unsafe_allow_html=True)

        # 2. Duplicate Rows Check (Remove automatically)
        st.markdown("#### 2. Duplicate Rows Check")
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            df = df.drop_duplicates()
            st.markdown(f'<div class="data-check-warning">Removed {duplicate_count} duplicate row(s). {len(df)} rows remaining.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="data-check-container">✅ No duplicate rows found.</div>', unsafe_allow_html=True)

        # 3. Date Conversion Check
        st.markdown("#### 3. Date Conversion Check")
        try:
            test_dates = pd.to_datetime(df[premium_date_col], errors='coerce')
            invalid_dates = test_dates.isna().sum()
            if invalid_dates > 0:
                errors_found = True
                st.markdown(f"""
                <div class="data-check-error">
                    <b>{invalid_dates} invalid date(s) found in Premium/Claim_Date column.</b><br>
                    Please fix these dates and re-upload.
                </div>
                """, unsafe_allow_html=True)
                st.stop()
            else:
                st.markdown('<div class="data-check-container">✅ All dates are valid.</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="data-check-error">
                <b>Date parsing error:</b> {str(e)}<br>
                Please check your Premium/Claim_Date column format.
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        st.markdown("---")

        # --- CREATE CLEAN DATAFRAME ---
        df_clean = pd.DataFrame()
        df_clean['Premium_Date'] = pd.to_datetime(df[premium_date_col], errors='coerce')
        df_clean['Line_of_Business'] = df[lob_col]

        for col in selected_columns:
            df_clean[col] = pd.to_numeric(df[col], errors='coerce')

        df_clean = df_clean.dropna(subset=['Premium_Date', 'Line_of_Business'])

        if df_clean.empty:
            st.error("No valid data found after cleaning. Please check your date columns.")
            st.stop()

        # --- Filter data by IBNR period ---
        df_filtered = df_clean[
            (df_clean['Premium_Date'] >= from_date) &
            (df_clean['Premium_Date'] <= to_date)
        ]

        if df_filtered.empty:
            st.error(f"No data found for the selected IBNR period: {from_date.date()} to {to_date.date()}")
            st.stop()

        st.success(f"**IBNR Period Filter Applied:** {len(df_filtered)} records selected (from {len(df_clean)} total)")

        # --- Calculate IBNR ---
        premium_summary = df_filtered.groupby('Line_of_Business')[selected_columns].sum().reset_index()

        ibnr_summary = premium_summary.copy()
        for col in selected_columns:
            ibnr_summary[f"{col}_IBNR"] = ibnr_summary[col] * ibnr_percentage

        total_premiums = premium_summary[selected_columns].sum()
        total_ibnr = total_premiums * ibnr_percentage

        total_row = {'Line_of_Business': 'TOTAL'}
        for col in selected_columns:
            total_row[col] = total_premiums[col]
            total_row[f"{col}_IBNR"] = total_ibnr[col]

        total_df = pd.DataFrame([total_row])
        ibnr_summary_with_total = pd.concat([ibnr_summary, total_df], ignore_index=True)

        # Display results
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"IBNR Results for Period: {from_date.date()} to {to_date.date()}")
        st.markdown(f"**IBNR Percentage Applied:** {ibnr_percentage * 100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Premium/Claim Summary by Line of Business")
        display_premium = premium_summary.copy()
        for col in selected_columns:
            display_premium[col] = display_premium[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
        st.dataframe(display_premium, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("IBNR by Line of Business")
        display_ibnr = ibnr_summary_with_total.copy()
        for col in display_ibnr.columns:
            if col != 'Line_of_Business':
                display_ibnr[col] = display_ibnr[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
        st.dataframe(display_ibnr, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Prepare Excel downloads with traceable filename
        output_premium = BytesIO()
        with pd.ExcelWriter(output_premium, engine='openpyxl') as writer:
            premium_summary.to_excel(writer, index=False, sheet_name='Premium_Summary')
        output_premium.seek(0)

        output_ibnr = BytesIO()
        with pd.ExcelWriter(output_ibnr, engine='openpyxl') as writer:
            ibnr_summary_with_total.to_excel(writer, index=False, sheet_name='IBNR_Summary')
        output_ibnr.seek(0)

        safe_client = re.sub(r'[\\/*?:"<>|]', "", client_name).strip() or "Client"
        safe_original = re.sub(r'[\\/*?:"<>|]', "", base_filename).strip() or "Data"

        st.markdown("### Download Results")
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            premium_filename = f"{safe_client}_{safe_original}_Premium_Summary_{from_date.year}_{to_date.year}.xlsx"
            st.download_button(
                label="Download Premium/Claim Summary (Excel)",
                data=output_premium,
                file_name=premium_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with dcol2:
            ibnr_filename = f"{safe_client}_{safe_original}_IBNR_Summary_{from_date.year}_{to_date.year}.xlsx"
            st.download_button(
                label="Download IBNR Summary (Excel)",
                data=output_ibnr,
                file_name=ibnr_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Optional: Show detailed calculations
        with st.expander("View Detailed Calculations"):
            st.write("**IBNR Calculation Formula:**")
            st.write(f"IBNR = Premium/Claim Amount × {ibnr_percentage * 100:.2f}%")
            st.write("")
            st.write("**Calculation Steps:**")
            st.write("1. Filter premiums/claims by selected date range")
            st.write("2. Group by Line of Business")
            st.write("3. Sum premium/claim amounts for each line of business")
            st.write(f"4. Multiply total premiums/claims by {ibnr_percentage * 100:.2f}% to calculate IBNR")

            if len(premium_summary) > 0:
                sample_lob = premium_summary.iloc[0]['Line_of_Business']
                sample_premium = premium_summary.iloc[0][selected_columns[0]] if len(selected_columns) > 0 else 0
                sample_ibnr = sample_premium * ibnr_percentage
                st.write("")
                st.write("**Sample Calculation (first line of business):**")
                st.write(f"- Line of Business: {sample_lob}")
                st.write(f"- Premium Amount: {sample_premium:,.2f}")
                st.write(f"- IBNR Percentage: {ibnr_percentage * 100:.2f}%")
                st.write(f"- IBNR Calculation: {sample_premium:,.2f} × {ibnr_percentage:.4f} = {sample_ibnr:,.2f}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.write("Please check your file format and column selections.")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
    <p>© 2026 African Actuarial Consultants. All rights reserved. | <a href="#">Privacy</a> | <a href="#">Terms</a></p>
    <p style="margin-top: 0.5rem; font-size: 0.9rem;">Powered by Vanababa</p>
</div>
""", unsafe_allow_html=True)
