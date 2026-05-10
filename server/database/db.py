from sqlalchemy import create_engine
from sqlalchemy import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"

engine = create_engine({
	SQLALCHEMY_DATABASE_URL,
	connect_args = {"check_same_thread": False}
	)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
	pass

def get_db():
	with sessionlocal() as db:
		yield db