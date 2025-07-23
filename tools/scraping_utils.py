import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re

class WebScraper:
    """Utility class for web scraping job-related content"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def extract_job_details(self, url: str) -> Dict[str, str]:
        """Extract job details from a job posting URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generic job detail extraction
            job_details = {
                'title': self._extract_title(soup),
                'company': self._extract_company(soup),
                'location': self._extract_location(soup),
                'description': self._extract_description(soup),
                'requirements': self._extract_requirements(soup),
                'salary': self._extract_salary(soup)
            }
            
            return {k: v for k, v in job_details.items() if v}
            
        except Exception as e:
            return {'error': f"Failed to scrape {url}: {str(e)}"}
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract job title from various possible selectors"""
        selectors = [
            'h1',
            '[data-testid="job-title"]',
            '.job-title',
            '.jobTitle',
            'h1.jobTitle',
            '.title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def _extract_company(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract company name"""
        selectors = [
            '[data-testid="company-name"]',
            '.company-name',
            '.companyName',
            '.employer',
            '[data-testid="employer-name"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def _extract_location(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract job location"""
        selectors = [
            '[data-testid="job-location"]',
            '.location',
            '.jobLocation',
            '[data-testid="location"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract job description"""
        selectors = [
            '[data-testid="job-description"]',
            '.job-description',
            '.jobDescription',
            '.description',
            '#job-description'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Get text and clean it up
                text = element.get_text(separator='\n', strip=True)
                return ' '.join(text.split())[:1000]  # Limit length
        return None
    
    def _extract_requirements(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract job requirements"""
        # Look for common requirement section keywords
        requirement_keywords = ['requirements', 'qualifications', 'skills', 'experience']
        
        for keyword in requirement_keywords:
            # Find headings containing the keyword
            headings = soup.find_all(['h2', 'h3', 'h4', 'strong'], 
                                   string=re.compile(keyword, re.IGNORECASE))
            
            for heading in headings:
                # Get the next sibling elements (usually ul, ol, or div)
                next_element = heading.find_next_sibling(['ul', 'ol', 'div', 'p'])
                if next_element:
                    text = next_element.get_text(separator='\n', strip=True)
                    return ' '.join(text.split())[:500]  # Limit length
        
        return None
    
    def _extract_salary(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract salary information"""
        selectors = [
            '[data-testid="salary"]',
            '.salary',
            '.compensation',
            '.pay'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Look for salary patterns in text
        salary_pattern = r'\$[\d,]+(?:\s*-\s*\$[\d,]+)?(?:\s*per\s+year|/year|annually)?'
        text = soup.get_text()
        salary_match = re.search(salary_pattern, text, re.IGNORECASE)
        if salary_match:
            return salary_match.group()
        
        return None
    
    def extract_learning_resource_info(self, url: str) -> Dict[str, str]:
        """Extract information from learning resource URLs"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            resource_info = {
                'title': self._extract_course_title(soup),
                'provider': self._extract_provider(soup),
                'duration': self._extract_duration(soup),
                'rating': self._extract_rating(soup),
                'price': self._extract_price(soup),
                'description': self._extract_course_description(soup)
            }
            
            return {k: v for k, v in resource_info.items() if v}
            
        except Exception as e:
            return {'error': f"Failed to scrape learning resource {url}: {str(e)}"}
    
    def _extract_course_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course title"""
        selectors = ['h1', '.course-title', '.title', 'h1.course-title']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def _extract_provider(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course provider"""
        # Check URL for known providers
        domain = urlparse(soup.find('link', {'rel': 'canonical'})['href'] if soup.find('link', {'rel': 'canonical'}) else '').netloc
        
        providers = {
            'coursera.org': 'Coursera',
            'udemy.com': 'Udemy',
            'edx.org': 'edX',
            'youtube.com': 'YouTube',
            'pluralsight.com': 'Pluralsight',
            'linkedin.com': 'LinkedIn Learning'
        }
        
        for domain_key, provider in providers.items():
            if domain_key in domain:
                return provider
        
        return None
    
    def _extract_duration(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course duration"""
        duration_pattern = r'(\d+(?:\.\d+)?)\s*(hour|hr|minute|min|week|month|day)s?'
        text = soup.get_text()
        duration_match = re.search(duration_pattern, text, re.IGNORECASE)
        if duration_match:
            return duration_match.group()
        return None
    
    def _extract_rating(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course rating"""
        rating_selectors = ['.rating', '.stars', '.score']
        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element:
                rating_text = element.get_text(strip=True)
                rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                if rating_match:
                    return rating_match.group()
        return None
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course price"""
        price_pattern = r'\$\d+(?:\.\d{2})?|free|Free'
        text = soup.get_text()
        price_match = re.search(price_pattern, text, re.IGNORECASE)
        if price_match:
            return price_match.group()
        return None
    
    def _extract_course_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract course description"""
        selectors = ['.description', '.course-description', '.about', '.overview']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator=' ', strip=True)
                return ' '.join(text.split())[:300]  # Limit length
        return None
    
    def rate_limit_delay(self):
        """Add random delay to avoid rate limiting"""
        time.sleep(random.uniform(1, 3))
