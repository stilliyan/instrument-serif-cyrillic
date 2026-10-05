"""Set the public release metadata without changing font geometry or layout."""

def finalize_release(font, style):
    font['head'].fontRevision = 1.0
    for record in font['name'].names:
        if record.nameID in (3, 5):
            value = f'Lirena {style} 1.000' if record.nameID == 3 else 'Version 1.000'
            record.string = value.encode(record.getEncoding())
