from market import db,login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#the logic is we will build a model for the database here,and in terminal 
#using commands we can create database
class User(db.Model,UserMixin):
    # here usermixin will allow us call function like is_authenticated,is_active etc..
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email=db.Column(db.String(length=60),nullable=False,unique=True)
    paswd_hash=db.Column(db.String(length=60),nullable=False,unique=True) 
    budget=db.Column(db.Integer(),nullable=False,default=1000)
    items=db.relationship('Item',backref="owned_user",lazy=True)
    # User.items will give the list of all items owned by that user
    # But if we want to know the owner of a specific item
    # we can access by item.owned_user.So basically owned_user is an attribute of Item table
    # but for this we have to make a column named owner in item database

    # Lazy =True is to grab all the items owned by an user through a single shot

    @property
    # this property is dynamic
    def pretty_budget(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"


    @property
    def password(self):
        return self.password

    # takes the password from password column in form and encrypted password will be set
    @password.setter
    def password(self,plain_text_password):
        self.paswd_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        # print(bcrypt.check_password_hash(self.paswd_hash,attempted_password))
        return bcrypt.check_password_hash(self.paswd_hash,attempted_password)

    def can_purchase(self,item_obj):
        return self.budget>=item_obj.price

    def can_sell(self,item_obj):
        return item_obj in self.items
            

class Item(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    barcode=db.Column(db.String(length=15),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    description=db.Column(db.String(length=1024),nullable=False,unique=True)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Item.{self.name}'

    def buy(self,user):
        self.owner=user.id
        user.budget-=self.price
        db.session.commit()

    def sell(self,user):
        self.owner=None
        user.budget+=self.price
        db.session.commit()


#The baseclass for all your models is called db. Model 
# . It's stored on the SQLAlchemy instance you have to create. 
# What is model in SQLAlchemy?
# Model is a class within the Flask-SQLAlchemy project. Flask-SQLAlchemy makes it easier 
# to use SQLAlchemy within a Flask application. SQLAlchemy 
# is used to read, write, query and delete persistent data in a relational database through SQL