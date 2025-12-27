import os
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langgraph.prebuilt import create_react_agent
# from langchain_classic.agent import AgentExecutor
# from langchain.agents import AgentExecutor

os.environ["OPENAI_API_KEY"] = "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"

@tool
def get_course_schedule(course_name: str) -> str:
    """
    Get the schedule for a given course."""
    
    schedule = {
        "ai architect mastery": "Mondays and Wednesdays, 6 PM - 8 PM",
        "data science bootcamp": "Tuesdays and Thursdays, 7 PM - 9 PM",
        "full stack development": "Saturdays, 10 AM - 4 PM",
    }
    key  = course_name.lower()
    return schedule.get(key, "Course not found.")

@tool
def calculate_discounted_price(original_price: float, discount_percentage: float) -> float:
    """
    Calculate the discounted price given the original price and discount percentage.
    """
    discount_amount = (discount_percentage / 100) * original_price
    discounted_price = original_price - discount_amount
    return round(discounted_price, 2)

@tool
def recommend_next(topic: str) -> str:
    """
    its a real life tool :which will help me out for next step recommendation for my learning path

    """
    t = topic.lower()
    if "python" in t:
        return (
            "next step for python is to learn web development using Django or Flask."
        )
    elif "data science" in t:
        return "next step for data science is to learn machine learning algorithms and their applications."
    elif "machine learning" in t:
        return "next step for machine learning is to learn deep learning and neural networks."
    else:
        return "Sorry, I don't have a recommendation for that topic."


tools = [get_course_schedule, calculate_discounted_price, recommend_next]
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful teaching assistant that helps students with learning paths and course-related queries.\n"
     "Use the tools to answer questions.\n"
     "Rules:\n"
     "1) If the question is about schedules/batches/timings, use get_course_schedule.\n"
     "2) If the question is about price/discount/GST/splits, use calc.\n"
     "3) If the question is about what to learn next, use recommend_next.\n"
     "4) If the user asks something outside these, respond:\n"
     "   'Sorry, I can only help with course schedules, discounted prices, and learning path recommendations.'\n"
     "If you use a tool, summarize the tool result in a human-readable way."
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

demo_query = "I am learning python, what should i learn next?"
response = executor.invoke({"input": demo_query})

demo_query = "tell me the schedule for AI Architect Mastery course"
response = executor.invoke({"input": demo_query})

