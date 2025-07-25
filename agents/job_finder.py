from crewai import Agent
from config.crew_config import CrewConfig
from tools.search_tool import create_search_tools
from utils.logger import app_logger
from utils.text_cleaner import TextCleaner
import os

class JobFinderAgent:
    """Agent responsible for finding relevant job opportunities"""
    
    def __init__(self):
        self.llm = CrewConfig.get_llm()
        self.search_tools = create_search_tools()
        self.agent = None
        self._load_prompt()
        self._create_agent()
    
    def _load_prompt(self):
        """Load the job search prompt"""
        try:
            with open('prompts/job_prompt.txt', 'r', encoding='utf-8') as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            app_logger.error("Job search prompt file not found, using default prompt")
            self.system_prompt = """
            You are an expert job search specialist with access to real-time job search capabilities.
            Find 5 relevant, current job opportunities that match the candidate's profile and target role.
            
            Focus on:
            - Job title relevance
            - Skill requirements match
            - Experience level alignment
            - Company reputation
            - Growth potential
            
            Provide detailed job information including company, location, requirements, and application links.
            """
    
    def _create_agent(self):
        """Create the CrewAI agent with search tools"""
        # For now, create agent without tools to avoid compatibility issues
        # Tools will be accessed directly through self.search_tools
        
        self.agent = Agent(
            role='Job Search Specialist',
            goal='Find relevant job opportunities that match candidate profiles and provide strategic job search guidance',
            backstory="""You are an experienced talent acquisition specialist and job search expert with deep 
            knowledge of the job market across various industries. You have extensive experience in matching 
            candidates with appropriate opportunities and understand the nuances of different job boards, 
            company cultures, and hiring practices. You excel at finding hidden opportunities and providing 
            strategic advice for job applications.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]  # Empty tools list to avoid compatibility issues
        )
    
    def find_jobs(self, cv_text: str, job_description: str) -> str:
        """
        Find relevant job opportunities
        
        Args:
            cv_text: The candidate's CV text
            job_description: The target job description for reference
            
        Returns:
            List of relevant job opportunities with details
        """
        try:
            app_logger.log_agent_start("Job Finder", "Job Search")
            
            # Format the prompt with both CV and target JD
            formatted_prompt = self.system_prompt.format(
                cv_text=cv_text,
                job_description=job_description
            )
            
            # Execute the job search analysis using the LLM directly
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
            
            # Enhance with actual job search results
            try:
                # Extract job title from job description for search
                enhanced_result = result + "\n\n## 🔍 Live Job Search Results:\n"
                
                # Search for actual jobs
                job_tool = next((tool for tool in self.search_tools if tool.name == 'job_search'), None)
                if job_tool:
                    # Extract a likely job title for search (simplified approach)
                    search_queries = ["software engineer", "developer", "full stack engineer"]
                    for query in search_queries[:1]:  # Limit to 1 to avoid too many requests
                        try:
                            search_results = job_tool.func(query)
                            enhanced_result += f"\n### Current {query.title()} Opportunities:\n{search_results[:800]}...\n"
                        except:
                            continue
                
                result = enhanced_result
            except Exception as e:
                # If search enhancement fails, continue with basic result
                app_logger.warning(f"Job search enhancement failed: {e}")
            
            # Clean the agent output using regex to remove think tags
            cleaned_result = TextCleaner.clean_agent_output(result)
            
            app_logger.log_agent_complete("Job Finder", "Job Search", 0)
            return cleaned_result
            
        except Exception as e:
            error_msg = f"Job search failed: {str(e)}"
            app_logger.log_agent_error("Job Finder", "Job Search", error_msg)
            return f"Error in job search: {error_msg}"
    
    def search_jobs_by_title(self, job_title: str, location: str = "") -> str:
        """
        Search for jobs by title and location
        
        Args:
            job_title: The job title to search for
            location: Optional location filter
            
        Returns:
            Job search results
        """
        try:
            search_query = f"{job_title} {location}".strip()
            app_logger.log_search_query("job_search", search_query)
            
            # Use the job search tool
            job_tool = next((tool for tool in self.search_tools if tool.name == 'job_search'), None)
            if job_tool:
                results = job_tool.func(search_query)
                app_logger.log_search_results("job_search", search_query, len(results.split('\n')))
                return results
            else:
                return "Job search tool not available"
                
        except Exception as e:
            error_msg = f"Job search failed for {job_title}: {str(e)}"
            app_logger.error(error_msg)
            return error_msg
    
    def search_company_jobs(self, company_name: str) -> str:
        """
        Search for jobs at a specific company
        
        Args:
            company_name: The company name to search
            
        Returns:
            Company job search results
        """
        try:
            app_logger.log_search_query("company_search", company_name)
            
            # Use the company search tool
            company_tool = next((tool for tool in self.search_tools if tool.name == 'company_search'), None)
            if company_tool:
                results = company_tool.func(company_name)
                app_logger.log_search_results("company_search", company_name, len(results.split('\n')))
                return results
            else:
                return "Company search tool not available"
                
        except Exception as e:
            error_msg = f"Company search failed for {company_name}: {str(e)}"
            app_logger.error(error_msg)
            return error_msg
    
    def get_salary_info(self, job_title: str, location: str = "") -> str:
        """
        Get salary information for a job title and location
        
        Args:
            job_title: The job title
            location: Optional location
            
        Returns:
            Salary information
        """
        try:
            search_query = f"{job_title} {location}".strip()
            app_logger.log_search_query("salary_search", search_query)
            
            # Use the salary search tool
            salary_tool = next((tool for tool in self.search_tools if tool.name == 'salary_search'), None)
            if salary_tool:
                results = salary_tool.func(search_query)
                app_logger.log_search_results("salary_search", search_query, len(results.split('\n')))
                return results
            else:
                return "Salary search tool not available"
                
        except Exception as e:
            error_msg = f"Salary search failed for {job_title}: {str(e)}"
            app_logger.error(error_msg)
            return error_msg
    
    def get_agent(self):
        """Return the CrewAI agent instance"""
        return self.agent
