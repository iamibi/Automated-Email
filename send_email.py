#!/usr/bin/env python3

# Imports
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib


class SendEmail:
    def __init__(self, email_address: str, email_password: str) -> None:
        """
        Initialize the class with the email_address and email password.
        """

        self.email_address = email_address
        self.email_password = email_password

    @staticmethod
    def get_contacts(filepath: str) -> tuple:
        """
        Reads a text file with name and email entry.
        It should be like <name email>.
        Return a tuple of two list.
        list 1: Names
        list 2: Emails
        """

        names = []
        emails = []
        try:
            with open(filepath, mode='r', encoding='utf-8') as contacts_file:
                for a_contact in contacts_file:
                    names.append(a_contact.split()[0])
                    emails.append(a_contact.split()[1])
        except Exception as error:
            print('Error occurred while reading the contact file: %s' % (str(error)))
            raise error

        return names, emails

    @staticmethod
    def generate_template(filepath: str) -> Template:
        """
        Reads a text file with the message as plain text and create
        a template with substitutable values.

        Returns a Template object comprising the contents of the
        file specified by filepath.
        """

        try:
            with open(filepath, 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()
        except Exception as error:
            print('Error occurred while reading the message file: %s' % (str(error)))
            raise error

        return Template(template_file_content)

    def init_smtp_library(self, host='smtp.gmail.com', port=587) -> SMTP:
        # set up the SMTP server
        s = smtplib.SMTP(host=host, port=port)
        s.starttls()
        s.login(self.email_address, self.email_password)

        return s

    def send_email(self,
                   message_filepath: str,
                   contacts_filepath: str,
                   email_subject: str,
                   subs_dict: dict = {}):
        """
        Reads the message template and contacts file
        and sends the email to respective address.
        """

        # Read the message file.
        message_template = self.generate_template(message_filepath)
        smtp = self.init_smtp_library()
        names, emails = self.get_contacts(contacts_filepath)

        # Iterate over the names and email combination.
        for receiver_name, receiver_email in zip(names, emails):
            subs_dict['NAME'] = receiver_name

            # create a message
            msg = MIMEMultipart()

            email_body = message_template.substitute(subs_dict)
            msg['From'] = self.email_address
            msg['To'] = receiver_email
            msg['Subject'] = email_subject

            # Add the Email body as plain text.
            msg.attach(MIMEText(email_body, 'plain'))

            # Send the email.
            smtp.send_message(msg)
            del msg

        # Terminate the SMTP session and close the connection
        smtp.quit()


if __name__ == '__main__':
    main()
