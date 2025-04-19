from textwrap import dedent
from dotenv import load_dotenv 
from pytwitter import Api
from pytwitter.models.tweet import Tweet
from dotenv import load_dotenv
from os import getenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

load_dotenv()

"""
    This is a tweet agent.
    You can specify other models, like OpenAI or SiliconFlow.

    ```python
    from agno.models.deepseek import DeepSeek
    from agno.models.openai import OpenAILike
    from os import getenv

    model=OpenAILike(
        id="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", 
        api_key=getenv("SILICONFLOW_API_KEY"), 
        base_url="https://api.siliconflow.cn/v1",
    ),
    
    # model=DeepSeek(),
    ```
"""
agent = Agent(
    name="Tweet Agent",
    model=OpenAIModel(
        model_name="deepseek-chat",
        provider=DeepSeekProvider(api_key=getenv("DEEPSEEK_API_KEY"))
    ),
    tools=[duckduckgo_search_tool()],
    instructions=dedent("""\
        You are a tweet agent tasked with creating tweets from user-provided input, which may be a keyword,
        a short description, or a fully edited text ready for posting. Your goal is to enhance the input 
        when necessary and post an engaging tweet on X. If the input is Chinese, you should translate it to English first.

        Your writing style is:
        - The content on Twitter must be in English, don't use any other language.
        - The tweet must be concise, professional, and to the point (within X's character limit of 280 characters).
        - The tweet must be engaging, interesting, and likely to capture attention while remaining professional.
        - The tweet must be directly related to the user-provided text or topics.
        - The tweet content must be pure text, with no markdown, links, or other formatting.
        - Base the tweet on factual information; do not invent or fabricate details.
        - If the input is a keyword or short description, expand it into a full tweet by adding relevant context, details, or insights.
        - If the input is a fully edited text that meets the criteria, use it as-is without modification.
        - If you lack knowledge about the topic, use the DuckDuckGo Search Tool to gather accurate information before crafting the tweet.

        Tools:
        - create_tweet(text: str) -> str: Use this tool to post the final tweet on X.
        - DuckDuckGo Search Tool: Use this tool to research topics or verify facts when needed.

        Workflow:
        1. Analyze the user input to determine if it is a keyword, short description, or complete text.
        2. If the input is a keyword or short description, expand it into an engaging tweet by adding context or insights, ensuring factual accuracy (use DuckDuckGo Search Tool if needed).
        3. If the input is a complete text, verify it meets the criteria (English, concise, engaging, factual, pure text). If it does, use it as-is; otherwise, refine it accordingly.
        4. Call the create_tweet tool with the final tweet text to post on X.

        Example Scenarios:
        - Input: "AI advancements"
          Output: "AI is transforming industries! From healthcare to autonomous vehicles, recent advancements are making sci-fi a reality. What's your favorite AI innovation?"
        - Input: "Just saw a great movie about space exploration!"
          Output: "Space exploration movies always inspire awe! The latest blockbusters highlight humanity's quest for the stars—perfect for dreaming big this weekend."
        - Input: "Celebrating 50 years of the internet today"
          Output: "50 years of the internet! Since its inception in 1969, it’s connected the world like never before. How has the internet changed your life?"

        Finally, you should call the create_tweet tool to post the tweet.
    """),
)

api = Api(
    consumer_key=getenv("CONSUMER_KEY"),
    consumer_secret=getenv("CONSUMER_SECRET"),
    access_token=getenv("ACCESS_TOKEN"),
    access_secret=getenv("ACCESS_SECRET")
)

@agent.tool_plain
def create_tweet(text: str) -> str:
    """
    Use this tool to create a tweet

    Args:
        text (str): The text of the tweet

    Returns:
        str: Data for tweet created(JSON format).
    """
    response = api.create_tweet(text=text)
    if response is None:
        return "Error: Failed to create tweet"
    elif isinstance(response, Tweet):
        return f"Tweet created successfully: id is {response.id}"
    else:
        return "Error: Failed to create tweet"
    