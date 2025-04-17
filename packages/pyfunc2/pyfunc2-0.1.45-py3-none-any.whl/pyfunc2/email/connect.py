import imaplib
import email


# Connect to an IMAP server
def connect(server, user, password):
    m = imaplib.IMAP4_SSL(server)
    m.login(user, password)
    #m.select()
    #m.select(remote_folder, readonly=False)
    return m

# Download all attachment files for a given email
def downloaAttachmentsInEmail(m, emailid, outputdir, remote_folder):
    m.store(emailid, '+FLAGS', '\Seen')
    resp, data = m.fetch(emailid, "(BODY.PEEK[])")
    email_body = data[0][1]
    mail = email.message_from_bytes(email_body)
    if mail.get_content_maintype() != 'multipart':
        return
    for part in mail.walk():
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            open(outputdir + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))


# Download all the attachment files for all emails in the inbox.
def downloadAllAttachmentsInInbox(server, user, password, outputdir, remote_folder="inbox"):
    m = connect(server, user, password)
    # (ALL/UNSEEN)
    #resp, items = m.search(None, "(ALL)")
    resp, items = m.search(None, "(UNSEEN)")
    items = items[0].split()
    for emailid in items:
        downloaAttachmentsInEmail(m, emailid, outputdir, remote_folder)

