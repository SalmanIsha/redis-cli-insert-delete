from rediscluster import RedisCluster

startup_nodes = [{"host": "192.168.3.31", "port": "6379"},{"host": "192.168.3.32", "port": "6380"},{"host": "192.168.3.33", "port": "6381"}]

# Note: decode_responses must be set to True when used with python3
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)


print(rc.keys("*"))
#To remove all data from cluster use below command
#print(rc.flushall())
#To save data forcefully to disk use below command
#print(rc.save())
