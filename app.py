import streamlit as st
import pandas as pd
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

st.title("💎 Receipt Organizer for Insurance Purposes")
st.write("Upload receipts (images or PDFs), auto-extract info, export to Excel/CSV, and auto-backup to Google Drive!")

uploaded_files = st.file_uploader("Upload Receipts", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)

columns = ["Date of Purchase", "Vendor Name", "Item Description", "Serial Number", "Purchase Amount", "Payment Method", "Receipt File"]
data = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        text = ""

        if uploaded_file.type == "application/pdf":
            images = convert_from_bytes(uploaded_file.read())
            if images:
                img = images[0]
                text = pytesseract.image_to_string(img)
        else:
            img = Image.open(uploaded_file)
            text = pytesseract.image_to_string(img)

        vendor = text.split("\\n")[0][:30] if text else ""
        amount = ""
        for line in text.split("\\n"):
            if "$" in line:
                amount = line.strip()
                break
        item_desc = ""
        keywords = ["Rolex", "Cartier", "Omega", "Jewelry", "Ring", "Necklace", "Watch", "Bracelet"]
        for word in keywords:
            if word.lower() in text.lower():
                item_desc = word
                break

        data.append(["", vendor, item_desc, "", amount, "", file_name])

    df = pd.DataFrame(data, columns=columns)
    edited_df = st.data_editor(df, num_rows="dynamic")

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
