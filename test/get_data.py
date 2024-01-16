import redis
import json

class RedisDataFetcher:
    def __init__(self):
        self.redis_conn = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0)
        self.table_name = "inference_metadata"

    def get_all_data(self):
        data_list = self.redis_conn.lrange(self.table_name, 0, -1)
        return [json.loads(item.decode('utf-8')) for item in data_list]

if __name__ == "__main__":
    # Initialize the RedisDataFetcher
    redis_fetcher = RedisDataFetcher()

    # Retrieve all inserted data from the Redis list
    all_data = redis_fetcher.get_all_data()

    # Print the retrieved data
    for data in all_data:
        print(data)
