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
        Return a tuple of two list.
        list 1: Names
        list 2: Emails
        """

        names = []
        emails = []
        with open(filepath, mode='r', encoding='utf-8') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split()[0])
                emails.append(a_contact.split()[1])

        return names, emails

    @staticmethod
    def generate_template(filepath: str) -> Template:
        """
        Returns a Template object comprising the contents of the
        file specified by filename.
        """

        try:
            with open(filepath, 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()
        except Exception as error:
            print('Error Occurred', str(error))
            raise error

        return Template(template_file_content)


companies = ['Google', 'Facebook', 'Tata Consultancy Services', 'Freshworks', 'EBay', 'Amazon', 'Apple', 'Pinterest',
             'Twitter', 'Tumblr', 'Snapchat', 'Qualcomm', 'TikTok', 'Evernote', 'Flipkart']

arr_names = ['Robert', 'David', 'Elise', 'Charles', 'Bill', 'Will', 'Johnny', 'Bruce', 'Barbara', 'Donald', 'Alberta',
             'Tyler', 'Shawn', 'Arthur', 'Brenda']

MY_ADDRESS = '<Enter EMAIL>'
PASSWORD = '<Enter Password>'


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    # names, emails = #get_contacts('mycontacts.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    # for name, email in zip(names, emails):
    for company, n in zip(companies, arr_names):
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=n.title(), COMPANY_NAME=company.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = 'crpc.spc10@gmail.com'
        msg['Subject'] = "IIM Ranchi || Invitation for Colloquium – A Leadership Talk Series || " + company

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()


if __name__ == '__main__':
    main()
