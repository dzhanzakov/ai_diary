from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class TranscriberCrew():
    """Transcriber crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
   
    @agent
    def diary_ai_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['diary_ai_agent'], 
            verbose=True
        )

    @task
    def diary_summarization_task(self) -> Task:
        return Task(
            config=self.tasks_config['diary_summarization_task'], # type: ignore[index]
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Transcriber crew"""
        

        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
