from flask import Flask
import yaml
from models import db,User
from flask_migrate import Migrate
from flask_login import LoginManager
import json

# app构造函数
def create_app(env='DEFAULT'):
    app = Flask(__name__)
    with open("config/luncher.yaml",'r',encoding='utf-8') as config_file:
        config_data = yaml.safe_load(config_file,)
        if env in config_data:
            current_config = config_data[env]
        else:
            current_config = config_data["DEFAULT"]
        app.config.update(current_config)

    # 初始化扩展
    db.init_app(app=app)

    # 初始化migrate
    migrate = Migrate(app=app,db=db)

    # 注册蓝图
    # from views.auth import auth_bp
    from views.index import index_bp
    from views.cas import cas_bp

    # app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(cas_bp)

    # 初始化Flask-Login
    login_manager = LoginManager(app=app)
    # 设置登陆视图的端点，需要登录的时候重定向到此处
    login_manager.login_view = "cas.login" # type: ignore 


    # 创建登录加载器
    with app.app_context():
        @login_manager.user_loader
        def load_user(user_id):
            return db.session.get(User,user_id)
        
    return app

# 创建应用
app = create_app("DEVELOPMENT")



if __name__ == "__main__":
    print(app.config)
    app.run(
        host=app.config["HOST"]
    )