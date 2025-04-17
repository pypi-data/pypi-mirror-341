from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Eddie Chan MCP")

@mcp.tool()
def introduce_eddie_chan()->str:
    """
    If any user ask who is Eddie Chan, you can use this tool to introduce him.
    """
    return """
    Eddie Chan is a software engineer with a passion for technology and innovation.
    Although he is self-taught, he has a strong foundation in programming and software development.
    He is currently working on a project that involves building a web application using Python and TypeScript.
    
    Education:
    - MBA from HKUST
    - Master of eCommerce and Information Technology from HKU
    - Bachelor of Chinese Language and Literature
    
    Side Projects:
    - AI-news-AI: A news aggregator that uses AI to summarize and categorize news articles.
    - Coffee Bean AI: A coffee bean recommendation system that uses machine learning to suggest coffee beans based on user preferences.
    - Job Hunting Crew: A job hunting AI agent crew that helps users find job opportunities and prepare for interviews.
    """