from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import json
import math
import _Script_Handler as SC
scriptHandler = SC._Script_Handler()

origins = [
    "http://127.0.0.1",
]

show_amount = 6

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/command={cmd}")
def commandHandler(cmd: int):
    try:
        scriptHandler.receiveCommand(cmd)
        return JSONResponse(content={"message": "success running script"}, status_code=200)
    except Exception as ex:
        return JSONResponse(content={"message": "error when running script"}, status_code=500)

@app.get("/page={pages}")
def pagination(pages: int):
    with open("config/menu.json") as json_file:
        json_data = json.load(json_file)
        amount = len(json_data["menu"])
        allPages = math.ceil(amount/show_amount)
        if pages > allPages or pages == 0:
            return JSONResponse(content={"message": "Not Found"}, status_code=404)
        else:
            toBe_sent = []
            index_start = ((int(pages) - 1) * show_amount)
            limit = (math.floor(pages/allPages) * amount%show_amount)
            if limit == 0:
                limit = show_amount
            for index in range(index_start, (index_start+limit)):
                toBe_sent.append(json_data["menu"][index])
            json_data = {
                "menu": toBe_sent,
                "pages": allPages
            }
            return JSONResponse(content=json_data, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3001)
    
