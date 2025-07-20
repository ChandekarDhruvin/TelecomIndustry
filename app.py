import streamlit as st
import asn1tools
import json
import time
import os
import binascii
from io import BytesIO

# Load ASN.1 schema
with open("cdr.asn1") as f:
    asn_schema = f.read()

schemata = {
    'BER': asn1tools.compile_string(asn_schema, 'ber'),
    'DER': asn1tools.compile_string(asn_schema, 'der'),
    'PER': asn1tools.compile_string(asn_schema, 'per')
}

# Create folder for encoded files
os.makedirs("encoded_samples", exist_ok=True)

st.title("📡 Telecom CDR Binary Parser Demo")

# Load sample records
with open("sample_record.json") as f:
    records = json.load(f)

selected_encoding = st.selectbox("Select Encoding Format", list(schemata.keys()))

st.subheader("📋 Sample Call Records")
st.json(records)

results = []

for idx, record in enumerate(records):
    codec = schemata[selected_encoding]
    start_encode = time.time()
    encoded = codec.encode('CallRecord', record)
    encode_time = (time.time() - start_encode) * 1000

    # Save file
    filename = f"encoded_samples/record_{idx+1}_{selected_encoding}.bin"
    with open(filename, "wb") as f:
        f.write(encoded)

    # Decode again
    start_decode = time.time()
    decoded = codec.decode('CallRecord', encoded)
    decode_time = (time.time() - start_decode) * 1000

    # Store results
    results.append({
        "Record #": idx + 1,
        "Encoding": selected_encoding,
        "Binary Size (Bytes)": len(encoded),
        "Bits": len(encoded) * 8,
        "Encode Time (ms)": round(encode_time, 2),
        "Decode Time (ms)": round(decode_time, 2),
        "Decoded Call ID": decoded['callId'],
        "Decoded Duration": decoded['duration'],
        "Hex Preview": binascii.hexlify(encoded).decode()[:32] + "..."
    })

# Show Results
st.subheader("📊 Encoding & Decoding Summary")
st.dataframe(results)

# File Upload and Decode
st.subheader("📤 Decode Your Own Encoded File")
uploaded_file = st.file_uploader("Upload Encoded CDR (.bin)", type=["bin"])
user_encoding = st.selectbox("Select Encoding of Uploaded File", list(schemata.keys()), key="upload_enc")

if uploaded_file:
    data = uploaded_file.read()
    decoded = schemata[user_encoding].decode('CallRecord', data)
    st.success("Successfully decoded record:")
    st.json(decoded)

# Download Encoded Files
st.subheader("📥 Download Binary Files")
for idx, record in enumerate(records):
    with open(f"encoded_samples/record_{idx+1}_{selected_encoding}.bin", "rb") as f:
        st.download_button(
            label=f"Download Record {idx+1} - {selected_encoding}",
            data=f.read(),
            file_name=f"cdr_record_{idx+1}_{selected_encoding}.bin"
        )
