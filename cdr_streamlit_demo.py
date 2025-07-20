import streamlit as st
import asn1tools
import pandas as pd
import time

# Compile ASN.1 schema with different encodings
schemata = {
    "BER": asn1tools.compile_files('cdr.asn1', 'ber'),
    "DER": asn1tools.compile_files('cdr.asn1', 'der'),
    "PER Aligned": asn1tools.compile_files('cdr.asn1', 'per'),
    "PER Unaligned": asn1tools.compile_files('cdr.asn1', 'uper'),
}

# Sample CDR data
sample_record = {
    "callId": 12345,
    "caller": "9123456789",
    "callee": "9876543210",
    "duration": 360,
    "timestamp": "202507201400"
}

# Lists for results
encode_results, decode_results = [], []

# Process each encoding type
for name, schema in schemata.items():
    start_time = time.time()
    encoded = schema.encode('CallRecord', sample_record)
    encode_duration = (time.time() - start_time) * 1000  # in ms
    memory_bytes = len(encoded)

    # Decode
    start_time = time.time()
    decoded = schema.decode('CallRecord', encoded)
    decode_duration = (time.time() - start_time) * 1000  # in ms

    # Encoding analysis
    encode_results.append({
        "Encoding": name,
        "Encoded Size (Bytes)": memory_bytes,
        "Bits Used": memory_bytes * 8,
        "Time to Encode (ms)": f"{encode_duration:.3f}"
    })

    # Decoding analysis
    decode_results.append({
        "Encoding": name,
        "Decoded Call ID": decoded["callId"],
        "Decoded Caller": decoded["caller"],
        "Decoded Callee": decoded["callee"],
        "Decoded Duration": decoded["duration"],
        "Decoded Timestamp": decoded["timestamp"],
        "Time to Decode (ms)": f"{decode_duration:.3f}"
    })

# Streamlit UI
st.title("📡 ASN.1 CDR Encoding & Decoding Analysis")

st.subheader("📥 Sample CDR Record")
st.json(sample_record)

st.subheader("📊 Encoding Results")
st.dataframe(pd.DataFrame(encode_results), use_container_width=True)

st.subheader("📤 Decoding Results")
st.dataframe(pd.DataFrame(decode_results), use_container_width=True)

st.markdown("✅ This tool benchmarks ASN.1 encoding formats for telecom CDR data in terms of size and speed.")
