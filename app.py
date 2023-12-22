import streamlit as st
from PIL import Image
import tempfile
import urllib.parse
import os
from pypdf import PdfReader, PdfWriter

st.title(":page_facing_up: PDF MetaData Editor")

st.write("PDFのメタデータの中にあるタイトル/作者を修正します。")

pdf_file = st.file_uploader("PDFファイル", type=['pdf'], accept_multiple_files=False)
if pdf_file is not None:
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    writer.clone_reader_document_root(reader)
    d = reader.metadata
    d = {k: d[k] for k in d.keys()}
    print(d)
    title = st.text_input("タイトル", d.get('/Title', ''))
    author = st.text_input("作者", d.get('/Author', ''))
    if st.button("PDFを修正"):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            d['/Title'] = title
            d['/Author'] = author
            writer.add_metadata(d)
            with open(tmp.name, "wb") as f:
                writer.write(f)
                writer.close()
            st.download_button(
                label="ダウンロード",
                data=open(tmp.name,'br'),
                file_name=urllib.parse.quote(os.path.basename(pdf_file.name)),
                mime="application/pdf"
            )

