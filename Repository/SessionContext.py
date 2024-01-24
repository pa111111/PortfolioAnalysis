from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st

user = st.secrets["database"]["user"]
password = st.secrets["database"]["password"]
host = st.secrets["database"]["host"]
port = st.secrets["database"]["port"]
dbname = st.secrets["database"]["dbname"]


class SessionContext:
    def __enter__(self):
        engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, dbname))
        session_factory = sessionmaker(bind=engine)
        self.session = session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
