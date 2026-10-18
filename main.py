from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_3qtvdjbl4107sc6kmji4bnol"
EMAIL = "24f3005093@ds.study.iitm.ac.in"   # <-- put your exam-site email here


@app.post("/analytics")
async def analytics(request: Request):
    if request.headers.get("x-api-key") != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    body = await request.json()
    events = body.get("events", [])

    total_events = len(events)
    unique_users = len({e["user"] for e in events})

    revenue = 0.0
    per_user = {}
    for e in events:
        amount = e["amount"]
        if amount > 0:
            revenue += amount
            per_user[e["user"]] = per_user.get(e["user"], 0) + amount

    top_user = max(per_user, key=per_user.get) if per_user else None

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": round(revenue, 2),
        "top_user": top_user,
    }