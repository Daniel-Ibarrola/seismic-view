from ewauth.config import ProdConfig


def test_prod_config_loads_email_from_file():
    emails = ProdConfig.valid_emails()
    assert emails == ["triton@example.com"]
