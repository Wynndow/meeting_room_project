from . import auth
from ..lib.email_reminder import EmailReminder

@auth.route('/send_emails', methods=['POST'])
def send_emails():
    email_reminder = EmailReminder()
    email_reminder.send_reminders()
    return 'Nice', 204
