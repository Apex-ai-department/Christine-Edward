import redis

# Connect to cloud Redis (replace placeholders)
redis_client = redis.Redis(
    host='viable-ram-48359.upstash.io',  # From your token
    port=6379,                 # From your token
    password='AbznAAIjcDFlMGI2NDg3NDc1OWQ0YTZhOGI2MzQ0NzlmZTE3YTEwM3AxMA', # From your token
    ssl=True                    # Usually required for cloud Redis
)


#DEBUG
try:
    redis_client.ping()
    print("✅ Connected to Upstash Redis")
except Exception as e:
    print(f"❌ Connection failed: {e}")
