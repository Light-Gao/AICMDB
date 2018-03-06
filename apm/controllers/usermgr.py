from os import path
from flask import render_template, Blueprint, redirect, url_for, flash
from apm.forms import LoginForm, RegisterForm
from apm.models import db, User, Service

"""Define BluePrint for users"""
user_blueprint = Blueprint('user', __name__,
                           template_folder=path.join('../templates/user'),
                           url_prefix='/user')

@user_blueprint.route('/')
def index():
    return redirect(url_for('svc.show_svc'))

@user_blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
    #create login form from LoginForm
    login_form = LoginForm()
    #define action if validate_on_submit()
    if login_form.validate_on_submit():
        flash("Login succeed!", category="success")
        return redirect(url_for('svc.dashboard'))

    #render template
    return render_template('login.html', form=login_form)

@user_blueprint.route('/logout', methods=['GET', 'POST'])
def user_logout():
    flash("Logged OUT succeed!", category="success")
    return redirect(url_for('svc.show_svc'))

@user_blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    #create register form from RegisterForm
    reg_form = RegisterForm()
    #define action if reg_form.validate_on_submit()
    if reg_form.validate_on_submit():
        #reg_form.user_name's type is StringField, So must use '.data'.
        new_user = User(user_name=reg_form.user_name.data,
                        user_passwd=reg_form.user_passwd.data)
        db.session.add(new_user)
        db.session.commit()

        flash("You have registered, please login!", category="success")
        return redirect(url_for('user.user_login'))
    #render template
    return render_template('register.html', form=reg_form)

@user_blueprint.route('/<string:username>')
def user(username):
    """View function for user page
    form = UserForm()
    if form.validate_on_submit():
        """

    apm_user = db.session.query(User).filter_by(apm_user_name=username).first_or_404()
    svc = apm_user.service.order_by(Service.apm_service_id.asc()).all()

    return render_template('user.html', user=apm_user, svc=svc)
