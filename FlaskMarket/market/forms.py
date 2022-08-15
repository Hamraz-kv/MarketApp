from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    # HERE WE WILL SEE REST OF THE VALIDATIONS
    # here the name validate_username is unique
    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists,please try a different username")
            # raise will also act like flash

    def validate_email(self,email_to_check):
        user=User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("Email already exists,please try a different email")
    #---------------------------------------------------------------------------------------------
    username=StringField(label="Username",validators=[Length(min=2,max=30),DataRequired()])
    # LABEL SEEING HERE WILL BE IN OUR FRONT END FORM
    email=StringField(label="Email Id", validators=[Email(),DataRequired()])
    pswd1=PasswordField(label="Password1",validators=[Length(min=6),DataRequired()])
    pswd2=PasswordField(label="Password2",validators=[EqualTo('pswd1'),DataRequired()])
    submit=SubmitField(label="Create Account")

class LoginForm(FlaskForm):
    username=StringField(label="Username",validators=[DataRequired()])
    password=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField(label="Login")

class PurchaseItemForm(FlaskForm):
    submit=SubmitField(label="Buy Item!")

class SellItemForm(FlaskForm):
    submit=SubmitField(label="Sell Item!")
