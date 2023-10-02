# This is the working code for sending bulk emails
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
                    
                    # reset attachment for the next email
                    attachment.seek(0)

        messages.success(request, "Your email was sent")
        return redirect('debtors')
    

    # EMAIL PALAVA
@login_required
# def single_recipient_send_mail(request):
#     if request.method == 'POST':
#         email = request.POST.get("email")
#         email_subject = request.POST.get("email_subject")
#         email_message = request.POST.get("email_message")
#         attachment = request.FILES.get('email_file')
#         content_type = attachment.content_type if attachment else None

#         # validate form data
#         if not email or not email_subject or not email_message:
#             return HttpResponseBadRequest('Missing required fields')

#         # create email message
#         email_msg = MIMEMultipart()
#         email_msg['Subject'] = email_subject
#         email_msg['To'] = email
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

#         # send email
#         email_sender = 'nsikanadaowo90@gmail.com'
#         email_password = 'jduzadsuapibwahj'
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
#             smtp.login(email_sender, email_password)
#             smtp.send_message(email_msg)

#         messages.success(request, "Email notification was successfully sent")
#         return redirect('debtors')



@login_required
def single_recipient_send_mail(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        email_subject = request.POST.get("email_subject")
        email_message = request.POST.get("email_message")
        attachment = request.FILES.get('email_file')
        content_type = attachment.content_type if attachment else None

        # Validate form data
        if not email or not email_subject or not email_message:
            return HttpResponseBadRequest('Missing required fields')

        # Create email message
        email_msg = MIMEMultipart()
        email_msg['Subject'] = email_subject
        email_msg['To'] = email
        email_msg.attach(MIMEText(email_message))

        # Add attachment, if provided
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

        # Send email
        email_sender = 'nsikanadaowo90@gmail.com'
        email_password = 'jduzadsuapibwahj'
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(email_msg)

        messages.success(request, "Email notification was successfully sent")
        return redirect('debtors')



@login_required
def multiple_recipients(request):
    selected_user_ids = request.POST.getlist('selected_users')

    debtors = Debtor.objects.all()

    emails = [debtor.email for debtor in debtors]
            
    return render(request, "admins_dashboard/email_notifications/multiple_recipient.html", {'emails': emails})
        
    # return render(request, "admins_dashboard/email_notifications/multiple_recipient.html")


@login_required
# def multiple_recipient_send_mail(request):
#     if request.method == 'POST':
#         email_subject = request.POST["email_subject"]
#         email_message = request.POST["email_message"]
#         attachment = request.FILES.get('email_file')
#         content_type = attachment.content_type if attachment else None

#         # validate form data
#         if not email_subject or not email_message:
#             return HttpResponseBadRequest('Missing required fields')

#         # create email message
#         email_sender = 'nsikanadaowo90@gmail.com'
#         email_password = 'jduzadsuapibwahj'
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#             smtp.login(email_sender, email_password)

#             # get all debtors
#             debtors = Debtor.objects.all()
#             for debtor in debtors:
#                 email = debtor.email
#                 if email:
#                     # create a new email_msg object for each debtor
#                     email_msg = MIMEMultipart()
#                     email_msg['Subject'] = email_subject
#                     email_msg['To'] = email
#                     email_msg.attach(MIMEText(email_message))

#                     # add attachment, if provided
#                     if attachment:
#                         file_data = attachment.read()
#                         if content_type.startswith('image/'):
#                             image = MIMEImage(file_data)
#                             image.add_header('Content-Disposition', 'attachment', filename='image.jpg')
#                             email_msg.attach(image)
#                         elif content_type == 'application/pdf':
#                             attachment_msg = MIMEApplication(file_data, _subtype='pdf')
#                             attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.pdf')
#                             email_msg.attach(attachment_msg)
#                         elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#                             attachment_msg = MIMEApplication(file_data, _subtype='docx')
#                             attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.docx')
#                             email_msg.attach(attachment_msg)
#                         else:
#                             return HttpResponseBadRequest('Unsupported file type')
                            
#                     # send email to current debtor
#                     smtp.send_message(email_msg)
                    
#                     # reset attachment for the next email
#                     attachment.seek(0)

#         messages.success(request, "Your email was sent")
#         return redirect('debtors')


@login_required
def multiple_recipient_send_mail(request):
    if request.method == 'POST':
        email_subject = request.POST["email_subject"]
        email_message = request.POST["email_message"]
        attachment = request.FILES.get('email_file')
        content_type = attachment.content_type if attachment else None

        # Validate form data
        if not email_subject or not email_message:
            return HttpResponseBadRequest('Missing required fields')

        # Create email message
        email_sender = 'nsikanadaowo90@gmail.com'
        email_password = 'jduzadsuapibwahj'
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)

            # Get all debtors
            debtors = Debtor.objects.all()

            for debtor in debtors:
                email = debtor.email

                if email:
                    # Create a new email_msg object for each debtor
                    email_msg = MIMEMultipart()
                    email_msg['Subject'] = email_subject
                    email_msg['To'] = email
                    email_msg.attach(MIMEText(email_message))

                    # Add attachment, if provided
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

                    # Send email to the current debtor
                    smtp.send_message(email_msg)

                    # Reset attachment for the next email if it exists
                    if attachment:
                        attachment.seek(0)

        messages.success(request, "Your email was sent")
        return redirect('debtors')