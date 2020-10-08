from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ORMAnimal(Base):
    __tablename__ = 'orm_animals'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    specie = Column(String(50))

    def __repr__(self):
        return "<ORMAnimal(id='%s', name='%s', specie='%s')>" % (
                                self.id, self.name, self.specie)

engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


session.add_all([
     ORMAnimal(name='Tortoise', specie='Testudines'),
     ORMAnimal(name='Salmon', specie='Salmonidae'),
     ORMAnimal(name='Dog', specie='Canis lupus'),
     ORMAnimal(name='Cat', specie='Felis silvestrus catus')])

session.commit()

def print_values(results):
    for element in results:
        print("Element: ", element)

def insert_element(name, specie):
    session.add(ORMAnimal(name=name, specie=specie))
    session.commit()

def find_by_id(id):
    return session.query(ORMAnimal).filter_by(id=id).one()

query = session.query(ORMAnimal)
for element in query.all():
    print("Element: ", element)

query = session.query(ORMAnimal).filter(ORMAnimal.specie.like('%ni%')).order_by(ORMAnimal.specie)
print_values(query.all())

insert_element("Squirrel", "Sciurinae")
query = session.query(ORMAnimal)
print_values(query.all())

insert_element("Fox", "Vulpini")
insert_element("Wolf", "Canis lupus")

print_values(session.query(ORMAnimal).all())
print("Value: ", find_by_id(5))

