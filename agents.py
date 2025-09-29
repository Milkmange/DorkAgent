from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

def agents(llm) -> list:
    """Create and configure CrewAI agents."""

    searcher = Agent(
        role="searcher",
        goal="Performing advanced Google searches using Google Dorks",
        backstory="An expert in Google Dorking techniques for information gathering",
        verbose=True,
        tools=[SerperDevTool()],
        llm=llm,
    )

    bughunter = Agent(
        role="bughunter",
        goal="Identifying attack surfaces and vulnerabilities in target domains",
        backstory="A skilled penetration tester specializing in web security and vulnerability assessments",
        verbose=True,
        tools=[ScrapeWebsiteTool()],
        llm=llm,
    )

    writer = Agent(
        role="writer",
        goal="Generating well-structured and detailed reports based on findings",
        backstory="A technical writer specializing in cybersecurity documentation and structured reporting",
        verbose=True,
        llm=llm,
    )

    return [searcher, bughunter, writer]