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

# from flask import Flask, request, render_template
# import ssl
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.application import MIMEApplication

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def send_email():
#     if request.method == 'POST':
#         # get the form data
#         # Get the recipient email addresses from the form
#         recipient_string = request.form['recipients']

#         # Split the string into a list of email addresses
#         recipients = recipient_string.split(',')

#         # Trim any leading or trailing whitespace from each email address
#         recipients = [r.strip() for r in recipients]
        
#         subject = request.form['subject']
#         body = request.form['body']
        
#         # create the email message
#         em = MIMEMultipart()
#         em['From'] = 'your-email-address@example.com'
#         em['To'] = recipients
#         em['Subject'] = subject
#         em.attach(MIMEText(body, 'plain'))

#         # attach the files
#         for file in request.files.getlist('file'):
#             file_data = file.read()
#             attachment = MIMEApplication(file_data, _subtype=file.content_type.split('/')[-1])
#             attachment.add_header('Content-Disposition', 'attachment', filename=file.filename)
#             em.attach(attachment)

#         # send the email
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#             smtp.login('your-email-address@example.com', 'your-email-password')
#             smtp.sendmail('your-email-address@example.com', recipients.split(','), em.as_string())

#         return 'Email sent!'
#     else:
#         return render_template('form.html')



# # SENDING THE EMAIL TO MULTIPLE EMAIL CONTACTS
# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
# from email.mime.image import MIMEImage
# from django.core.mail import EmailMessage
# from django.shortcuts import redirect
# from django.contrib import messages
# from django.http import HttpResponseBadRequest

# def send_email(request):
#     if request.method == 'POST':
#         email_subject = request.POST["email_subject"]
#         email_message = request.POST["email_message"]
#         attachment = request.FILES.get('email_file')
#         content_type = attachment.content_type if attachment else None

#         # validate form data
#         if not email_subject or not email_message:
#             return HttpResponseBadRequest('Missing required fields')

#         # retrieve list of email addresses
#         email_list = request.POST.getlist('email_list')

#         # create email message
#         email_msg = MIMEMultipart()
#         email_msg['Subject'] = email_subject
#         email_msg.attach(MIMEText(email_message))

#         # add attachment, if provided
#         if attachment:
#             file_data = attachment.read()
#             if content_type.startswith('image/'):
#                 image = MIMEImage(file_data)
#                 image.add_header('Content-Disposition', 'attachment', filename='image.jpg')
#                 email_msg.attach(image)
#             elif content_type == 'application/pdf':
#                 attachment_msg = MIMEApplication(file_data, _subtype='pdf')
#                 attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.pdf')
#                 email_msg.attach(attachment_msg)
#             elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#                 attachment_msg = MIMEApplication(file_data, _subtype='docx')
#                 attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.docx')
#                 email_msg.attach(attachment_msg)
#             else:
#                 return HttpResponseBadRequest('Unsupported file type')

#         # send email to each recipient in the list
#         email_sender = 'nsikanadaowo90@gmail.com'
#         email_password = 'jduzadsuapibwahj'
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
#             smtp.login(email_sender, email_password)
#             for recipient in email_list:
#                 email_msg['To'] = recipient
#                 smtp.send_message(email_msg)

#         messages.success(request, "Your email was sent")
#         return redirect('debtors')



# This part is to schedule the email to send at a specified time
# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime

# # create a new scheduler instance
# scheduler = BackgroundScheduler()

# def send_email():
#     # your email sending code here

# # schedule the email to be sent at 8:00 am on March 15th, 2023
# scheduled_time = datetime(2023, 3, 15, 8, 0, 0)
# scheduler.add_job(send_email, 'date', run_date=scheduled_time)

# # start the scheduler
# scheduler.start()


