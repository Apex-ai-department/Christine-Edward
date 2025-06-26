import redis

# Connect to cloud Redis (replace placeholders)
redis_client = redis.Redis(
    host='your-redis-host.com',  # From your token
    port=12345,                 # From your token
    password='your-redis-token', # From your token
    ssl=True                    # Usually required for cloud Redis
)
