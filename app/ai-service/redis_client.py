# ai_service/redis_client.py
import redis

# Initialize Redis client
redis_client = redis.Redis(
    host='localhost',  # Replace with Redis server IP
    port=6379,
    db=0,
    decode_responses=True  # Auto-convert bytes to strings
)

# Test connection
try:
    redis_client.ping()
    print("✅ Redis connected")
except Exception as e:
    print(f"❌ Redis connection failed: {e}")
