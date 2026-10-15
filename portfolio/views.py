
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages


def home(request):
    return render(request, 'portfolio/home.html')


def about(request):
    return render(request, 'portfolio/about.html')


def skills(request):
    return render(request, 'portfolio/skills.html')


def projects(request):
    return render(request, 'portfolio/projects.html')


def contact(request):
    form_data = {
        'name': '',
        'email': '',
        'subject': '',
        'message': '',
    }

    # Process the form only when it is submitted.
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'subject': request.POST.get('subject', '').strip(),
            'message': request.POST.get('message', '').strip(),
        }

        errors = []

        # Validate required fields.
        if not form_data['name']:
            errors.append('Please enter your name.')

        if not form_data['email']:
            errors.append('Please enter your email address.')
        else:
            try:
                validate_email(form_data['email'])
            except ValidationError:
                errors.append('Please enter a valid email address.')

        if not form_data['subject']:
            errors.append('Please enter a subject.')

        if not form_data['message']:
            errors.append('Please enter a message.')

        # Validate maximum field lengths.
        if len(form_data['name']) > 100:
            errors.append('Your name must be 100 characters or fewer.')

        if len(form_data['email']) > 254:
            errors.append('Your email address is too long.')

        if len(form_data['subject']) > 150:
            errors.append('The subject must be 150 characters or fewer.')

        if len(form_data['message']) > 5000:
            errors.append('Your message must be 5000 characters or fewer.')

        # Display validation errors and retain entered values.
        if errors:
            for error in errors:
                messages.error(request, error)

            return render(
                request,
                'portfolio/contact.html',
                {
                    'form_data': form_data,
                    'form_errors': True,
                },
            )

        # Create and send the email.
        try:
            email_message = EmailMessage(
                subject=f"Portfolio enquiry: {form_data['subject']}",
                body=(
                    "New message from your portfolio.\n\n"
                    f"Name: {form_data['name']}\n"
                    f"Email: {form_data['email']}\n"
                    f"Subject: {form_data['subject']}\n\n"
                    f"Message:\n{form_data['message']}"
                ),
                to=['ishatvag4@gmail.com'],
                reply_to=[form_data['email']],
            )

            email_message.send(fail_silently=False)

            messages.success(
                request,
                'Your message has been sent successfully. '
                'Thank you for reaching out!'
            )

            return redirect('contact')

        except Exception as error:
            # Log the actual error in the Django development terminal.
            print('EMAIL ERROR:', repr(error))

            messages.error(
                request,
                'We could not send your message right now. '
                'Please try again later or email us directly.'
            )

            return render(
                request,
                'portfolio/contact.html',
                {
                    'form_data': form_data,
                    'form_errors': False,
                },
            )

    # Display the contact page for a normal GET request.
    return render(
        request,
        'portfolio/contact.html',
        {
            'form_data': form_data,
        },
    )
