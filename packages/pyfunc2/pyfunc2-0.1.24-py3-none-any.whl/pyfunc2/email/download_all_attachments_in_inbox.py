import sys

sys.path.append('../')

from download_attachments_in_email import download_attachments_in_email
from connect import connect


# Download all the attachment files for all emails in the inbox.
def download_all_attachments_in_inbox(server, user, password, outputdir, remote_folder="inbox", limit=3):
    m = connect(server, user, password)

    # resp, messages = m.search(None, "(ALL)")
    # resp, messages = m.search(None, "(UNSEEN)")

    # resp, messages = m.select("INBOX")
    # resp, messages = m.select(remote_folder, readonly=True)
    resp, messages = m.select(remote_folder)

    # number of top emails to fetch

    get_newest_messages(m, messages, outputdir, limit)
    # get_all_messages(m, messages, outputdir)


def get_newest_messages(m, messages, outputdir="", limit=999999, xx=1):
    # total number of emails
    messages = int(messages[0])
    print("get_newest_messages messages:", messages)
    for emailid in range(messages, messages - limit, -1):
        resp, data = m.fetch(str(emailid), "(BODY.PEEK[])")
        download_attachments_in_email(resp, data, emailid, outputdir)
        print(emailid, outputdir)
        xx = xx + 1


def get_all_messages(m, messages, outputdir="", limit=999999, xx=1):
    messages = messages[0].split()
    for emailid in messages:
        download_attachments_in_email(m, emailid, outputdir)
        print(emailid, outputdir)
        xx = xx + 1
        if xx > limit: exit(1)
