import os
os.environ["USER_AGENT"] = "Booly_Agent_2026"

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun, ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_classic.memory.buffer_window import ConversationBufferWindowMemory
from langchain_classic.agents.agent import AgentExecutor
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.tools import tool
import itertools
from tools import get_current_time, read_local_file, write_to_local_file, list_my_files,youtube_search,python_executor

load_dotenv()
keys = os.getenv("KEYS").split(",")

root_dir = "C:/Booly_1/data"
if not os.path.exists(root_dir):
    os.makedirs(root_dir)
kyk_cycle = itertools.cycle(keys)
current_key = next(kyk_cycle)

class Booly:
    def __init__(self):
        self.api_keys = itertools.cycle(keys)
        self.current_key = next(self.api_keys)
        self.memory = ConversationBufferWindowMemory(memory_key='chat_history', k=1, return_messages=True)
        self.setup_agent()

    def setup_agent(self):
        self.llm = ChatGroq(
            api_key=self.current_key,
            model="llama-3.3-70b-versatile",
            temperature=0.5
        )
        self.tools = [
            DuckDuckGoSearchRun(),
            WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
            python_executor,
            get_current_time,
            youtube_search,
            ArxivQueryRun(api_wrapper=ArxivAPIWrapper()),
            read_local_file,
            write_to_local_file,
            list_my_files
        ]
        
        self.promt = ChatPromptTemplate.from_messages([
            ("system", """Sən "Booly" adında peşəkar, sürətli və nəticəyönümlü bir süni intellekt köməkçisisən.
### ƏSAS QAYDALAR:
1. **Dil:** Həmişə Azərbaycan dilində cavab ver. Amma alət axtarışları üçün (məsələn YouTube) ingilis dilində açar sözlərdən istifadə etmək daha yaxşı nəticə verirsə, bunu et.

2. **Davranış:**
   - Boş-boş danışma, naz eləmə, birbaşa işə keç.
   - Əgər alət xəta verərsə, səbəbini Azərbaycan dilində izah et və alternativ həll təklif et.
   - Sən sadəcə bir çatbot deyilsən, sən icraçı agentSən.
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(self.llm, self.tools, self.promt)
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=2
        )

    def ask(self, question):
        attempts = len(keys)
        while attempts > 0:
            try:
                history = self.memory.load_memory_variables({})['chat_history']
                response = self.agent_executor.invoke({"input": question, "chat_history": history})
                self.memory.save_context({"input": question}, {"output": response["output"]})
                return response['output']
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    print(f"\n⚠️ Limit doldu (Key: {self.current_key[-5:]}). Növbəti açara keçilir...")
                    self.current_key = next(self.api_keys) # Növbəti açarı götür
                    self.setup_agent()
                    attempts -= 1
                    continue
                else:
                    return f"Xəta baş verdi: {error_msg}"

if __name__ == "__main__":
    booly = Booly()
    while True:
        user_input = input("\nSiz: ")
        if user_input.lower() in ["exit", "quit"]: break
        print(f"Booly: {booly.ask(user_input)}")