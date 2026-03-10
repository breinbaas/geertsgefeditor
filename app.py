import streamlit as st
import zipfile
import io

st.set_page_config(page_title="Geerts GEF Editor", page_icon="📝")

st.title("Geerts GEF Editor")
st.write(
    "Upload een of meerdere `.gef` files. De app bewerkt ze en maakt een zip bestand met de aangepaste bestanden."
)

with st.form("upload_form", clear_on_submit=False):
    uploaded_files = st.file_uploader(
        "Kies .gef files", type=["gef"], accept_multiple_files=True
    )
    submitted = st.form_submit_button("Upload files")

if submitted and uploaded_files:
    st.success(f"Je hebt {len(uploaded_files)} bestanden geüpload.")

    # Create a BytesIO object to store the zip file in memory
    zip_buffer = io.BytesIO()

    # Create the zip file
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            # Read the content of the uploaded file as text
            file_content = uploaded_file.getvalue().decode("utf-8")

            for line in file_content.split("\n"):
                print(line)
                break

            # TODO: Add text editing logic here (e.g., file_content = file_content.replace('old', 'new'))

            # Write the file to the zip
            zip_file.writestr(uploaded_file.name, file_content)

    # Reset the buffer's file pointer to the beginning
    zip_buffer.seek(0)

    st.download_button(
        label="Download Zipped GEF Files",
        data=zip_buffer,
        file_name="gef_files.zip",
        mime="application/zip",
        type="primary",
    )
