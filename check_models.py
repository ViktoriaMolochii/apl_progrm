
from models import Session, User, Custom, Production, StatusCustom

session = Session()

user1 = User(Id=1, userName='vika', firstName='Viktoriia', lastName='Molochii', email='vika2999@gmail.com',
            password='12kjk345', phone='0682608928', userStatus=False)
user2 = User(Id=2, userName='katya', firstName='Kateryna', lastName='Ivanova', email='me12post@gmail.com',
            password='fef3434', phone='0681539818', userStatus=False)

stasusOrder1 = StatusCustom(statusCustom=1, name='delivered')
stasusOrder2 = StatusCustom(statusCustom=2, name='placed')



product1 = Production(id=1, name="phone", number=1)
product2 = Production(id=2, name="pen", number=3)

custom1 = Custom(id=1, shipDate='2021-12-10', statusCustomid=1, userid=1, productionid=2)
custom2 = Custom(id=2, shipDate='2021-11-29', statusCustomid=2, userid=2, productionid=1)





session.add(user1)
session.add(user2)

session.add(stasusOrder1)
session.add(stasusOrder2)

session.commit()


session.add(product1)
session.add(product2)

session.commit()

session.add(custom1)
session.add(custom2)
session.commit()

print(session.query(User).all()[0])
print(session.query(Custom).all()[1])
print(session.query(Production).all())
print(session.query(StatusCustom).all())

session.close()