from crewai import Agent
from langchain.tools import Tool
from config.crew_config import CrewConfig
from utils.logger import app_logger
from utils.text_cleaner import TextCleaner
import os

class CVEvaluatorAgent:
    """Agent responsible for evaluating CV for ATS compatibility and scoring"""
    
    def __init__(self):
        self.llm = CrewConfig.get_llm()
        self.agent = None
        self._load_prompt()
        self._create_agent()
    
    def _load_prompt(self):
        """Load the ATS evaluation prompt"""
        try:
            with open('prompts/ats_prompt.txt', 'r', encoding='utf-8') as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            app_logger.error("ATS prompt file not found, using default prompt")
            self.system_prompt = """
            You are an expert CV/Resume evaluator specializing in ATS compatibility.
            Analyze the provided CV and give an ATS score from 0-100, along with detailed feedback
            on formatting, keywords, and overall quality.
            
            Provide specific, actionable recommendations for improvement.
            """
    
    def _create_agent(self):
        """Create the CrewAI agent"""
        self.agent = Agent(
            role='CV Evaluator Specialist',
            goal='Analyze and evaluate CVs for ATS compatibility, providing detailed scoring and improvement recommendations',
            backstory="""You are an experienced recruiter and ATS systems expert with over 10 years 
            of experience in talent acquisition. You understand exactly what makes a CV pass through 
            ATS filters and catch recruiter attention. You have deep knowledge of industry standards, 
            keyword optimization, and formatting best practices.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
    
    def evaluate_cv(self, cv_text: str) -> str:
        """
        Evaluate CV for ATS compatibility
        
        Args:
            cv_text: The CV text to evaluate
            
        Returns:
            Detailed evaluation results
        """
        try:
            app_logger.log_agent_start("CV Evaluator", "ATS Evaluation")
            
            # Format the prompt with CV text
            formatted_prompt = self.system_prompt.format(cv_text=cv_text)
            
            # Execute the evaluation using the LLM directly
            try:
                # Try different methods based on LLM version
                if hasattr(self.llm, 'invoke'):
                    result = self.llm.invoke(formatted_prompt)
                elif hasattr(self.llm, '__call__'):
                    result = self.llm(formatted_prompt)
                elif hasattr(self.llm, 'generate'):
                    result = self.llm.generate([formatted_prompt]).generations[0][0].text
                else:
                    # Fallback to string conversion
                    result = str(self.llm.invoke(formatted_prompt))
            except Exception as llm_error:
                # Fallback method
                result = f"LLM invocation failed: {llm_error}. Using fallback analysis."
            
            # Clean the agent output using regex to remove think tags
            cleaned_result = TextCleaner.clean_agent_output(result)
            
            app_logger.log_agent_complete("CV Evaluator", "ATS Evaluation", 0)
            return cleaned_result
            
        except Exception as e:
            error_msg = f"CV evaluation failed: {str(e)}"
            app_logger.log_agent_error("CV Evaluator", "ATS Evaluation", error_msg)
            return f"Error in CV evaluation: {error_msg}"
    
    def get_agent(self):
        """Return the CrewAI agent instance"""
        return self.agent
