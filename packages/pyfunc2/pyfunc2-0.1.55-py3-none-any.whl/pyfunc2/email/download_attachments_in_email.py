import base64
import os
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pyfunc2.file.check_and_create_path import check_and_create_path
import logging

from types import NoneType


# pip install python-magic

def download_attachments_in_email(resp, data, emailid="", outputdir="", xx=0,
                                  attachements=["pdf", "jpg", "gif", "png"]):
    logging.basicConfig(level=logging.DEBUG)
    # m.store(emailid, '+FLAGS', '\Seen')
    # print("download_attachments_in_email emailid:", emailid)
    # print("download_attachments_in_email outputdir:", outputdir)

    # print("download_attachments_in_email emailid:", emailid)
    # resp, data = m.fetch(emailid, '(RFC822)')
    global type
    print("mail respo:", resp)


    if not isinstance(data, list):
        print("data is not list")
        return

    if not isinstance(data[0], tuple):
        print("data[0] is not list")
        return

    email_body = data[0][1]

    if not isinstance(email_body, bytes):
        print("email_body is not bytes")
        return

    # print(email_body)
    # print(str(email_body))
    # print(str(type(email_body)))
    # check if email_body is bytes


    #email_body = email_body.decode('utf-8')

    # print("email_body after decode is bytes")

    # print(type(email_body))
    # print(email_body)

    # print("email_body
    mail = email.message_from_bytes(email_body)

    if mail.get_content_maintype() != 'multipart':
        return

    if len(outputdir):
        outputdir = outputdir + '/'

    for part in mail.walk():
        xx = xx + 1

        names = str(emailid)
        if len(names) < 9:
            names = str(int(emailid))

        filename = names + "_" + str(xx)
        logging.debug(f"Processing part: filename={filename}")
        logging.debug(f"part.get_content_maintype()={part.get_content_maintype()}")
        logging.debug(f"part.get('Content-Disposition')={part.get('Content-Disposition')}")
        if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
            try:
                if not isinstance(part.get_filename(), NoneType):
                    print(part.get_filename())
                    root, extension = os.path.splitext(part.get_filename())
                    extension = extension.replace('.', '')
                    print("extension ", extension)

                    if extension in attachements:
                        subfolder = ""
                        if extension != attachements[0]:
                            subfolder = f'/{extension}/'
                            logging.debug(f"Creating/checking path: {outputdir + subfolder}")
                            check_and_create_path(outputdir + subfolder)

                        file_path = outputdir + subfolder + part.get_filename()
                        logging.debug(f"Saving attachment to: {file_path}")
                        open(file_path, 'wb').write(part.get_payload(decode=True))
                    # print(part.get_filename())
                else:
                    print(f"DEBUG: part.get_content_maintype()={part.get_content_maintype()}, part.get('Content-Disposition')={part.get('Content-Disposition')}")
                    try:
                        #content = part.get_payload(decode=True)
                        # get mime type from content
                        type = part.get_content_type()
                        extension = type.split("/")[1] if "/" in type else ""
                    except:
                        extension = ""

                        #print(type)
                        #print(content)
                        #print(extension)
                        #exit()
                    # print(type, extension)
                    # exit()

                    if extension in attachements:
                        subfolder = ""
                        if extension != attachements[0]:
                            subfolder = f'/{extension}/'
                            logging.debug(f"Creating/checking path: {outputdir + subfolder}")
                            check_and_create_path(outputdir + subfolder)

                        file_path = outputdir + subfolder + filename + "." + extension
                        logging.debug(f"Saving attachment to: {file_path}")
                        open(file_path, 'wb').write(part.get_payload(decode=True))
                    # open(outputdir + filename + ".html", 'wb').write()

            except FileNotFoundError as ex:
                for character in part.get_filename():
                    if character.isalnum():
                        filename += character

                #content = part.get_payload(decode=True)
                #mime = magic.Magic(mime=True)
                #type = mime.from_file(content)
                type = part.get_content_type()
                extension = type.split("/")[1] if "/" in type else ""
                print(f"DEBUG: type={type}, extension={extension}, attachements={attachements}")

                subfolder = ""
                if extension != attachements[0]:
                    subfolder = f'/{extension}/'
                    logging.debug(f"Creating/checking path: {outputdir + subfolder}")
                    check_and_create_path(outputdir + subfolder)

                file_path = outputdir + subfolder + filename + "." + extension
                logging.debug(f"Saving attachment to: {file_path}")
                open(file_path, 'wb').write(part.get_payload(decode=True))
            except Exception as e:
                logging.error(f"Error saving attachment: {e}")
        else:
            logging.debug("Skipping part: not an attachment or multipart.")
