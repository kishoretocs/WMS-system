import streamlit as st
import pandas as pd
from fuzzywuzzy import process

st.set_page_config(page_title="SKU to MSKU Web App", layout="wide")
st.title("📦 SKU → MSKU Mapper & Dashboard")

# Upload Sales CSV
sales_file = st.file_uploader("📂 Upload Sales CSV", type=["csv"])
inventory_file = st.file_uploader("📦 Upload Inventory CSV", type=["csv"])
combo_file = st.file_uploader("🧩 Upload Combo Definitions CSV", type=["csv"])

if sales_file and inventory_file and combo_file:
    sales_df = pd.read_csv(sales_file)
    msku_df = pd.read_csv(inventory_file,header=1)
    combo_df = pd.read_csv(combo_file,header=1)

    st.subheader("🧾 Uploaded Sales Data")
    st.dataframe(sales_df)

    # Step 1: Prepare Inventory & Combo Data
    msku_set = set(msku_df["msku"].dropna())
    item_to_combo = {}
    for _, row in combo_df.iterrows():
        for col in [c for c in combo_df.columns if c.startswith("SKU")]:
            sku = row[col]
            if pd.notna(sku):
                item_to_combo[sku] = row["Combo"]

    # Step 2: Matching
    threshold = st.slider("🎯 Matching Threshold", 70, 100, 85)

    def map_one(sku):
        if pd.isna(sku): return None, None
        if sku in msku_set: return sku, None
        if sku in item_to_combo: return item_to_combo[sku], sku
        best, score = process.extractOne(sku, list(msku_set))
        return best if score >= threshold else None, None

    if st.button("🔍 Map SKUs"):
        results = [map_one(s) for s in sales_df["sku"]]
        sales_df["mapped_msku"] = [m for m, _ in results]
        sales_df["via_combo"] = [bool(c) for _, c in results]

        st.success("✅ Mapping Complete")
        st.dataframe(sales_df)

        # Metrics
        st.header("📊 Dashboard")
        total = len(sales_df)
        mapped = sales_df["mapped_msku"].notna().sum()
        via_combo = sales_df["via_combo"].sum()
        unmapped = total - mapped

        st.metric("Total SKUs", total)
        st.metric("Mapped SKUs", mapped)
        st.metric("Mapped via Combo", via_combo)
        st.metric("Unmapped SKUs", unmapped)

        # Download Cleaned CSV
        cleaned_csv = sales_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Cleaned CSV", cleaned_csv, "cleaned_sales.csv", "text/csv")
