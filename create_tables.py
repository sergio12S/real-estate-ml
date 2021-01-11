from db import engine, Apartments

Apartments.__table__.create(bind=engine, checkfirst=True)
