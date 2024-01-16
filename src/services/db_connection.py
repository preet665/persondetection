"""
File : db_connection.py
Description : Class is responsible for Handling Redis-DataBase operations
Created on : 
Author :
E-mail :

"""
from src.constant.project_constant import Constant as constant 
from src.constant.global_data import GlobalData
from src.common.config_manager import cfg
import redis
import json

class RedisDatabaseHandler:
    def __init__(self):
        self.redis_conn = redis.StrictRedis(host=cfg.get_environment_config(constant.CONFIG_ENVIRONMENT_SERVER_IP),
                                             port=cfg.get_environment_config(constant.CONFIG_ENVIRONMENT_SERVER_PORT), db=cfg.get_environment_config(constant.CONFIG_ENVIRONMENT_DATABASE))
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        self.redis_conn.delete(constant.INFERENECE_METADATA_DB_TABLE)
        if not self.redis_conn.exists(constant.INFERENECE_METADATA_DB_TABLE):
            try:
                table_structure = GlobalData.inference_metadata
                #self.redis_conn.hmset(constant.INFERENECE_METADATA_DB_TABLE, table_structure)
                self.redis_conn.rpush(constant.INFERENECE_METADATA_DB_TABLE, json.dumps(table_structure))
        
            except Exception as e:
                print(f'Exception as: {e}')

    def insert_data(self, data):
        json_data = json.dumps(data)
        #self.redis_conn.hset(constant.INFERENECE_METADATA_DB_TABLE, 'frame_metadata', json_data)
        self.redis_conn.rpush(constant.INFERENECE_METADATA_DB_TABLE, json_data)
        #print(f'Data inserting in Redis')

    def get_data(self):
        # Retrieve and deserialize data from the specified table
        json_data = self.redis_conn.hget(constant.INFERENECE_METADATA_DB_TABLE, 'frame_metadata')
        if json_data:
            return json.loads(json_data.decode('utf-8'))
        else:
            return None

