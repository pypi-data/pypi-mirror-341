from .models import Base
from . import engine

def init_db():
    Base.metadata.create_all(engine)