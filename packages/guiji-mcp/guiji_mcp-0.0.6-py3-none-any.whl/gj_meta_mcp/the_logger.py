import logging

# 配置日志基本设置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建一个logger实例
logger = logging.getLogger(__name__)

# 创建一个文件处理器，并指定日志文件的路径
file_handler = logging.FileHandler('gj_meta.log', encoding='utf-8')  # 日志文件名为log.txt，路径为当前目录
file_handler.setLevel(logging.INFO)  # 设置文件处理器的日志级别

# 创建一个格式化器，并将其应用到文件处理器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到logger中
logger.addHandler(file_handler)