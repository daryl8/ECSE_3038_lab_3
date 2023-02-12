from fastapi import FastAPI, Request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
import motor.motor_asyncio
import pydantic


app = FastAPI()

orgins = [
    "http://localhost:8000", 
    "https://ecse3038-lab3-tester.netlify.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://daryl8:IEM5i03xwbwGFaAi@cluster0.9mesohm.mongodb.net/?retryWrites=true&w=majority")
db = client.water_tank

pydantic.json.ENCODERS_BY_TYPE[ObjectId]= str

@app.post ("/profile")
async def create_new_profile(request: Request):
    profile_object = await request.json()
    new_profile = await db["profile"].insert_one(profile_object)
    created_profile = await db["profile"].find_one ({"_id": new_profile.inserted_id})

    return created_profile


@app.get("/profile")
async def get_all_profiles():
    prof = await db["profile"].find().to_list(999)
    return prof

