"""
Audit Log module for interacting with the Y360.
"""

__version__ = "0.1.0"

from y360_orglib.audit.audit_mail import AuditMail
from y360_orglib.audit.models import MailEventsPage, MailEvent

__all__ = ["AuditMail", "MailEventsPage", "MailEvent"]
