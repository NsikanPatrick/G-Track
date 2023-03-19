# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.application import MIMEApplication
# import ssl
# import smtplib

# email_sender = 'nsikanadaowo90@gmail.com'
# email_password = 'jduzadsuapibwahj'
# # The list of recipients below can accept as many or less emails as possible
# # This implies that you can add only one email there incase you want to send
# # to one recipient or 100 incase of 100 recipients.
# recipients = ["adaowonsikan6952@gmail.com", "nsikanpatrick69@gmail.com", "adaowonsikan69@gmail.com"]
# subject = 'Example2 email with multiple attachments'
# body = """\
# Dear recipient,

# This email contains multiple attachments, including an image, a PDF, and a Word document.

# Best regards,
# Your Name"""

# em = MIMEMultipart()
# em['From'] = email_sender
# em['To'] = ", ".join(recipients)
# em['Subject'] = subject

# # attach the body of the email
# em.attach(MIMEText(body, 'plain'))

# # attach the image
# with open('Me2.jpg', 'rb') as img_file:
#     img_data = img_file.read()
#     img = MIMEImage(img_data, name='image.jpg')
#     em.attach(img)

# # attach the PDF file
# with open('NSIKAN ADAOWO - SOFTWARE ENGINEER.pdf', 'rb') as pdf_file:
#     pdf_data = pdf_file.read()
#     pdf = MIMEApplication(pdf_data, _subtype='pdf')
#     pdf.add_header('Content-Disposition', 'attachment', filename='document.pdf')
#     em.attach(pdf)

# # attach the Word document
# with open('Third term exams - 2022.docx', 'rb') as docx_file:
#     docx_data = docx_file.read()
#     docx = MIMEApplication(docx_data, _subtype='docx')
#     docx.add_header('Content-Disposition', 'attachment', filename='document.docx')
#     em.attach(docx)

# # send the email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(email_sender, email_password)
#     smtp.sendmail(email_sender, recipients, em.as_string())

# Here's the working code
def multiple_recipient_send_mail(request):
    if request.method == 'POST':
        email_subject = request.POST["email_subject"]
        email_message = request.POST["email_message"]
        attachment = request.FILES.get('email_file')
        content_type = attachment.content_type if attachment else None

        # validate form data
        if not email_subject or not email_message:
            return HttpResponseBadRequest('Missing required fields')

        # create email message
        email_sender = 'nsikanadaowo90@gmail.com'
        email_password = 'jduzadsuapibwahj'
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)

            # get all debtors
            debtors = Debtor.objects.all()
            for debtor in debtors:
                email = debtor.email
                if email:
                    # create a new email_msg object for each debtor
                    email_msg = MIMEMultipart()
                    email_msg['Subject'] = email_subject
                    email_msg['To'] = email
                    email_msg.attach(MIMEText(email_message))

                    # add attachment, if provided
                    if attachment:
                        file_data = attachment.read()
                        if content_type.startswith('image/'):
                            image = MIMEImage(file_data)
                            image.add_header('Content-Disposition', 'attachment', filename='image.jpg')
                            email_msg.attach(image)
                        elif content_type == 'application/pdf':
                            attachment_msg = MIMEApplication(file_data, _subtype='pdf')
                            attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.pdf')
                            email_msg.attach(attachment_msg)
                        elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                            attachment_msg = MIMEApplication(file_data, _subtype='docx')
                            attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.docx')
                            email_msg.attach(attachment_msg)
                        else:
                            return HttpResponseBadRequest('Unsupported file type')

                    # send email to current debtor
                    smtp.send_message(email_msg)

        messages.success(request, "Your email was sent")
        return redirect('debtors')
# End of working code

from gtrack_app.models import Debtor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import ssl
import smtplib

email_sender = 'nsikanadaowo90@gmail.com'
email_password = 'jduzadsuapibwahj'

# create email message
email_msg = MIMEMultipart()
email_msg['From'] = email_sender
email_msg['Subject'] = 'Example email with multiple attachments'
body = """\
Dear debtor,

This email contains multiple attachments, including an image, a PDF, and a Word document.

Best regards,
Your Name"""
email_msg.attach(MIMEText(body, 'plain'))

# attach the image
with open('Me2.jpg', 'rb') as img_file:
    img_data = img_file.read()
    img = MIMEImage(img_data, name='image.jpg')
    email_msg.attach(img)

# attach the PDF file
with open('NSIKAN ADAOWO - SOFTWARE ENGINEER.pdf', 'rb') as pdf_file:
    pdf_data = pdf_file.read()
    pdf = MIMEApplication(pdf_data, _subtype='pdf')
    pdf.add_header('Content-Disposition', 'attachment', filename='document.pdf')
    email_msg.attach(pdf)

# attach the Word document
with open('Third term exams - 2022.docx', 'rb') as docx_file:
    docx_data = docx_file.read()
    docx = MIMEApplication(docx_data, _subtype='docx')
    docx.add_header('Content-Disposition', 'attachment', filename='document.docx')
    email_msg.attach(docx)

# send email to all debtors
debtors = Debtor.objects.all()
for debtor in debtors:
    if debtor.email:
        email_msg['To'] = debtor.email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, debtor.email, email_msg.as_string())

print('Emails sent successfully!')


