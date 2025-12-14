#!/usr/bin/env python3
"""
Email Sender
Sends the weekly digest presentation via email
"""

import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
from datetime import datetime

class EmailSender:
    def __init__(self, config_path: str = "../config.yaml"):
        self.base_dir = Path(__file__).parent.parent
        config_file = self.base_dir / "config.yaml"

        with open(config_file) as f:
            self.config = yaml.safe_load(f)

        self.email_config = self.config.get('email', {})

    def send_presentation(self, filepath: str) -> bool:
        """Send the presentation via email"""
        if not self.email_config.get('enabled', False):
            print("  ℹ️  Email delivery is disabled in config.yaml")
            return False

        print("\n📧 Sending email...")

        # Email configuration
        sender_email = self.email_config.get('sender_email')
        sender_password = self.email_config.get('sender_password')
        recipient = self.email_config.get('recipient')
        smtp_server = self.email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = self.email_config.get('smtp_port', 587)

        # Validate configuration
        if sender_email == "your-email@example.com" or not sender_email:
            print("  ⚠️  Please configure sender_email in config.yaml")
            return False

        if sender_password == "your-app-password" or not sender_password:
            print("  ⚠️  Please configure sender_password in config.yaml")
            print("  💡 For Gmail, use an App Password: https://myaccount.google.com/apppasswords")
            return False

        # Create message
        msg = MIMEMultipart()
        date_str = datetime.now().strftime('%Y-%m-%d')
        subject = self.email_config.get('subject_template', 'AI Weekly Digest - {date}')
        msg['Subject'] = subject.replace('{date}', date_str)
        msg['From'] = sender_email
        msg['To'] = recipient

        # Email body
        body = f"""
Your Weekly Agentic AI Digest is ready!

This week's presentation includes:
• Key Research Papers
• Industry Updates
• Tools & Frameworks
• Notable Discussions

Generated automatically from arXiv, Hacker News, and Reddit.

Enjoy your learning!

---
AI Weekly Digest System
Generated on {date_str}
"""
        msg.attach(MIMEText(body, 'plain'))

        # Attach presentation
        filename = Path(filepath).name
        try:
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                msg.attach(part)

            print(f"  ✓ Attached: {filename}")

        except Exception as e:
            print(f"  ❌ Error attaching file: {e}")
            return False

        # Send email
        try:
            print(f"  ✓ Connecting to {smtp_server}:{smtp_port}...")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            print(f"  ✓ Logging in as {sender_email}...")
            server.login(sender_email, sender_password)

            print(f"  ✓ Sending to {recipient}...")
            server.send_message(msg)
            server.quit()

            print(f"\n✅ Email sent successfully!")
            return True

        except smtplib.SMTPAuthenticationError:
            print(f"  ❌ Authentication failed")
            print(f"  💡 For Gmail, use an App Password:")
            print(f"     https://myaccount.google.com/apppasswords")
            return False

        except Exception as e:
            print(f"  ❌ Error sending email: {e}")
            return False

async def send_email(filepath: str) -> bool:
    """Async wrapper for email sending"""
    sender = EmailSender()
    return sender.send_presentation(filepath)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        sender = EmailSender()
        sender.send_presentation(sys.argv[1])
    else:
        print("Usage: python email_sender.py <path-to-presentation>")
