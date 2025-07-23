from crewai import Agent
from config.crew_config import CrewConfig
from utils.logger import app_logger
import os

class CVImproverAgent:
    """Agent responsible for improving CV based on job description"""
    
    def __init__(self):
        self.llm = CrewConfig.get_llm()
        self.agent = None
        self._load_prompt()
        self._create_agent()
    
    def _load_prompt(self):
        """Load the CV improvement prompt"""
        try:
            with open('prompts/improve_prompt.txt', 'r', encoding='utf-8') as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            app_logger.error("CV improvement prompt file not found, using default prompt")
            self.system_prompt = """
            You are an expert CV improvement specialist. Analyze the provided CV against the job description
            and provide specific, actionable improvement suggestions.
            
            Focus on:
            - Keyword alignment with job requirements
            - Experience highlighting
            - Skills optimization
            - Achievement quantification
            - Structure improvements
            
            Provide specific rewrite suggestions with before/after examples.
            """
    
    def _create_agent(self):
        """Create the CrewAI agent"""
        self.agent = Agent(
            role='CV Improvement Specialist',
            goal='Optimize CVs for specific job opportunities by providing targeted improvement recommendations',
            backstory="""You are a professional CV writer and career coach with expertise in tailoring 
            CVs for specific job opportunities. You have helped thousands of candidates land their dream jobs 
            by optimizing their CVs for maximum impact. You understand how to highlight relevant experience, 
            integrate keywords naturally, and present achievements in the most compelling way.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
    
    def improve_cv(self, cv_text: str, job_description: str) -> str:
        """
        Provide CV improvement suggestions based on job description
        
        Args:
            cv_text: The CV text to improve
            job_description: The target job description
            
        Returns:
            Detailed improvement recommendations
        """
        try:
            app_logger.log_agent_start("CV Improver", "CV Optimization")
            
            # Format the prompt with both CV and JD
            formatted_prompt = self.system_prompt.format(
                cv_text=cv_text,
                job_description=job_description
            )
            
            # Execute the improvement analysis
            result = self.agent.llm.invoke(formatted_prompt)
            
            app_logger.log_agent_complete("CV Improver", "CV Optimization", 0)
            return result
            
        except Exception as e:
            error_msg = f"CV improvement analysis failed: {str(e)}"
            app_logger.log_agent_error("CV Improver", "CV Optimization", error_msg)
            return f"Error in CV improvement analysis: {error_msg}"
    
    def get_agent(self):
        """Return the CrewAI agent instance"""
        return self.agent
