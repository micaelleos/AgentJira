from typing import Annotated
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from mangum import Mangum
import uvicorn

from src.agent import EBIagent
from src.getSession import get_all_keys


description = """

"""

app = FastAPI(title="",
            description=description)

handler=Mangum(app)

class Prompt(BaseModel):
    user_message: str = Field(default=None,title="user message")

@app.post("/session/{chat_session}")
async def chat(chat_session: str, prompt: Annotated[Prompt, Body(embed=True)]):
    chat = EBIagent(session_id=chat_session)
    try:
        response = chat.chat_agent(query=prompt.user_message)
    except:
       return {"Ai_response": "", "ChatId":"", "EBI":"","status":"errror"}
    
    ebi = get_ebi(chat_session)
    results = {"Ai_response": response["output"], "EBI": ebi, "status":"sucsses"}
    return results

@app.get('/session/{chat_session}/history')
def chat_history(chat_session:str):
   history = EBIagent(session_id=chat_session).message_history.messages
   return {'chat_session':chat_session,"history":history}

@app.get('/session/list')
def chat_list():
   list = get_all_keys()
   return {'Session_ids':list}

#@app.delete("/items/{item_id}")
#def delete_item(item_id: int):
#    return {"message": f"Item {item_id} deleted"}

if __name__=="__main__":
  uvicorn.run(app,host="0.0.0.0",port=8080)