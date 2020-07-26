from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "postgresql://postgres:admin@localhost/timesheets"
EMAIL_DOMAIN = "@example.com"

engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)
