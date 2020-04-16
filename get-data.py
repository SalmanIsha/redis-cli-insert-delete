from rediscluster import RedisCluster

startup_nodes = [{"host": "192.168.3.31", "port": "6379"},{"host": "192.168.3.32", "port": "6380"},{"host": "192.168.3.33", "port": "6381"}]

# Note: decode_responses must be set to True when used with python3
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)


print(rc.keys("*"))
#print(rc.flushall())
