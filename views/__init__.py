from flask import Blueprint,current_app,request
from flask import redirect, session,url_for
from functools import wraps

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

index_bp = Blueprint(
    "index",
    __name__,
    url_prefix="/index"
)

cas_bp = Blueprint(
    "cas",
    __name__,
    url_prefix="/cas"
)


# 自定义登录装饰器
def cas_required(view_func):
    """自定义CAS登录装饰器"""
    @wraps(view_func) # 关键：保留原始函数的元数据，查了很久才搞定
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            # 保存原始请求URL
            session['next'] = request.url
            current_app.logger.debug(f"cas_required: User not authenticated. Saving next to session: {request.url}")
            return redirect(url_for('cas.login'))
        return view_func(*args, **kwargs)
    return wrapper