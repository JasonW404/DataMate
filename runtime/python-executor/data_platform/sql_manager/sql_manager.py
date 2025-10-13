# -- encoding: utf-8 --

import time
from random import uniform

from loguru import logger
from sqlalchemy import create_engine, inspect


class SQLManager:

    @staticmethod
    def create_connect(max_retries=5, base_delay=1):
        """
        连接到 MySQL 数据库，使用 SQLAlchemy 和 PyMySQL。
        :param max_retries: 最大重试次数
        :param base_delay: 基础时延
        :return: 返回 SQLAlchemy 连接对象
        """

        # todo 需要从环境变量中获取数据库配置
        connection_url = f"mysql+pymysql://root:Huawei%40123@101.201.105.190:9988/dataengine"

        attempt = 0

        while True:
            try:
                engine = create_engine(connection_url, pool_pre_ping=True)
                return engine.connect()
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed with error: {str(e)}")
                if attempt >= max_retries - 1:
                    raise
                wait_time = min(30, base_delay * (2 ** attempt))  # 不超过30秒的最大延时
                jitter = uniform(-wait_time / 4, wait_time / 4)  # 增加随机抖动因子
                time.sleep(wait_time + jitter)
                attempt += 1


if __name__ == "__main__":
    with SQLManager.create_connect() as connection:
      inspector = inspect(connection)
      print(inspector.get_table_names())

