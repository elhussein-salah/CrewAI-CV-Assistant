import re
from typing import List, Dict

class TextCleaner:
    """Utility class for cleaning and processing text data"""
    
    @staticmethod
    def clean_cv_text(text: str) -> str:
        """
        Clean CV text by removing extra whitespace, formatting artifacts
        
        Args:
            text: Raw CV text
            
        Returns:
            Cleaned CV text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and line breaks
        text = re.sub(r'\s+', ' ', text)
        
        # Remove multiple consecutive periods or dashes
        text = re.sub(r'[.\-_]{3,}', '', text)
        
        # Remove page numbers and formatting artifacts
        text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d+/\d+', '', text)
        
        # Clean up common PDF extraction artifacts
        text = re.sub(r'[^\w\s@.,:()\-/&%$#]', '', text)
        
        # Normalize spacing around punctuation
        text = re.sub(r'\s+([,.;:])', r'\1', text)
        text = re.sub(r'([,.;:])\s*', r'\1 ', text)
        
        return text.strip()
    
    @staticmethod
    def clean_job_description(text: str) -> str:
        """
        Clean job description text
        
        Args:
            text: Raw job description text
            
        Returns:
            Cleaned job description text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML tags if present
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Clean up bullet points and special characters
        text = re.sub(r'[•·‣⁃▪▫◦‧⁌⁍]', '-', text)
        
        return text.strip()
    
    @staticmethod
    def extract_skills_from_text(text: str) -> List[str]:
        """
        Extract potential skills from text using pattern matching
        
        Args:
            text: Text to extract skills from
            
        Returns:
            List of potential skills
        """
        # Common skill patterns
        skill_patterns = [
            # Programming languages
            r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|Go|Rust|Swift|Kotlin|PHP|Ruby|Scala|R|MATLAB)\b',
            # Web technologies
            r'\b(?:React|Angular|Vue|HTML|CSS|Node\.js|Express|Django|Flask|Spring|Laravel)\b',
            # Databases
            r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Oracle|SQL Server|SQLite)\b',
            # Cloud platforms
            r'\b(?:AWS|Azure|Google Cloud|GCP|Docker|Kubernetes|Terraform|Jenkins)\b',
            # Tools and frameworks
            r'\b(?:Git|GitHub|GitLab|Jira|Confluence|Slack|Figma|Photoshop|Excel)\b'
        ]
        
        skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)
        
        # Remove duplicates and convert to proper case
        skills = list(set([skill.title() for skill in skills]))
        
        return skills
    
    @staticmethod
    def extract_experience_years(text: str) -> int:
        """
        Extract years of experience from text
        
        Args:
            text: Text to extract experience from
            
        Returns:
            Number of years of experience (0 if not found)
        """
        # Patterns for extracting years of experience
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
            r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in\s*\w+'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return 0
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        """
        Extract contact information from CV text
        
        Args:
            text: CV text
            
        Returns:
            Dictionary with contact information
        """
        contact_info = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Phone pattern (various formats)
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{10,15}'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group()
                break
        
        # LinkedIn profile
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin\.com/profile/view\?id=)([A-Za-z0-9\-]+)'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = f"linkedin.com/in/{linkedin_match.group(1)}"
        
        # GitHub profile
        github_pattern = r'(?:github\.com/)([A-Za-z0-9\-]+)'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact_info['github'] = f"github.com/{github_match.group(1)}"
        
        return contact_info
    
    @staticmethod
    def extract_education(text: str) -> List[str]:
        """
        Extract education information from CV text
        
        Args:
            text: CV text
            
        Returns:
            List of education entries
        """
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'degree',
            'university', 'college', 'institute', 'school',
            'b.s.', 'm.s.', 'b.a.', 'm.a.', 'mba', 'certification'
        ]
        
        education_entries = []
        
        # Split text into lines and look for education-related content
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                # Try to get context (current line + next 1-2 lines)
                context_lines = lines[i:i+3]
                education_entry = ' '.join(context_lines).strip()
                if len(education_entry) > 10:  # Filter out very short entries
                    education_entries.append(education_entry[:200])  # Limit length
        
        return education_entries
    
    @staticmethod
    def standardize_text(text: str) -> str:
        """
        Standardize text formatting for consistent processing
        
        Args:
            text: Input text
            
        Returns:
            Standardized text
        """
        if not text:
            return ""
        
        # Convert to lowercase for processing
        text = text.lower()
        
        # Standardize common variations
        replacements = {
            'javascript': 'javascript',
            'js': 'javascript',
            'typescript': 'typescript',
            'ts': 'typescript',
            'reactjs': 'react',
            'react.js': 'react',
            'nodejs': 'node.js',
            'node': 'node.js',
            'postgresql': 'postgresql',
            'postgres': 'postgresql',
            'mongodb': 'mongodb',
            'mongo': 'mongodb'
        }
        
        for old, new in replacements.items():
            text = re.sub(rf'\b{old}\b', new, text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def clean_agent_output(text: str) -> str:
        """
        Clean agent output by removing unwanted tags and formatting
        
        Args:
            text: The raw output from an agent (string or object)
            
        Returns:
            Cleaned text string
        """
        # Convert to string if not already
        if not isinstance(text, str):
            text = str(text)
        
        # Remove <think></think> tags and their content
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove other common AI reasoning tags
        text = re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<analysis>.*?</analysis>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<thoughts>.*?</thoughts>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<internal>.*?</internal>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Replace multiple newlines with double newline
        text = re.sub(r'^\s+|\s+$', '', text)  # Strip leading/trailing whitespace
        
        # Remove empty lines at the beginning
        text = re.sub(r'^\n+', '', text)
        
        return text
