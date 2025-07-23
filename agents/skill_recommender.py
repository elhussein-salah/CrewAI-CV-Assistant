from crewai import Agent
from config.crew_config import CrewConfig
from tools.search_tool import create_search_tools
from utils.logger import app_logger
import os

class SkillRecommenderAgent:
    """Agent responsible for identifying skill gaps and recommending learning resources"""
    
    def __init__(self):
        self.llm = CrewConfig.get_llm()
        self.search_tools = create_search_tools()
        self.agent = None
        self._load_prompt()
        self._create_agent()
    
    def _load_prompt(self):
        """Load the skill recommendation prompt"""
        try:
            with open('prompts/skills_prompt.txt', 'r', encoding='utf-8') as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            app_logger.error("Skills prompt file not found, using default prompt")
            self.system_prompt = """
            You are an expert career development advisor specializing in skill gap analysis.
            Compare the CV with the job description to identify missing skills and recommend
            specific learning resources.
            
            Focus on:
            - Technical skill gaps
            - Soft skill development
            - Certification recommendations
            - Learning pathway suggestions
            
            Provide specific courses, tutorials, and resources with links when possible.
            """
    
    def _create_agent(self):
        """Create the CrewAI agent with search tools"""
        # For now, create agent without tools to avoid compatibility issues
        # Tools will be accessed directly through self.search_tools
        
        self.agent = Agent(
            role='Skill Development Advisor',
            goal='Identify skill gaps and recommend high-quality learning resources to bridge them',
            backstory="""You are a career development expert and learning specialist with deep knowledge 
            of online education platforms, certification programs, and skill development pathways. You have 
            helped countless professionals upskill and advance their careers by identifying precise skill gaps 
            and recommending the most effective learning resources tailored to their goals.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]  # Empty tools list to avoid compatibility issues
        )
    
    def recommend_skills(self, cv_text: str, job_description: str) -> str:
        """
        Analyze skill gaps and recommend learning resources
        
        Args:
            cv_text: The CV text to analyze
            job_description: The target job description
            
        Returns:
            Skill gap analysis and learning recommendations
        """
        try:
            app_logger.log_agent_start("Skill Recommender", "Skill Gap Analysis")
            
            # Format the prompt with both CV and JD
            formatted_prompt = self.system_prompt.format(
                cv_text=cv_text,
                job_description=job_description
            )
            
            # Execute the skill analysis
            result = self.agent.llm.invoke(formatted_prompt)
            
            # Enhance with search results for key skills
            try:
                # Extract potential skills that need development
                enhanced_result = result + "\n\n## 🔍 Additional Learning Resources:\n"
                
                # Search for learning resources for common skills
                learning_tool = next((tool for tool in self.search_tools if tool['name'] == 'learning_search'), None)
                if learning_tool:
                    # Sample skills to search for (in a real implementation, this would be extracted from the analysis)
                    sample_skills = ["Python", "React", "Machine Learning", "Data Analysis"]
                    for skill in sample_skills[:2]:  # Limit to 2 to avoid too many requests
                        try:
                            search_results = learning_tool['func'](skill)
                            enhanced_result += f"\n### {skill} Learning Resources:\n{search_results[:500]}...\n"
                        except:
                            continue
                
                result = enhanced_result
            except Exception as e:
                # If search enhancement fails, continue with basic result
                app_logger.warning(f"Search enhancement failed: {e}")
            
            app_logger.log_agent_complete("Skill Recommender", "Skill Gap Analysis", 0)
            return result
            
        except Exception as e:
            error_msg = f"Skill recommendation analysis failed: {str(e)}"
            app_logger.log_agent_error("Skill Recommender", "Skill Gap Analysis", error_msg)
            return f"Error in skill recommendation: {error_msg}"
    
    def search_learning_resources(self, skill: str) -> str:
        """
        Search for learning resources for a specific skill
        
        Args:
            skill: The skill to search learning resources for
            
        Returns:
            Learning resource search results
        """
        try:
            app_logger.log_search_query("learning_search", skill)
            
            # Use the learning search tool
            learning_tool = next((tool for tool in self.search_tools if tool['name'] == 'learning_search'), None)
            if learning_tool:
                results = learning_tool['func'](skill)
                app_logger.log_search_results("learning_search", skill, len(results.split('\n')))
                return results
            else:
                return "Learning search tool not available"
                
        except Exception as e:
            error_msg = f"Learning resource search failed for {skill}: {str(e)}"
            app_logger.error(error_msg)
            return error_msg
    
    def get_agent(self):
        """Return the CrewAI agent instance"""
        return self.agent
