import imaplib
def delete_emails(email, password, mailserver, mailbox="Inbox", mailtrash="Trash", last_messages=100, xx = 0):
    # Connecting to the mail server
    mail = imaplib.IMAP4_SSL(mailserver)
    # Logging in
    mail.login(email, password)
    mail.select(mailbox)

    # get the list of email IDs
    result, data = mail.uid('search', None, "ALL")
    if result == 'OK':
        for num in data[0].split():
            print(num)
            xx = xx + 1
            if xx > last_messages: break
            mail.uid('store', num, '+FLAGS', '(\Deleted)')
        mail.expunge()
    # close the mailbox
    mail.close()

    # logout from the email server
    mail.logout()
