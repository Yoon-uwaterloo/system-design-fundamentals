import redis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


r = redis.Redis(host="localhost", port=6379)
app = FastAPI()
MAX_REQUEST = 5
MAX_TIME = 60

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    current = r.get(ip)
    if current is None:
        r.set(ip, 1)
        r.expire(ip, MAX_TIME)
    else:
        current_count = int(current)
        if current_count >= MAX_REQUEST:
            return JSONResponse(
                status_code=429,
                content=
                {
                    "detail": "Too many requests",
                    "X-RateLimit-Limit": f"{MAX_REQUEST} per {MAX_TIME}s",
                    "X-RateLimit-Retry-After": str(r.ttl(ip))},
                headers=
                {
                    "X-RateLimit-Limit": f"{MAX_REQUEST} per {MAX_TIME}s",
                    "X-RateLimit-Retry-After": str(r.ttl(ip)),
                })

        r.incr(ip)
    remaining = MAX_REQUEST - int(r.get(ip))
    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response

@app.get("/")
async def get_ip(request: Request):
    ip = request.client.host 
    remaining = MAX_REQUEST - int(r.get(ip))
    return {"Hello!": "World", 
            "rate_limit": 
                {"remaining": remaining,
                 "limit": f"{MAX_REQUEST} per {MAX_TIME}s",}}