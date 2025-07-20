import asn1tools

cdr_record = {
    'callId': 1001,
    'caller': '9876543210',
    'callee': '1234567890',
    'duration': 300,
    'timestamp': '2025-07-20T14:55:00'
}

encodings = {
    'ber': 'cdr_ber.bin',
    'der': 'cdr_der.bin',
    'per': 'cdr_per_aligned.bin',
    'uper': 'cdr_per_unaligned.bin'
}

for enc, filename in encodings.items():
    compiled = asn1tools.compile_files('cdr.asn1', enc)
    encoded = compiled.encode('CallRecord', cdr_record)
    with open(filename, 'wb') as f:
        f.write(encoded)
    print(f"✅ {filename} generated.")
