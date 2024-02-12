from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import toml

parsed_toml = toml.load("Repository/secrets.toml")
user = parsed_toml["user"]
password = parsed_toml["password"]
host = parsed_toml["host"]
port = parsed_toml["port"]
dbname = parsed_toml["dbname"]


class SessionContext:
    def __enter__(self):
        engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, dbname))
        session_factory = sessionmaker(bind=engine)
        self.session = session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
