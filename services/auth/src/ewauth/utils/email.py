from ewauth.config import get_emails_file_path


def insert_email(email: str) -> None:
    """ Insert a new email into the valid emails file.
    """
    email_file = get_emails_file_path()
    with open(email_file, "a") as fp:
        fp.write('\n' + email)
