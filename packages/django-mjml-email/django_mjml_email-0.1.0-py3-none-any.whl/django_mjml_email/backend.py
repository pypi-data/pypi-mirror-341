from django.core.mail.backends.smtp import EmailBackend

from django_mjml_email.mjml_email import MJMLEmailMixin


class SMTPMJMLEmailBackend(MJMLEmailMixin, EmailBackend):
    """
    You can set this email backend in Django settings file if you're using the built-in SMTP backend.

    EMAIL_BACKEND = "mjml_email.backend.SMTPMJMLEmailBackend"
    """

    pass
