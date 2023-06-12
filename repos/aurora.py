from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class DischargeSummary(Base):
    __tablename__ = 'discharge_summaries'

    submission_id = Column(String, primary_key=True)
    submit_revision = Column(String, primary_key=True)
    submit_date = Column(DateTime)
    form_id = Column(String)
    pdf_id = Column(String)
    provider_name = Column(String)
    chart_number = Column(Integer)
    discharge_date = Column(Date)
    admission_date = Column(Date)


class AuroraStore:
    
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create(self, model):
        try:
            self.session.add(model)
            self.session.commit()
        except Exception as e:
            print(f"Error adding to database: {e}")
            self.session.rollback()
        finally:
                self.close()


    def close(self):
        self.session.close()


