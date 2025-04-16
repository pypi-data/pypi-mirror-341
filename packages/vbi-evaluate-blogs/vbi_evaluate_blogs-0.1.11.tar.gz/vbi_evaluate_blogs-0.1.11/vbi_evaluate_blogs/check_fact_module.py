from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from playwright.sync_api import sync_playwright, Browser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests

# Load environment variables from a .env file
load_dotenv()

def draw_web_content_playwright(browser: Browser, url: str) -> str:
    with sync_playwright() as p:
        page = browser.new_page()
        page.goto(url)
        return page.content()
    
def searxng_search(query: str) -> str:
    """
    This function performs a search using the SearxNG search engine.

    Parameters:
    - query: The search query string.

    Functionality:
    1. Sends a GET request to the SearxNG API with the query and specified parameters.
    2. Extracts the top 10 search results from the API response.
    3. Formats the results into a readable string containing the title, URL, and content of each result.

    Returns:
    - A formatted string of search results or an error message if the search fails.
    """
    base_url = os.getenv("SEARXNG_URL")  # Base URL for the SearxNG instance
    params = {
        "q": query,  # Query string
        "format": "json",  # Response format
        "language": "en",  # Language for the search results
        "categories": "general"  # Search categories
    }

    try:
        # Send a GET request to the SearxNG API
        response = requests.get(f"{base_url}/search", params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response

        # Extract the top 5 results
        results = data.get("results", [])[:10]
        if not results:
            return "No relevant results found."  # Return a message if no results are found

        # Format the results into a readable string
        return "\n\n".join([f"{r['title']}\n{r['url']}\n{r['content']}" for r in results])

    except Exception as e:
        # Handle exceptions and return an error message
        return f"Error during search: {str(e)}"

def extract_claim(llm, content):
    """
    This function extracts claims from text content using a language model (LLM) and translates them into English.

    Parameters:
    - llm: The language model object used to process the content.
    - content: The text content from which claims need to be extracted.

    Functionality:
    1. Defines a prompt template to instruct the LLM to extract claims requiring verification and translate them into English.
    2. The prompt specifies that each claim should be listed on a separate line.
    3. Ensures the output contains only the necessary results without any explanations, symbols, or markings.
    4. Creates a processing chain that combines the prompt, the LLM, and an output parser.
    5. Invokes the chain with the provided content to extract and translate claims.

    Returns:
    - A string containing the extracted and translated claims, with each claim on a separate line.
    """
    # Define a prompt template for extracting and translating claims
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant specializing in extracting claims that need verification from a text and translating them into English."),
        ("user", "Extract a list of claims that need verification from the following content, translate each claim into English, and list them on separate lines. Only provide the necessary results without any explanations, symbols, or markings: {content}")
    ])
    chain = prompt | llm | StrOutputParser()  # Create a processing chain with the prompt, LLM, and output parser
    return str(chain.invoke({"content": content}))  # Invoke the chain with the provided content

