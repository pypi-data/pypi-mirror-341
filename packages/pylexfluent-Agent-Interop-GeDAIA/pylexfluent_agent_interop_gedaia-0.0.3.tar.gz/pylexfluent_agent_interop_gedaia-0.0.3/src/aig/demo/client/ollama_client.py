

import json
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, GetPromptResult
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent

from langchain.prompts import PromptTemplate

from aig import load_model

# Définir un prompt template pour l'agent
prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    Vous êtes un agent intelligent capable de répondre aux questions et d'effectuer des tâches et utilisant exlusivement les outils mis à ta disposition.
    Vous ne pouvez répondre qu'en utilisant les outils fournis.
    Voici la requête de l'utilisateur : {query}
    """
)

async def agent_matheux(model_name:str) :
    """
    """
    # server_params = StdioServerParameters(
    #     command="python",
    #     # Make sure to update to the full absolute path to your math_server.py file
    #     args=["aig/demo/server/math_server.py"],
    # )  
     
    model:ChatOllama = load_model(base_url="https://models-ai.lexfluent.com",name=model_name, temperature=0.8)
    
    async with sse_client(url="http://localhost:8005/sse") as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # Get tools
            mcp_tools = await load_mcp_tools(session)
            # Get prompts 
            mcp_prompts= await session.list_prompts()            
            try:
                agent= create_react_agent(model, mcp_tools)
                custom_prompt:str=""
                for i,prompt in enumerate(mcp_prompts.prompts) :
                    print(f"{i+1}: prompt= {prompt.name} ({prompt.description})")                
                
                idx_prompt=input("Quel numéro de prompt voulez utiliser? ")
                idx = int(idx_prompt)
                if idx>0 and idx<=len(mcp_prompts.prompts) :
                    custom_prompt=mcp_prompts.prompts[idx-1].name
                    custom_arguments:list[PromptArgument] = mcp_prompts.prompts[idx-1].arguments
                print("Poser votre question \n")
            except Exception as ex:
                print(f"Exception: \n{ex}")
                return -1, ex 
            while True:
                current_context:dict[str,str]=dict()
                current_context["volumId"]="9-volum-123"
                current_context["documentId"]="8-document-123"
                texte="Climatisation monobloc sans groupe extérieur : Composé d'un seul bloc, le climatiseur monobloc rafraîchit l'air intérieur en y récupérant la chaleur pour la rejeter à l'extérieur via une gaine d'évacuation. Performants et silencieux, les climatiseurs monoblocs ont pour atout principal leur flexibilité : ne nécessitant pas de lourds travaux d'installation, elles sont faciles à intégrer et n'altèrent pas l'esthétique extérieure d'un bâtiment. Certaines climatisations monoblocs se font mobile, pour vous accompagner dans les différentes pièces de votre logement. Découvrez notre sélection de climatiseurs monoblocs de grandes marques !"
                question= input("Question: ")
                if question.lower()=="exit" : return 0
                try:
                    if mcp_prompts.prompts and custom_prompt!="" : 
                        promptResult:GetPromptResult = await session.get_prompt(
                            custom_prompt,
                            arguments={
                                custom_arguments[0].name:question,
                                custom_arguments[1].name:json.dumps(current_context)
                                })
                        if promptResult!=None :
                            for prompt in promptResult.messages:
                                question= prompt.content.text 
                                break
                            
                    response:dict = await agent.ainvoke({"messages": question})
                    if response !=None :
                        messages=response.get("messages",None)
                        if messages !=None :
                            for message in messages :
                                if message.name !=None : _name=message.name
                                else :  _name="GeDAIA"
                                print(f"=>\tType: {_name}({message.type})\n\t{message.content}\n")            
                        else : print('Aucune réponse retournée')
                    else : print("Aucune réponse du modèle")
                except Exception as ex:
                    print(f"Désolé mais une erreur est apparue :\n{ex}")


            