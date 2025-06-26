from . import cas_bp
from flask import redirect,url_for,session,current_app,request
import requests
from xml.etree import ElementTree
from urllib.parse import quote


@cas_bp.route("/login")
def login():
    
    next_url = request.args.get("next") or url_for("index.index")
    session["next"] = next_url
    
    cas_server = current_app.config.get("CAS_SERVER")
    service_url = get_service_url()
    service_encoded = quote(service_url, safe='')
    current_app.logger.info(f"{cas_server}/login?service={service_encoded}")
    return redirect(f"{cas_server}/login?service={service_encoded}")


@cas_bp.route("/callback")
def callback():
    ticket = request.args.get("ticket")
    if not ticket:
        current_app.logger.error("Missing CAS ticket")
        return "Authentication faild: missing ticket", 400
    
    cas_server = current_app.config.get("CAS_SERVER")
    service_url = get_service_url()
    service_encoded = quote(service_url, safe='')
    validate_url = f"{cas_server}/lyuapServer/serviceValidate?service={service_encoded}&ticket={ticket}"

    try:
        response = requests.get(validate_url,timeout=10)
        response.raise_for_status()

        ns = {
            "cas":"http://www.yale.edu/tp/cas"
        }

        
        try:
            root = ElementTree.fromstring(response.content)
        except ElementTree.ParseError:
            current_app.logger.error("Invalid XML response: %s", response.text)
            return "CAS validation error", 500
        
        user_element = root.find("cas:authenticationSuccess/cas:user", ns)
        if user_element is None:
            current_app.logger.error("CAS authentication failed: %s", response.content)
            return "Authentication faild", 401
        
        user_id = user_element.text
        session["user_id"] = user_id
        current_app.logger.info(f"User authenticated:{user_id}")

        next_url = session.pop('next', None)
        if next_url is None:
            next_url = url_for('index.index')  # 确保这里端点正确
            current_app.logger.debug(f"Callback: next_url is None, using default: {next_url}")
        current_app.logger.debug(f"Callback: next_url is None, using default: {next_url}")
        current_app.logger.info("登录成功")
        return redirect(next_url) # 重定向到原始请求页面或默认页面
    except Exception as e:
        current_app.logger.exception("CAS validation error")
        return f"Authentication error: {str(e)}", 500
    

def get_service_url():
    """获取服务回调URL"""
    return url_for('cas.callback', _external=True)


@cas_bp.route('/logout')
def logout():
    session.clear()
    cas_server = current_app.config.get("CAS_SERVER")
    service_url = url_for('cas.login', _external=True)
    return redirect(f"{cas_server}/logout?service={service_url}")