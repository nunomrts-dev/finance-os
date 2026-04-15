import time
from collections import defaultdict
from fastapi import Request, HTTPException, status

request_counts = defaultdict(list)

RATE_LIMIT = 5
WINDOW_SECONDS = 60

async def rate_limit_middleware(request: Request, call_next):
    if request.url.path in ["/auth/login", "/auth/register"]:
        client_ip = request.client.host
        now = time.time()
        request_counts[client_ip] = [
            t for t in request_counts[client_ip]
            if now - t < WINDOW_SECONDS
        ]
        if len(request_counts[client_ip]) >= RATE_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        request_counts[client_ip].append(now)
    return await call_next(request)