import pytest

from ewauth import mail
from ewauth.api.mail import send_email


@pytest.mark.usefixtures("in_memory_db")
def test_send_mail():
    html_template = "<h1>Test Message</h1>"
    text_template = "Test Message"

    with mail.record_messages() as outbox:
        send_email("sanson@example.com",
                   "test",
                   html_template=html_template,
                   text_template=text_template
                   )
        assert len(outbox) == 1

        msg = outbox[0]
        assert msg.subject == "test"
        assert "Test Message" in msg.body
        assert "Test Message" in msg.html
