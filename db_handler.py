from sqlalchemy.orm import Session

# DB Handler class that handles all database interaction
class DBHandler:
    def __init__(self, db: Session) -> None:
        super().__init__()
        self._db = db