# Function to perform fact-checking using the AzureChatOpenAI model
def check_fact(llm: AzureChatOpenAI , content: str) -> str:
    """
    This function performs fact-checking on a list of claims using a language model (LLM) and tools.

    Parameters:
    - llm: The AzureChatOpenAI language model used for processing.
    - claims: A string containing the claims to be fact-checked.

    Functionality:
    1. Defines two tools:
       - `search_tool`: Uses the SearxNG search engine to find relevant information.
       - `draw_tool`: Extracts detailed content from URLs if search results are insufficient.
    2. Binds the tools to the LLM for enhanced functionality.
    3. Constructs a detailed query for fact-checking, including instructions and guidelines.
    4. Creates an agent with the tools and query to process the claims.
    5. Executes the agent and returns the fact-checking results.

    Returns:
    - A string containing the fact-checking results in Markdown format.
    """

    claims = extract_claim(llm,content)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
    
    def tool_draw_with_playwright(url: str) -> str:
        return draw_web_content_playwright(browser,url)

    # Create a search tool using the SearxNG search function
    search_tool = Tool(
        name="search_tool",
        description="Search for factual information from the internet to verify the authenticity of statements.",
        func=searxng_search
    )

    draw_tool = Tool(
        name="draw_tool",
        description="Used to retrieve and extract the main content of a URL if search_tool does not provide sufficient information.",
        func=tool_draw_with_playwright
    )

    tools = [search_tool,draw_tool]

    # Define the query for fact-checking
    query = f"""
    <verification_task>
        <role>You are an assistant for fact-checking information.</role>
        <instruction>
            Use the tool <tool>search_tool</tool> to verify whether the statements below are <b>true or false</b>, 
            then <b>explain clearly</b> by <b>citing specific evidence from reliable sources</b>.
            If the information from <tool>search_tool</tool> is <b>not detailed enough</b> to draw a conclusion, you can use <tool>draw_tool</tool> to retrieve full content from any URL in the search results.
        </instruction>
        
        <tool_usage>
            <description>How to use <code>search_tool</code> and <code>draw_tool</code>:</description>

            <search>
                <tool><b>search_tool</b></tool> is used to find sources related to the statement to be verified.
                Returns a list of <code>results</code>, which can be reformatted as:
                <format>
                    "\\n\\n".join([f"r['title']\\nr['url']\\nr['content']" for r in results])
                </format>
            </search>

            <draw>
                <tool><b>draw_tool</b></tool> is used to extract detailed content from a webpage, based on a URL in the results of <code>search_tool</code>.
                Only use when the information from <code>search_tool</code> is <b>ambiguous, unclear, or too short</b> to draw a conclusion.
                For example, if <code>search_tool</code> only provides a title and a short description, but you need the original content to verify data or context, call <code>draw_tool</code> with the corresponding URL.
            </draw>
        </tool_usage>

        <guidelines>
            <step>1. If the statement contains <b>numbers, dates, names, or specific events</b>, prioritize verifying the <b>accuracy of those details</b>.</step>
            <step>2. If the statement does not contain specific numbers, verify the <b>overall accuracy of the content</b>.</step>
            <step>
                3. <b>Only use reliable sources</b>, for example:
                <sources>
                    <source>Official news websites (.vn, .com, .net, .org, .gov, .edu)</source>
                    <source>Government websites, international organizations, research institutes</source>
                    <source>Do not use Wikipedia or user-contributed sites</source>
                </sources>
            </step>
            <step>4. If <b>verification is not possible</b>, state clearly <i>Unable to verify</i> and explain why.</step>
        </guidelines>

        <note>
            When processing information related to time, note that the current date is April 2025.  
            For proper names, especially common or ambiguous ones, search with context or related information (such as organization, field, specific role) to ensure correct identification.
        </note>

        <output_format>
            Translate all the text in the results into Vietnamese before returning.
            For each statement, return the result in Markdown format:
            - **Statement:** The content to be verified
            - **Result:** ✅ True / ❌ False / ⚠️ Unable to verify
            - **Source:** (URL or name of a reliable source)
            - **Evidence:** (Specific citation from the source to explain the conclusion)
        </output_format>

        <example>
            - **Statement:** The Earth is flat.
            - **Result:** ❌ False
            - **Source:** https://www.nasa.gov/mission_pages/planetearth/shape
            - **Evidence:** According to NASA, satellite images show that the Earth is spherical, not flat.
        </example>

        <claims>
            <!-- Below is the list of statements to be verified, each statement on one line -->
            <insert_here>
                {claims}
            </insert_here>
        </claims>
    </verification_task>
    """

    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=False, 
        handle_parsing_errors=True,
        max_iterations=15
        )
    
    response = agent.invoke(query)
    markdown_output = response["output"]
    # print(markdown_output)
    return markdown_output

