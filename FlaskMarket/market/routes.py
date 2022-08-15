from market.forms import LoginForm, PurchaseItemForm, RegisterForm, SellItemForm
from market.models import Item,User
from flask import render_template,redirect,url_for,flash,request
from market import app
from market import db,bcrypt
from flask_login import login_user,logout_user,login_required,current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')
    # this will go to home.html and when we click getstarted there it will redirected to market page


@app.route("/market@market@",methods=['GET','POST'])

# this will be responsible for not taking user to market page without authentication ,this is a function
# which can be used as a decorator
# decorators are like functions which gets executed before the actual function itself
@login_required
# if the user is not authenticated it has to go to login page,for that it will go to init file
def market_page():
    purchase_form=PurchaseItemForm() 
    selling_form=SellItemForm()
    

    # request is an inbuilt object
    # request.method=="GET" and request.method=="POST" will prevent our form 
    # from resubmisission after every refresh 
    if request.method=="POST":
        #PURCHASE ITEM LOGIC
        
        # request has to be imported-As we know there are already diiferent requests is created 
        # for manging this website,so flask library gives us access to that built in request object 
        # to really have a fully control of how the request object looks like every time that we create 
        # some requests like GET or POST.here info about the purchased_item will be availbale in the 
        # built in object request

        

        purchased_item=request.form.get('purchased_item')
        p_item_object=Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            # current_user has to import 
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congrats,You have purchased {p_item_object.name} for {p_item_object.price}$",category="success")
            else:
                flash(f"Unfortunately,you dont have enough money to purchase {p_item_object.name}",category="danger")

        #SELLING ITEM LOGIC
        selling_item=request.form.get("selling_item")
        s_item_object=Item.query.filter_by(name=selling_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"You have Successfully sold {s_item_object.name} for {s_item_object.price}$ back to market",category="success")
            else:
                flash(f"Something went wrong in selling {s_item_object.name}")
        return redirect(url_for('market_page'))

        
    # items = [
    # {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    # {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    # {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    #         ]

    # when it comes to market_page this will execute first
    # that means it shows items yet to purchase in the market and items that owns by that particular
    if request.method=="GET":
        items=Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items,purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)

@app.route("/register",methods=['GET','POST'])
def reg_page():
    form=RegisterForm()
    if form.validate_on_submit():
        # here the password is not in encrypted form,In models.py password encryption takes place
        new_user=User(username=form.username.data,email=form.email.data,password=form.pswd1.data)
        #HERE ACTUALLY THE REGISTER FORM IN THE UI AND DATABASE IN THE BACKEND CONNECTS,WHERE BACKEND
        #COLLECTS INFORMATION FROM FORM_______
        db.session.add(new_user)
        db.session.commit()

        # if we have not done this then the page will be redirected to login page after reg page
        login_user(new_user)
        flash(f"Account created successfully ! You are logged in as {new_user.username}",category='success')
        return redirect(url_for('market_page'))
    if form.errors!={}:
        # here what errors we get is ,with form validators we have verified many errors in the form.py file 
        # that errors will pop out here
        for x in form.errors.values():
            flash(f'There was an error creating with a user {x}',category="danger")
            # flash will helps in displaying the message in the html template
            # in the html file there will be get flash messages which will gather all the 
            # flashed messages.we will be using this in base.html
    return render_template("register.html",form=form)

@app.route("/login",methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        
        attempted_user=User.query.filter_by(username=form.username.data).first()
        # checks the attempteduser with user object and if exits ,checks is the password  matched with that in database
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
            #bcrypt.check_password_hash(self.paswd_hash,form.password.data)
          login_user(attempted_user)
          flash(f'Success!You are logged in as :{attempted_user.username}',category='success')
          return redirect(url_for('market_page'))
        else:
            flash("Username and password doesnot match!Please Try again",category='danger')

    return render_template("login.html",form=form)

@app.route("/logout")
def logout_page():
    # grabs the current logged in user and log it out
    logout_user()

    flash("You have been logged out!", category='info' )
    return render_template("home.html")