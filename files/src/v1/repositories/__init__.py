from typing import NamedTuple

from sqlalchemy.orm import Session

from ...db import engine


class Pagination(NamedTuple):

    total: int
    pages: int
    page: int
    page_size: int
    items: list


class Repository:

    def __init__(self, session: Session | None = None):
        self.session = session if session else Session(bind=engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:  # Check if an exception occurred
            self.session.rollback()  # Roll back the session to revert changes

        self.session.close()  # Close the session in any case
        if exc_type:  # Re-raise the exception after handling it
            raise exc_val

    def commit(self):
        self.session.commit()
