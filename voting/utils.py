import StringIO
import qrcode
import qrcode.image.svg

def get_ticket(user):
    qrcode_output = StringIO.StringIO()
    qrcode.make(user.pk, image_factory=qrcode.image.svg.SvgImage, version=3).save(qrcode_output)
    qrcode_value = str(user.pk).join(qrcode_output.getvalue().split('\n')[1:])
    return qrcode_value