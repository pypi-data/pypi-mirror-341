# Django MJML Email

Django MJML Email is a package that allows Django developers to write email 
templates using the MJML language. This tool simplifies the creation of
responsive and well-structured emails.

## What is MJML?
From the [documentation](https://documentation.mjml.io/) of the project:
> MJML is a markup language designed to reduce the pain of coding a responsive 
> email. Its semantic syntax makes it easy and straightforward and its rich 
> standard components library speeds up your development time and lightens your 
> email codebase. MJML’s open-source engine generates high quality responsive 
> HTML compliant with best practices.

## Then what?

While the original compiler is written in Javascript and runs on Node.js, this
package leverages [mrml](https://github.com/jdrouet/mrml), a rust implementation
of `mjml` through [mjml-python](https://github.com/mgd020/mjml-python).

The rust port is almost complete, it lacks a single feature:
https://github.com/jdrouet/mrml?tab=readme-ov-file#missing-implementations

## Requirements

- Python >= 3.12
- Django >= 4.2
- mjml-python == 1.3.5

## Installation

To install the package, run the following command:

```bash
pip install django-mjml-email
```

## Configuration

To start using `django-mjml-email`, you must configure a mail backend in your 
settings. If you're using SMTP to send your emails:

```python
EMAIL_BACKEND = "django_mjml_email.backend.SMTPMJMLEmailBackend"
```

If you're using any other email backend, you should define your custom backend 
and then refer to it in `settings.py`.

```python
# yourproject/my_email_backend.py
from django.core.mail.backends.console import EmailBackend

from django_mjml_email.mjml_email import MJMLEmailMixin


class MyEmailBackend(MJMLEmailMixin, EmailBackend):
    pass

```
```python
# settings.py
# ...
EMAIL_BACKEND = "my_email_backend.MyEmailBackend"

```

**Only Django builtin backends are tested**, so if you're using AnyMail or any
other email backend, please report any problem in the issues.



## Usage

You can create email templates using MJML. For example, create a file named `email_template.mjml`:

```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text>
          Welcome to our application!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

In your Django code, you don't need anything special to send it:

```python
from django.core.mail import send_mail
from django.template.loader import get_template

template = get_template("email_template.mjml")
send_mail(
    "It works!",
    template.render(),
    "MJML Sender <from@example.com>",
    ["to@example.com"],
)

```

## Contributions

Contributions, bug reports, and suggestions are welcome! Feel free to open an 
issue or submit a pull request.

## License

This project is distributed under the BSD 3-Clause Clear License. See the 
`LICENSE` file for more details.
