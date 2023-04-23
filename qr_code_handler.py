from io import BytesIO

import qrcode


def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=25,
        border=1
    )
    qr.add_data(data)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return buf
