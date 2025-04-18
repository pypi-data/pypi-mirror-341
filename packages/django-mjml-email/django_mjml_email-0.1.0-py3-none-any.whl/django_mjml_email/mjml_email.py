import logging
from email.mime.image import MIMEImage
from pathlib import Path

from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from mjml import mjml2html

MIME_TYPES = {
    "text/html",
}
logger = logging.getLogger("django_mjml_email")


def is_mrml_source(body: str) -> bool:
    return body.strip().startswith("<mjml>")


def get_email_message(source_message: EmailMessage) -> EmailMessage:
    """

    Get the email message and convert the message body to HTML format if the content subtype is
     'html' and the body contains <mrml> tags. Then, create a new EmailMessage object with the
     converted body and other attributes copied from the source message. If the source message
     has alternatives, check and convert them to HTML format if they are of specific MIME types
     and contain <mrml> tags. Finally, return the updated EmailMessage object.

    Parameters:
        source_message (EmailMessage): The input source email message to process and convert.

    Returns:
        EmailMessage: The modified email message object with updated content if necessary.

    """
    if is_mrml_source(source_message.body):
        logger.info("Converting message body in html...")
        body = mjml2html(source_message.body)
        content_subtype = "html"
    else:
        body = source_message.body
        content_subtype = source_message.content_subtype
    message = source_message.__class__(
        subject=source_message.subject,
        body=body,
        from_email=source_message.from_email,
        to=source_message.to,
        bcc=source_message.bcc,
        connection=source_message.connection,
        attachments=source_message.attachments,
        headers=source_message.extra_headers,
        cc=source_message.cc,
        reply_to=source_message.reply_to,
    )
    message.content_subtype = content_subtype
    if hasattr(source_message, "alternatives"):
        # This message could have some <mrml> in an attached alternative
        for source_content, mimetype in source_message.alternatives:
            if mimetype in MIME_TYPES and is_mrml_source(source_content):
                logger.info("Converting message alt content in html...")
                content = mjml2html(source_content)
            else:
                content = source_content
            message.attach_alternative(content, mimetype)
    return message


def attach_inline_image(message: EmailMessage, file_path: str):
    actual_file_path = Path(finders.find(file_path))
    with actual_file_path.open("rb") as handler:
        attachment = MIMEImage(handler.read())
        filename = actual_file_path.name
        attachment.add_header("Content-ID", f"<{filename}>")
        attachment.add_header("Content-Disposition", "inline", filename=filename)
        message.attach(attachment)

    return message


class MJMLEmailMixin:
    """Use this mixin to define a new EmailBackend class that inherits from one of the Django email backends:

    >>> from django.core.mail.backends.smtp import EmailBackend
    >>> class MyEmailBackend(MJMLEmailMixin, EmailBackend):
    >>>     pass

    Use the new email backend in your Django settings file:
    >>> EMAIL_BACKEND = "path.to.your.MyEmailBackend"
    """

    def send_messages(self, email_messages: list[EmailMessage]) -> None:
        """Scans the `EmailMessage` instances and recreate the content where
        it detects there's a <mjml> source.
        """
        return super().send_messages([get_email_message(message) for message in email_messages])
