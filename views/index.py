from . import index_bp,cas_required,session
from models import Salary,db
from flask import render_template,request,redirect,current_app,url_for


@index_bp.route("/",methods=["GET"])
@cas_required
def index():
    user_id = session["user_id"]
    if not find_user(user_id):
        current_app.logger.warning("user_id"+user_id)
        return redirect(url_for("index.user_not_find",user_id=user_id))
    year = request.args.get("year")
    frequency = request.args.get("frequency")
    month = request.args.get("month")
    if month:
        year = month[:4]
        frequency = month[4:6]
        current_app.logger.info("重定向。。。")
        return redirect(url_for("index.index",year=year, frequency=frequency))
    current_app.logger.warning("year===>"+str(year))
    current_app.logger.warning("frequency===>"+str(frequency))
    salary = fetch_latest_salary(user_id,year=year,frequency=frequency)
    current_app.logger.info("页面渲染成功")
    return render_template("base.html",salary=salary,month_list = get_month_list(user_id=user_id))


def fetch_latest_salary(user_id, **kwargs):
    query = Salary.query
    query = query.filter_by(user_id=user_id)
    if kwargs.get("year") not in [None, '']:
        query = query.filter_by(year=kwargs["year"])
    if kwargs.get("frequency") not in [None, '']:
        query = query.filter_by(frequency=kwargs["frequency"])
    results = query.order_by(Salary.time.desc()).all()
    if results:
        current_app.logger.info("salary data loaded")
        return results[0]
    else:
        current_app.logger.error("No salary record found for the given criteria")
        return None


def get_month_list(user_id):
    stmt = db.session.query(Salary.time).filter_by(user_id = user_id).order_by(Salary.time.desc()).distinct()
    result = db.session.scalars(stmt).all()
    current_app.logger.info(f"user:<{user_id} month:{','.join(result)}>")
    current_app.logger.info("月份数据已返回")
    return result


def find_user(user_id):
    return db.session.query(Salary).filter(Salary.user_id == user_id).first() is not None


@index_bp.route("/uef",methods=["GET"])
def user_not_find():
    return render_template("user_not_found.html",user_id = session["user_id"])