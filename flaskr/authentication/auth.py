from flask import Blueprint, redirect, render_template, request
from flaskr.functions import *
from flaskr.models import Users
from flaskr.forms import Login_form, RegistrationForm, Forgot_password_form, Creat_new_password, Reset_password
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer

bp = Blueprint('auth', __name__,
               template_folder='templates',
               static_folder='static')  # url_prefix="/auth"
s = URLSafeTimedSerializer("Very secret key")


@bp.route("/login", methods=["get", 'post'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        password = request.form.get('password')
        user = Users.query.filter_by(email=request.form.get('email').lower()).first()
        if user and user.password == password:
            login_user(user, remember=request.form.get("remember"))
        else:
            flash("Email address and password does not match!.", "info")
        return redirect("/")
    else:
        return render_template("login.html", title="Login", form=form)


@bp.route('/registration_form', methods=['GET', 'POST'])
def registration_form():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        fname = request.form.get('fname').title()
        mname = request.form.get('mname').title()
        lname = request.form.get('lname').title()
        dob = request.form.get('dob')
        password = request.form.get('password')
        quary = """INSERT INTO `users`(`fname`,`mname`,`lname`,`dob`,`email`,`password`) VALUES('{}','{}','{}','{}','{}',{})""".format(
            fname,
            mname,
            lname,
            dob, email,
            password)
        if run_in_database(quary=quary, commit='yes'):
            flash("Registration Successful!. Please Login with Your Email and Password!.", "success")
            return redirect("/")
        else:
            flash("Internal Database Problem!.", "danger")
    return render_template("register.html", title="Register", form=form)


@bp.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    form = Forgot_password_form()
    if form.validate_on_submit():
        email = request.form.get('email').lower()
        token = s.dumps(email, salt="this_is_the_email")
        reset_url = "http://" + str(request.host) + "/reset_password/" + str(token)
        send_mail(to=email, name=Users.query.filter_by(email=email).first().fname, reset_url=reset_url)
        flash("URL to reset your password is send to " + email + ", Visit your Email to Reset Your Password!",
              "success")
        return redirect('/')
    else:
        return render_template("forgot_password_one.html", form=form)


@bp.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password_with_token(token):
    form = Creat_new_password()
    try:
        email = s.loads(token, salt="this_is_the_email", max_age=900)
    except:
        flash("URL for password reset Expired!. Try Password reset option again to get a valid Password Reset URL.",
              "danger")
        return redirect("/")
    if form.validate_on_submit():
        password = request.form.get('cnpassword')
        query = "UPDATE `users` SET `password`= '{}' WHERE `email` = '{}';".format(password, email)
        _ = run_in_database(quary=query, commit='yes')
        flash("Password Changed Successfully!. Try Login with new Password.", "success")
        return redirect("/")
    else:
        return render_template("reset_password.html", form=form, )


@bp.route('/password_validation', methods=['GET', 'POST'])
@login_required
def password_validation():
    form = Reset_password()
    if form.validate_on_submit():
        cpassword = request.form.get('password')
        cnpassword = request.form.get('cnpassword')
        if current_user.password == cpassword:
            query = """UPDATE `users` SET `password`= '{}' WHERE `user_id` LIKE {};""".format(cnpassword,
                                                                                              current_user.id)
            __ = run_in_database(quary=query, commit='yes')
            flash("Password Updated Successful!.", "success")
        else:
            flash("Current Password Does Not Match!", "danger")
    return redirect("/settings")


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')