# Main function to execute the fact-checking
if __name__ == "__main__":

    from langchain_openai import AzureChatOpenAI
    import os

    # Initialize the AzureChatOpenAI model with API credentials and settings
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini", 
        api_version="2024-12-01-preview",
        # temperature=0.7,
        # max_tokens=16000
    )

    text="""
![](https://statics.gemxresearch.com/images/2025/04/09/160400/a-3d-render-of-a-pixar-style-cyberpunk-c_MgA2jR6QRoG4LMg9Y1m1Sw_ACcWep5XRhmU2SRVMLuXpg.jpeg)
 
# Doanh thu của nền tảng Virtuals Protocol sụt giảm mạnh xuống mức thấp kỷ lục 500 USD/ngày
 
Nền tảng tạo và kiếm tiền từ AI agent Virtuals Protocol đã chứng kiến doanh thu hàng ngày giảm mạnh xuống chỉ còn 500 USD khi nhu cầu về AI agent tiếp tục suy giảm."Có lẽ đây là một trong những biểu đồ  điên rồ nhất của chu kỳ này," nhà nghiên cứu Blockworks Sharples đã chia sẻ trong bài đăng trên X vào ngày 8 tháng 4. [Twitter Post](https://twitter.com/0xSharples/status/1909597333706232109) 
## Sự sụt giảm mạnh trong việc tạo AI agent
 
Sharples cho biết đã "khoảng một tuần" kể từ khi một đại lý AI mới được ra mắt trên Virtuals, so với cuối tháng 11 khi nền tảng này đang giúp tạo ra hơn 1.000 đại lý AI mới mỗi ngày, theo dữ liệu từ Dune Analytics.Vào ngày 2 tháng 1, khi token của Virtual Protocol (VIRTUAL) đạt mức cao kỷ lục 4,61 USD, dữ liệu của Blockworks cho thấy doanh thu hàng ngày của Virtuals đã tăng vọt lên trên 500.000 USD.Tuy nhiên, thời điểm đó dường như đánh dấu sự bắt đầu của xu hướng giảm, báo hiệu một đỉnh tiềm năng cho lĩnh vực đại lý AI. Sự suy giảm tiếp tục diễn ra ngay cả sau thông báo vào ngày 25 tháng 1 rằng dự án đã mở rộng sang Solana.Vào ngày 7 tháng 4, Sharples chỉ ra rằng Virtuals tạo ra "chưa đến 500 USD" doanh thu hàng ngày, với giá token giảm xuống mức thấp nhất là 0,42 USD.![](https://statics.gemxresearch.com/images/2025/04/09/154952/0196188f-6f21-7965-8e50-3a700d29.jpg)  Trước đó,[ Virtual đã có động thái mở rộng sang Solana](https://gfiresearch.net/post/virtuals-mo-rong-sang-he-sinh-thai-solana-thiet-lap-quy-du-tru-sol-chien-luoc) nhưng tình hình vẫn không mấy khả quan. 
## Tổng giá trị thị trường AI agent
 
Tổng giá trị thị trường đại lý AI là 153,81 triệu USD, theo Dune Analytics. Tuy nhiên, 76,6 triệu USD trong số đó được phân bổ cho AIXBT, công cụ phân tích tâm lý tiền mã hóa trên mạng xã hội X để nắm bắt xu hướng.AIXBT đã giảm 92% kể từ khi đạt mức cao kỷ lục 0,90 USD vào ngày 16 tháng 1. Tại thời điểm xuất bản, nó đang được giao dịch ở mức 0,07 USD, theo dữ liệu của CoinMarketCap.![](https://statics.gemxresearch.com/images/2025/04/09/155134/image.png)  Cộng tác viên chính của DeGen Capital, Mardo cho biết điều kiện thị trường hiện tại đã đóng vai trò trong sự suy giảm của Virtuals, nhưng nó cũng có thể liên quan đến các điều khoản mà Virtuals có với các nhà phát triển, chẳng hạn như "giữ lại thuế token mà các nền tảng khác tự do hoàn trả."Những khó khăn của Virtuals xảy ra trong bối cảnh toàn bộ thị trường tiền điện tử đang trải qua sự suy thoái cùng với thị trường tài chính toàn cầu, khi Tổng thống Hoa Kỳ Donald Trump tiếp tục tăng thuế quan và nỗi lo ngại gia tăng rằng điều đó có thể dẫn đến suy thoái kinh tế. 
## AI agent hiện tại bị đánh giá là "vô giá trị"
 
Tuy nhiên, nhiều người chỉ trích các đại lý AI vì thiếu chức năng. Nhà bình luận AI, BitDuke đã nói về sự suy giảm doanh thu của Virtuals: "Những kẻ ăn theo ChatGPT không còn thú vị nữa, dễ đoán mà."Nhà bình luận AI "DHH" đã nói trong bài đăng trên X vào ngày 8 tháng 4: "Tôi cũng tích cực về AI, nhưng bạn thật ảo tưởng nếu nghĩ rằng bất kỳ AI agent nào sẽ hoàn toàn thay thế một lập trình viên giỏi ngày nay. Ai biết về ngày mai, nhưng ngày đó chưa đến."Trong khi đó, người sáng lập Infinex Kain Warwick gần đây đã nói với tạp chí rằng AI có thể trở lại mặc dù "phiên bản đầu tiên của các AI agent lộn xộn" bị coi là "vô giá trị."
"""
    import time

    start_time = time.time()

    # Perform fact-checking and print the result
    print(check_fact(llm,text))

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")