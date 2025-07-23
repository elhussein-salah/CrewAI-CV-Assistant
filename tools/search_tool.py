from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
import re

class SearchTool:
    """Enhanced search tool for job hunting and learning resources"""
    
    def __init__(self):
        self.ddg_search = DuckDuckGoSearchRun()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_jobs(self, query: str, max_results: int = 5) -> str:
        """Search for job opportunities using multiple strategies"""
        try:
            # Job-specific search queries
            job_queries = [
                f"{query} site:linkedin.com/jobs",
                f"{query} site:indeed.com",
                f"{query} site:glassdoor.com",
                f"{query} remote jobs",
                f'"{query}" hiring 2024'
            ]
            
            all_results = []
            
            for job_query in job_queries[:3]:  # Limit to avoid rate limiting
                try:
                    results = self.ddg_search.run(job_query)
                    all_results.append(f"Search: {job_query}\nResults: {results}\n")
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    all_results.append(f"Search failed for {job_query}: {str(e)}\n")
            
            return "\n".join(all_results)
            
        except Exception as e:
            return f"Job search failed: {str(e)}"
    
    def search_learning_resources(self, skill: str) -> str:
        """Search for learning resources for a specific skill"""
        try:
            learning_queries = [
                f"{skill} tutorial coursera udemy",
                f"learn {skill} free course",
                f"{skill} certification course",
                f"{skill} youtube tutorial playlist",
                f"best {skill} learning resources 2024"
            ]
            
            all_results = []
            
            for query in learning_queries[:3]:  # Limit queries
                try:
                    results = self.ddg_search.run(query)
                    all_results.append(f"Learning search: {query}\nResults: {results}\n")
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    all_results.append(f"Learning search failed for {query}: {str(e)}\n")
            
            return "\n".join(all_results)
            
        except Exception as e:
            return f"Learning resource search failed: {str(e)}"
    
    def search_company_info(self, company: str) -> str:
        """Search for company information and current openings"""
        try:
            company_query = f"{company} careers jobs hiring 2024"
            results = self.ddg_search.run(company_query)
            return f"Company search for {company}:\n{results}"
        except Exception as e:
            return f"Company search failed: {str(e)}"
    
    def search_salary_info(self, job_title: str, location: str = "") -> str:
        """Search for salary information"""
        try:
            salary_query = f"{job_title} salary {location} 2024 glassdoor"
            results = self.ddg_search.run(salary_query)
            return f"Salary search for {job_title} {location}:\n{results}"
        except Exception as e:
            return f"Salary search failed: {str(e)}"

def create_search_tools():
    """Create search tools for CrewAI agents"""
    search_tool = SearchTool()
    
    # Create simple function-based tools instead of LangChain Tool objects
    # to avoid compatibility issues with CrewAI
    
    def job_search_func(query: str) -> str:
        """Search for job opportunities"""
        return search_tool.search_jobs(query)
    
    def learning_search_func(skill: str) -> str:
        """Search for learning resources"""
        return search_tool.search_learning_resources(skill)
    
    def company_search_func(company: str) -> str:
        """Search for company information"""
        return search_tool.search_company_info(company)
    
    def salary_search_func(query: str) -> str:
        """Search for salary information"""
        parts = query.split()
        job_title = " ".join(parts[:-1]) if len(parts) > 1 else query
        location = parts[-1] if len(parts) > 1 else ""
        return search_tool.search_salary_info(job_title, location)
    
    # Return simple tool objects
    tools = [
        {'name': 'job_search', 'func': job_search_func, 'description': 'Search for job opportunities'},
        {'name': 'learning_search', 'func': learning_search_func, 'description': 'Search for learning resources'},
        {'name': 'company_search', 'func': company_search_func, 'description': 'Search for company information'},
        {'name': 'salary_search', 'func': salary_search_func, 'description': 'Search for salary information'}
    ]
    
    return tools
