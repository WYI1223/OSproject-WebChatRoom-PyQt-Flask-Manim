from werkzeug.security import check_password_hash

class User:
    def __init__(self, username, email, password):
        # 用户类构造函数，用于初始化用户对象
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def is_authenticated():
        # 静态方法：用户是否已经通过身份验证
        return True

    @staticmethod
    def is_active():
        # 静态方法：用户是否处于活动状态
        return True

    @staticmethod
    def is_anonymous():
        # 静态方法：用户是否匿名
        return False

    def get_id(self):
        # 获取用户ID
        return self.username

    def check_password(self, password_input):
        # 检查用户输入的密码是否与存储的密码匹配
        return check_password_hash(self.password, password_input)
