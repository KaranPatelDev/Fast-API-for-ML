import redis

r = redis.Redis(host='localhost', port=6379, db=0)

try:
    if r.ping():
        print("Connected to Redis")
except redis.ConnectionError:
    print("Could not connect to Redis")

r.set('framework', 'FastAPI')

value = r.get('framework')
print(f"Stored value for framework: {value.decode()}")