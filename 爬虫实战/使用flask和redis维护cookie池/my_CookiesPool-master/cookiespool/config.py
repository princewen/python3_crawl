# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'redis'

# 配置信息，无需修改
REDIS_DOMAIN = '*'
REDIS_NAME = '*'


# 进程开关
# 产生器，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True


# 产生器和验证器循环周期
CYCLE = 120

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'weibo': 'WeiboCookiesGenerator'
}

# 产生器默认使用的浏览器
DEFAULT_BROWSER = 'Chrome'

# 云打码相关配置到yundama.com申请注册
YUNDAMA_USERNAME = 'ruc_wenwen'
YUNDAMA_PASSWORD = ''
YUNDAMA_APP_ID = '3485'
YUNDAMA_APP_KEY = '9419694d4afb3f780a0b92825ff5ec03'

YUNDAMA_API_URL = 'http://api.yundama.com/api.php'


# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}
# 云打码最大尝试次数
YUNDAMA_MAX_RETRY = 20

# API地址和端口
API_HOST = '127.0.0.1'
API_PORT = 5000