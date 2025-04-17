from ftplib import FTP
import os, os.path

# Connect to an IMAP server

# Download all the attachment files for all emails in the inbox.
def ftp_download(server, user, password, outputdir, remote_folder=".."):

    os.chdir(outputdir)
    ftp = FTP(server, user, password)

    print ('Logging in.')
    ftp.login(user, password)

    print('Changing to ' + outputdir)
    ftp.cwd(remote_folder)
    ftp.retrlines('LIST')

    print('Accessing files')
    filenames = ftp.nlst()  # get filenames within the directory
    print (filenames)

    for filename in filenames:
        local_filename = os.path.join(outputdir, filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, file.write)

        file.close()

    ftp.quit()

