import streamlit as st
import pandas as pd
import io

# --- App title ---
st.title("💎 Receipt Organizer for Insurance Purposes")
st.write("Upload your receipts (images or PDFs), organize manually, export to Excel/CSV!")

# --- Upload files ---
uploaded_files = st.file_uploader("Upload Receipts", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)

# --- Initialize empty DataFrame ---
columns = ["Date of Purchase", "Vendor Name", "Item Description", "Serial Number", "Purchase Amount", "Payment Method", "Receipt File"]
data = []

# --- Process uploaded files ---
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        data.append(["", "", "", "", "", "", file_name])

    # --- Display editable table ---
    df = pd.DataFrame(data, columns=columns)
    edited_df = st.data_editor(df, num_rows="dynamic")

    # --- Export buttons ---
    st.write("\\n")
    col1, col2 = st.columns(2)
    with col1:
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
            edited_df.to_excel(writer, index=False, sheet_name='Receipts')
        towrite.seek(0)
        st.download_button(label="📄 Download Excel", data=towrite, file_name="organized_receipts.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with col2:
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📄 Download CSV", data=csv, file_name='organized_receipts.csv', mime='text/csv')

else:
    st.info("⬆️ Upload receipts to get started!")
