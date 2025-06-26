from flask_sqlalchemy import SQLAlchemy
# import cx_Oracle


# # oracle连接使用精简模式
# cx_Oracle.init_oracle_client(lib_dir=None)

db = SQLAlchemy() # 创建db示例给模型使用

from .user import User
from .salary import Salary

# 明确要导出的列表
__all__ = [
    'db',
    'User',
    'Salary'
]