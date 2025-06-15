import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import io

st.set_page_config(page_title="SKU Mapper (Multi‑sheet)", layout="wide")
st.title("📦 SKU→MSKU Mapper – Multi‑Sheet WMS")

def sheet_csv_url(sheet_id, gid):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# --- Load Data ---
WMS_ID = "1ORu33oTA1KcLMkyjmujcBjdzfavOnkUJJJKxujFq2Fw"

# Sheet 2: Inventory / MSKU
inv_url = sheet_csv_url(WMS_ID, "1359739976")
msku_df = pd.read_csv(inv_url, header=1)
st.subheader("✅ Inventory / MSKU Data (Sheet 2)")
st.dataframe(msku_df)
if "msku" not in msku_df.columns:
    st.error("Sheet 2 must contain 'msku'")
    st.stop()

# Sheet 3: Combo SKUs
combo_url = sheet_csv_url(WMS_ID, "1566554648")
combo_df = pd.read_csv(combo_url, header=1)
st.subheader("✅ Combo SKUs Data (Sheet 3)")
st.dataframe(combo_df)

# Sheet 4: Sales SKUs
sales_url = sheet_csv_url(WMS_ID, "891383375")
sales_df = pd.read_csv(sales_url)
st.subheader("🛒 Sales SKUs (Sheet 4)")
st.dataframe(sales_df)
if "sku" not in sales_df.columns:
    st.error("Sheet 4 must contain column 'sku'")
    st.stop()

# --- Prepare Lookup Sets ---
msku_set = set(msku_df["msku"].dropna())
item_to_combo = {}
for _, row in combo_df.iterrows():
    combo = row["Combo"]
    for c in [col for col in combo_df.columns if col.startswith("SKU")]:
        sku = row[c]
        if pd.notna(sku):
            item_to_combo[sku] = combo

# --- Matching Logic ---
threshold = st.slider("Fuzzy match threshold", 70, 100, 85)
if st.button("🔎 Run SKU → MSKU Mapping", key="run_mapping_btn"):
    def map_one(sku):
        if pd.isna(sku):
            return None, None
        if sku in msku_set:
            return sku, None
        if sku in item_to_combo:
            return item_to_combo[sku], sku
        best, score = process.extractOne(sku, list(msku_set))
        return (best, None) if score >= threshold else (None, None)

    # Run mapping
    results = [map_one(s) for s in sales_df["sku"]]
    sales_df["mapped_msku"] = [m for m, _ in results]
    sales_df["via_combo"] = ["combo" if c else "" for _, c in results]

    # Show results
    unmapped = sales_df[sales_df["mapped_msku"].isna()]
    st.write(f"✅ Total rows: {len(sales_df)}, Unmapped SKUs: {len(unmapped)}")
    st.dataframe(sales_df)

    if not unmapped.empty:
        st.warning("⚠️ Unmapped SKUs:")
        st.write(unmapped["sku"].unique())

    # --- Save cleaned data ---
    sales_df_cleaned = sales_df[["sku", "mapped_msku", "via_combo"]].copy()
    sales_df_cleaned.to_csv("cleaned_sales.csv", index=False)

    # Products table from inventory
    products_df = msku_df[["msku"]].dropna().drop_duplicates()
    products_df.to_csv("products.csv", index=False)

    # Combos table
    combo_rows = []
    for _, row in combo_df.iterrows():
        combo_id = row["Combo"]
        for col in combo_df.columns:
            if col.startswith("SKU") and pd.notna(row[col]):
                combo_rows.append({
                    "combo_msku": combo_id,
                    "component_msku": row[col]
                })
    combos_flat = pd.DataFrame(combo_rows)
    combos_flat.to_csv("combos.csv", index=False)

    st.success("✅ All CSVs generated successfully!")
    st.code("cleaned_sales.csv\nproducts.csv\ncombos.csv")

    # Allow download as Excel
    buf = io.BytesIO()
    sales_df.to_excel(buf, index=False, engine="openpyxl")
    buf.seek(0)
    st.download_button(
        "📥 Download Cleaned File",
        buf,
        "cleaned_skus.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
