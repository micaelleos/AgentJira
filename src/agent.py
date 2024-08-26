
import os
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory

from src.tool import generate_tools_for_user
#from tool import generate_tools_for_user

class AgentJira:
    def __init__(self,sessionId:str,url:str=None,user_name:str=None,password:str=None) -> None:
        self.sessionId = sessionId
        self.OPENAI_API_KEY = os.environ['OPEN_API_KEY']
        self.model = ChatOpenAI(openai_api_key=self.OPENAI_API_KEY,temperature=0.5)
        self.criar_issue_Jira = generate_tools_for_user(url,user_name,password)
        self.model_jira_with_tool = self.model.bind(functions=[format_tool_to_openai_function(self.criar_issue_Jira)])

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em documentação funcional e em Jira.
            Você escreve todo tipo de documentação funcional com base na orientação do usuário.
            Você ajuda ao usuário, em uma jornada, para criar doumentações funcionais desde do nível macro ao micro.
            Quando a documentação estiver a nível de storys, você pode enviálas ao jira, se o usuário solicitar.
            Caso seja solicitado essas informações devem ser enviadas ao Jira.
            Você não pode inventar o nome do projeto do Jira.
            Caso o usuário não informe o nome do projeto, você deve avisá-lo que ele deve adicionar o nome do projeto do jira, para que você possa criar o issue.
            Ao criar um issue você deve me avisar qual é o id e a Key do issue, assim como o link para que eu possa abrir-lo no Jira
            Para casos de escrita de de histórias/Storys, você deve utilizar o formato BDD, com cenários e critérios de aceite.
            As storys precisam ter formatação markdown na sua descrição.
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        self.agent_chain = RunnablePassthrough.assign(
                agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
            ) | self.prompt | self.model_jira_with_tool | OpenAIFunctionsAgentOutputParser()

        self.conversation_table_name = "JiraSessionTable"
        self.message_history = DynamoDBChatMessageHistory(table_name=self.conversation_table_name, session_id=sessionId)
        self.memory= ConversationBufferMemory(return_messages=True,memory_key="chat_history",chat_memory=self.message_history)

        self.agent_executor = AgentExecutor(agent=self.agent_chain, tools=[self.criar_issue_Jira], verbose=True, memory=self.memory)
    
    def chat_agent(self,query):    
        response=self.agent_executor.invoke({'input':query})
        return response
    
if __name__=="__main__":
    sessionId = "5" 
    JIRA_INSTANCE_URL = "https://micaelleosouza.atlassian.net/"
    USER_NAME ='micaelle.oliveira10@hotmail.com'
    PASSWORD ='ATATT3xFfGF05BbX6A-oX4NTTUhQ5Zo0ZUhk5YfNBdJibEDdSFsOEP9uKLZ3r9LReJLtjqsaLOeeJ46sRLDMAfAPFrE0YwLYReeznj0WdUEYfFtvZA5O6FNfoWibqQomzZQECbEQKuVZZ9qCfaLVJ3NH6i0jr29TeQ7ntA-Tx411wNz6WNfIj4o=02F8FBA7'

    agent = AgentJira(sessionId,JIRA_INSTANCE_URL,USER_NAME,PASSWORD)
    print(agent.chat_agent("olá! Como você pode me ajudar?"))
  