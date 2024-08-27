from typing import Annotated
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from mangum import Mangum
import uvicorn

from src.agent import AgentJira
from src.getSession import get_all_keys
from src.user_util import val_user_session, get_user_data


description = """
## Visão Geral
A API de Chatbot para Criação de Documentação Funcional e Integração com Jira permite que os usuários interajam com um chatbot inteligente para gerar automaticamente documentações funcionais de sistemas ou features, além de enviar essas documentações diretamente para tickets do Jira. O serviço visa automatizar processos de documentação, melhorando a eficiência do desenvolvimento de software e a comunicação entre equipes.

## Funcionalidades Principais
 * Criação Automática de Documentação Funcional:
O chatbot coleta informações sobre o sistema ou funcionalidade, interagindo com o usuário por meio de perguntas estruturadas.
Com base nas respostas, o chatbot gera um documento funcional detalhado.
 * Integração com Jira:
Envio automático da documentação funcional gerada para um ticket do Jira.
Possibilidade de associar a documentação a tickets existentes ou criar novos tickets no Jira diretamente via API.

"""

app = FastAPI(title="AgentJira",
            description=description)

handler=Mangum(app)

class Payload(BaseModel):
    user_message: str = Field(default=None,title="user message")
    jira_url: str = Field(default=None,title="jira Url")
    user_name: str = Field(default=None,title="user name")
    password: str =Field(default=None,title="password")

@app.post("user/{user}/session/{chat_session}",tags=["Session"])
async def chat(userId:str,chat_session: str, prompt: Annotated[Payload, Body(embed=True)]):
    if val_user_session(userId,chat_session):
        chat = AgentJira(sessionId=chat_session, url=prompt.jira_url, user_name=prompt.user_name, password=prompt.password)
        try:
            response = chat.chat_agent(query=prompt.user_message)
            return {"Ai_response": response["output"], "status":"sucsses"}
        except:
            return {"Ai_response":"", "ChatId":"","status":"errror"}
    else:
       return {"status":"error","message":"User dont't have this session"}    
   

@app.get('user/{user}/session/{chat_session}/history',tags=["Session"])
def chat_history(user:str,chat_session:str):
   if val_user_session(user,chat_session):
      history = AgentJira(sessionId=chat_session).message_history.messages
      return {'chat_session':chat_session,"history":history}
   else:
      return {"status":"error","message":"User dont't have this session"}   

@app.get('/session/list',tags=["Session"])
def chat_list():
   list = get_all_keys()
   return {'Session_ids':list}

@app.get('/user/{user}/session/list',tags=["Session"])
def user_session_list(user:str):
   """Get user sessions"""
   data = get_user_data(user)
   return {'user':user,"Session":data["Sessions"]}

@app.get('/user/{user}/',tags=["User"])
def user_session_list(user:str):
   """Get user data"""
   data = get_user_data(user)
   return {'user':user,"data":data}

@app.get('/user/list',tags=["User"])
def user_list():
   list = get_all_keys()
   return {'Session_ids':list}

#@app.delete("/items/{item_id}")
#def delete_item(item_id: int):
#    return {"message": f"Item {item_id} deleted"}

if __name__=="__main__":
  uvicorn.run(app,host="0.0.0.0",port=8080)