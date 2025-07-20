import streamlit as st
import asn1tools
import pandas as pd
import time

# Load the ASN.1 schema with all encoding rules
schemata = {
    "BER": asn1tools.compile_files('cdr.asn1', 'ber'),
    "DER": asn1tools.compile_files('cdr.asn1', 'der'),
    "PER Aligned": asn1tools.compile_files('cdr.asn1', 'per'),
    "PER Unaligned": asn1tools.compile_files('cdr.asn1', 'uper'),
}

# Sample data to encode (must match ASN.1 schema field names)
sample_record = {
    "callId": 12345,
    "caller": "9123456789",
    "callee": "9876543210",  # ✅ corrected field name
    "duration": 360,
    "timestamp": "202507201400Z"  # ✅ valid IA5String format
}

# Encode and decode using each method
results = []

for name, schema in schemata.items():
    start = time.time()
    encoded = schema.encode('CallRecord', sample_record)
    memory = len(encoded)
    decoded = schema.decode('CallRecord', encoded)
    duration = (time.time() - start) * 1000  # in milliseconds

    results.append({
        "Encoding": name,
        "Binary Length (bytes)": memory,
        "Bits Used": memory * 8,
        "Time Taken (ms)": f"{duration:.3f}",
        "Decoded Call ID": decoded["callId"],
        "Decoded Duration": decoded["duration"]
    })

# Streamlit UI
st.title("📞 ASN.1 CDR Encoding Comparison")

st.subheader("📋 Sample Call Detail Record")
st.json(sample_record)

st.subheader("📊 Encoding Results")
df = pd.DataFrame(results)
st.dataframe(df, use_container_width=True)

st.markdown("🔍 This comparison shows differences in size and performance for each ASN.1 encoding rule.")
