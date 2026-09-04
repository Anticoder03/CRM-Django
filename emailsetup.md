# Email Setup Guide

This guide explains how to configure email sending in **CRM Pro** so that the **Send Email**, **Bulk Email Marketing**, and **Email Log** features actually deliver messages to real inboxes.

---

## 1. Overview

Emails are sent through Django's email framework. There are two ways to run email in this project:

| Mode | Backend | When to use |
|------|---------|-------------|
| Development | `console` | Testing locally — prints emails to the terminal |
| Production | `smtp` | Actually send emails to real inboxes |

By default the project is in **development (console)** mode.

---

## 2. Where the settings live

All email configuration lives in the file:

```
CRM/crm/settings.py
```

Look for the **Email** section (near the bottom):

```python
# Email - Console backend logs emails to terminal (development)
# For production, switch to SMTP backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "CRM Pro <noreply@crmpro.com>"
```

---

## 3. Switch from console to real email (SMTP)

To send real emails you must:

1. Change the `EMAIL_BACKEND` to the SMTP backend.
2. Put your **email address** in `EMAIL_HOST_USER`.
3. Put your **email password / app password** in `EMAIL_HOST_PASSWORD`.

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"
DEFAULT_FROM_EMAIL = "Your Name <your-email@gmail.com>"
```

> Replace `your-email@gmail.com` and `your-app-password` with your real values.

After editing `settings.py`, **restart the server** for the changes to take effect.

---

## 4. Setting up a Gmail address (recommended)

### Step 1 — Turn on 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** on the left.
3. Under **Signing in to Google**, click **2-Step Verification**.
4. Follow the steps to turn it **ON**.
   > Google requires 2-Step Verification before you can create an app password.

### Step 2 — Create an App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in if prompted.
3. Give the app a name, e.g. **CRM Pro**.
4. Click **Create**.
5. Google shows a **16-character app password** (looks like: `abcd efgh ijkl mnop`).
6. **Copy** this password — you'll paste it into `EMAIL_HOST_PASSWORD`.

> ⚠️ An **App Password** is NOT your normal Gmail password. Use the 16-character app password generated here. Remove the spaces when pasting.

### Step 3 — Put the values in settings.py

```python
EMAIL_HOST_USER = "your-email@gmail.com"        # your Gmail address
EMAIL_HOST_PASSWORD = "abcdefghijklmnop"        # the 16-char app password (no spaces)
```

---

## 5. Using Outlook / Microsoft 365

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.office365.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "you@outlook.com"
EMAIL_HOST_PASSWORD = "your-password"
DEFAULT_FROM_EMAIL = "you@outlook.com"
```

---

## 6. Using any other provider (generic SMTP)

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yourprovider.com"
EMAIL_PORT = 587            # or 465 for SSL
EMAIL_USE_TLS = True        # use False + EMAIL_USE_SSL=True for port 465
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "your-email@provider.com"
EMAIL_HOST_PASSWORD = "your-password"
```

---

## 7. Important notes

- **App Passwords work only for Gmail.** Providers differ, so check theirs.
- **Store the password securely.** For real deployments, use environment variables instead of hardcoding:
  ```python
  import os
  EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
  EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
  ```
- **Never commit your real email password to git.** The blank `""` defaults are safe.
- **Console mode** is helpful for testing: emails appear in the terminal where you ran `python manage.py runserver`, so you can verify everything works before switching to SMTP.

---

## 8. Testing if it works

After configuring, run the server and test from the CRM UI:

1. Log in to CRM Pro.
2. Go to **Email Marketing → Send Email**.
3. Choose any customer, enter a subject + message, and click **Send Email**.
4. Go to **Email Marketing → Email Log**. A new "Sent" entry should appear.

For a quick command-line test without the UI, you can also run:

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    "Test Subject",
    "This is a test message.",
    None,
    ["recipient@example.com"],
    fail_silently=False,
)
```

- In **SMTP mode**: the recipient should receive the email in a few seconds.
- In **console mode**: the message is printed to the terminal.

---

## 9. Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| `SMTPAuthenticationError` | Wrong email/password, or using your normal Gmail password instead of an app password | Recreate the app password and use it |
| `ConnectionRefusedError` | Wrong host / port | Confirm the provider's SMTP host and port |
| Emails not sent to real inboxes | `EMAIL_BACKEND` still set to `console` | Switch to `django.core.mail.backends.smtp.EmailBackend` |
| Gmail blocks "less secure apps" | 2-Step Verification is off | Turn on 2-Step Verification and use an app password |
| Emails land in spam | Sender reputation / SPF-DKIM not set | Configure SPF/DKIM records for your domain |
| Port 25 blocked | Some hosts block SMTP port 25 | Use port 587 (TLS) or 465 (SSL) |
| `Login attempt blocked` | Suspicious activity detected by provider | Visit the provider's security page to allow the attempt |

---

## 10. Quick reference — Gmail settings

You only need to fill in **two values** to make email work:

```python
EMAIL_HOST_USER = "your-email@gmail.com"     # ← YOUR GMAIL ADDRESS
EMAIL_HOST_PASSWORD = "your-app-password"    # ← 16-CHAR APP PASSWORD (NO SPACES)
```

Everything else (backend, host, port, TLS) is already configured correctly for Gmail.
