# from . import auth_bp
# from flask import render_template,redirect,url_for,flash,session
# from flask_login import login_user,current_user
# from werkzeug.security import check_password_hash
# from models import User,db
# from forms import LoginForm


# @auth_bp.route("/login",methods=["POST","GET"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for("index.index"))
    
#     form = LoginForm()
#     if form.validate_on_submit():
#         user_id = form.user_id.data
#         password = form.password.data

#         # user = User.query.filter_by(email=email).first()
        
#         user = db.session.scalars(db.select(User).where(User.user_id == user_id)).first()
#         print(user)

#         if user and check_password_hash(user.password,password=password): # type: ignore
#             login_user(user=user)
#             flash("登录成功",'success')
#             return redirect(url_for("index.index"))
#         else:
#             flash("用户名或密码错误",'danger')

#     return render_template("login.html",form=form)


# # @auth_bp.route("/logout")
# # @login_required
# # def logout():
