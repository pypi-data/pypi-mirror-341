import sys

sys.path.append('../')

from download_all_attachments_in_inbox import download_all_attachments_in_inbox
from config.get_email_path import get_email_path


def email_update(emails, storage_root="", limit=3):
    for email in emails:
        data_path = get_email_path(email["target"], storage_root)
        download_all_attachments_in_inbox(email["server"], email["username"], email["password"], data_path, email["source"], limit)
