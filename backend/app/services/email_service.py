import logging
import os
import resend
from app.core.config import settings

logger = logging.getLogger("email_service")


def send_password_reset_email(to_email: str, user_name: str, reset_token: str) -> bool:
    """
    Sends a password reset email using Resend API.
    Includes a direct reset button, fallback link, 30-minute expiration notice, and security warnings.
    """
    app_url = settings.FRONTEND_URL.rstrip("/")
    reset_link = f"{app_url}/reset-password?token={reset_token}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Reset Your Password</title>
      <style>
        body {{
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          background-color: #0F172A;
          color: #F8FAFC;
          margin: 0;
          padding: 40px 20px;
        }}
        .container {{
          max-width: 560px;
          margin: 0 auto;
          background: #1E293B;
          border: 1px solid #334155;
          border-radius: 16px;
          padding: 36px;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }}
        .brand {{
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 24px;
        }}
        .brand-title {{
          font-size: 20px;
          font-weight: 800;
          color: #38BDF8;
          letter-spacing: -0.5px;
        }}
        h1 {{
          font-size: 22px;
          font-weight: 700;
          color: #F8FAFC;
          margin-top: 0;
          margin-bottom: 12px;
        }}
        p {{
          font-size: 15px;
          line-height: 1.6;
          color: #94A3B8;
          margin-bottom: 24px;
        }}
        .button-wrapper {{
          text-align: center;
          margin: 32px 0;
        }}
        .reset-button {{
          display: inline-block;
          background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%);
          color: #FFFFFF !important;
          font-weight: 600;
          font-size: 15px;
          padding: 14px 32px;
          border-radius: 10px;
          text-decoration: none;
          box-shadow: 0 4px 16px rgba(14, 165, 233, 0.35);
        }}
        .fallback-box {{
          background: #0F172A;
          border: 1px solid #334155;
          border-radius: 8px;
          padding: 12px;
          word-break: break-all;
          font-size: 13px;
          color: #38BDF8;
          margin-bottom: 24px;
        }}
        .notice {{
          font-size: 13px;
          color: #64748B;
          border-top: 1px solid #334155;
          padding-top: 20px;
          margin-top: 32px;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="brand">
          <div class="brand-title">AI Learning Platform</div>
        </div>
        
        <h1>Password Reset Request</h1>
        
        <p>Hello {user_name or 'Learner'},</p>
        
        <p>We received a request to reset the password for your AI Learning Platform account. Click the button below to choose a new password:</p>
        
        <div class="button-wrapper">
          <a href="{reset_link}" class="reset-button" target="_blank">Reset Password</a>
        </div>
        
        <p style="margin-bottom: 8px;">Or copy and paste this link into your browser:</p>
        <div class="fallback-box">{reset_link}</div>
        
        <p><strong>Security Notice:</strong> This reset link will expire in <strong>30 minutes</strong> and can only be used once.</p>
        
        <div class="notice">
          If you did not request a password reset, you can safely ignore this email. Your password will remain unchanged and your account stays secure.
        </div>
      </div>
    </body>
    </html>
    """

    api_key = settings.RESEND_API_KEY
    if not api_key:
        logger.warning(
            f"[Resend Email Service] RESEND_API_KEY is not set. Email not dispatched to {to_email}. "
            f"Reset Link: {reset_link}"
        )
        return False

    try:
      resend.api_key = api_key
      params = {
          "from": settings.RESEND_FROM_EMAIL,
          "to": [to_email],
          "subject": "Reset your AI Learning Platform password",
          "html": html_content,
      }
      email_response = resend.Emails.send(params)
      logger.info(f"[Resend Email Service] Reset email successfully dispatched to {to_email}. Response: {email_response}")
      return True
    except Exception as e:
      logger.error(f"[Resend Email Service] Failed to send email to {to_email}: {e}")
      return False
