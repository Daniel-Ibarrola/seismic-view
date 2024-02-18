from ewauth import db


class Email(db.Model):
    """ Email table to store emails that can be used to register new users.
    """
    __tablename__ = "emails"
    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    email: db.Mapped[str] = db.mapped_column(db.String(64), unique=True, index=True)

    @staticmethod
    def is_email_valid(address: str) -> bool:
        result = db.session.execute(
            db.select(Email).filter_by(email=address)
        ).scalar_one_or_none()
        return result is not None
