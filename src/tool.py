from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from langchain.agents import tool
from langchain_core.tools import StructuredTool,BaseTool
from atlassian import Jira


class IssueJira(BaseModel):
    project: str = Field(description="nome do projeto onde será criado o issue")
    title: str = Field(description="Nome do issue, em frase resumida com até 4 palavras")
    description: str = Field(description="descrição do issue.")
    issuetype: Literal['Task', 'Story', 'Epic'] =  Field(description="Tipo do issue a ser criado")
    #priority: Literal['Highest', 'High', 'Medium','Low','Lowest'] = Field(description="An issue's priority indicates its relative importance. ")


def generate_tools_for_user(JIRA_INSTANCE_URL: str,USER_NAME: str,PASSWORD: str) -> List[BaseTool]:
    """Generate a set of tools that have a user id associated with them."""

    @tool(args_schema=IssueJira)
    def criar_issue_Jira(**dict_info:IssueJira) -> dict:
        """Chame essa função para criar issues no Jira"""
        fields = {
            "project":
            {
                "key": dict_info["project"]
            },
            "summary": dict_info["title"],
            "description": dict_info["description"],
            "issuetype": {
                "name": dict_info["issuetype"]
            }
            }
        
        try:    # Create issue
            jira = Jira(
                url=JIRA_INSTANCE_URL,
                username=USER_NAME,
                password= PASSWORD,
                cloud=True)
            result = jira.issue_create(fields)
            print(result)
        except Exception as e:
            print(e)
            if type(e).__name__ in ['MissingSchema','NameError']:
                return "Aconteceu um erro ao enviar o issue ao Jira. O usuário não configurou as credenciais da sua conta do Jira"
            else:
                return f"Aconteceu o erro {type(e).__name__} ao enviar o issue ao Jira"
        
        return result
    
    return criar_issue_Jira

if __name__=="__main__":
    JIRA_INSTANCE_URL = "https://micaelleosouza.atlassian.net/"
    USER_NAME ='micaelle.oliveira10@hotmail.com'
    PASSWORD ='ATATT3xFfGF05BbX6A-oX4NTTUhQ5Zo0ZUhk5YfNBdJibEDdSFsOEP9uKLZ3r9LReJLtjqsaLOeeJ46sRLDMAfAPFrE0YwLYReeznj0WdUEYfFtvZA5O6FNfoWibqQomzZQECbEQKuVZZ9qCfaLVJ3NH6i0jr29TeQ7ntA-Tx411wNz6WNfIj4o=02F8FBA7'

    jiratool = generate_tools_for_user(JIRA_INSTANCE_URL,USER_NAME,PASSWORD)
    print(jiratool.args_schema.schema_json())