import streamlit as st
import time
from datetime import datetime
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.cv_evaluator import CVEvaluatorAgent
from agents.cv_improver import CVImproverAgent
from agents.skill_recommender import SkillRecommenderAgent
from agents.job_finder import JobFinderAgent
from utils.text_cleaner import TextCleaner
from utils.pdf_reader import PDFReader
from utils.logger import app_logger
from config.crew_config import CrewConfig

# Page configuration
st.set_page_config(
    page_title="CrewAI CV Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CVAssistantApp:
    """Main Streamlit application for CV Assistant"""
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.pdf_reader = PDFReader()
        self.agents_initialized = False
        self.agents = {}
        
    def initialize_agents(self):
        """Initialize all agents with error handling"""
        if self.agents_initialized:
            return True
            
        try:
            with st.spinner("Initializing AI agents... This may take a moment."):
                # Test Ollama connection first
                llm = CrewConfig.get_llm()
                test_response = llm.invoke("Hello")
                
                # Initialize agents
                self.agents = {
                    'evaluator': CVEvaluatorAgent(),
                    'improver': CVImproverAgent(),
                    'skill_recommender': SkillRecommenderAgent(),
                    'job_finder': JobFinderAgent()
                }
                
                self.agents_initialized = True
                st.success("✅ AI agents initialized successfully!")
                app_logger.info("All agents initialized successfully")
                return True
                
        except Exception as e:
            st.error(f"❌ Failed to initialize AI agents: {str(e)}")
            st.error("Please ensure Ollama is running and the model is available.")
            app_logger.error(f"Agent initialization failed: {str(e)}")
            return False
    
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🤖 CrewAI CV Assistant</h1>
            <p>Powered by AI Agents | Ollama + LangChain + CrewAI</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with instructions and info"""
        with st.sidebar:
            st.header("🔧 Instructions")
            
            st.markdown("""
            ### How to use:
            1. **Paste your CV** in the text area or upload PDF
            2. **Paste the job description** you're targeting
            3. **Click "Analyze CV"** to start the AI analysis
            4. **Review results** from 4 specialized agents
            
            ### What you'll get:
            - 📊 **ATS Compatibility Score**
            - 🎯 **CV Improvement Suggestions**
            - 📚 **Skill Gap Analysis & Learning Resources**
            - 💼 **Relevant Job Opportunities**
            """)
            
            st.header("⚙️ System Status")
            
            # Ollama status check
            try:
                llm = CrewConfig.get_llm()
                test_response = llm.invoke("ping")
                st.success("🟢 Ollama Connected")
            except:
                st.error("🔴 Ollama Disconnected")
                st.info("Please start Ollama and ensure the model is available")
            
            # Agent status
            if self.agents_initialized:
                st.success("🟢 Agents Ready")
            else:
                st.warning("🟡 Agents Not Initialized")
            
            st.header("📋 Sample Data")
            if st.button("Load Sample CV"):
                self.load_sample_data('cv')
            if st.button("Load Sample Job Description"):
                self.load_sample_data('jd')
    
    def load_sample_data(self, data_type):
        """Load sample data into session state"""
        try:
            if data_type == 'cv':
                with open('data/sample_cv.txt', 'r', encoding='utf-8') as f:
                    st.session_state.cv_text = f.read()
                st.success("Sample CV loaded!")
            elif data_type == 'jd':
                with open('data/sample_jd.txt', 'r', encoding='utf-8') as f:
                    st.session_state.jd_text = f.read()
                st.success("Sample Job Description loaded!")
        except FileNotFoundError:
            st.error(f"Sample {data_type} file not found")
    
    def render_input_section(self):
        """Render CV and JD input section"""
        st.header("📝 Input Your Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Your CV/Resume")
            
            # File upload option
            uploaded_file = st.file_uploader(
                "Upload CV (PDF)", 
                type=['pdf'],
                help="Upload your CV as a PDF file"
            )
            
            cv_text = ""
            if uploaded_file is not None:
                if self.pdf_reader.validate_pdf_file(uploaded_file):
                    cv_text = self.pdf_reader.extract_text_from_pdf(uploaded_file)
                    if cv_text:
                        st.success("✅ PDF extracted successfully!")
                        pdf_info = self.pdf_reader.get_pdf_info(uploaded_file)
                        st.info(f"Pages: {pdf_info.get('num_pages', 'Unknown')}")
                    else:
                        st.error("❌ Failed to extract text from PDF")
                else:
                    st.error("❌ Invalid PDF file")
            
            # Text area for CV
            cv_text_input = st.text_area(
                "Or paste your CV text here:",
                value=cv_text or st.session_state.get('cv_text', ''),
                height=300,
                placeholder="Paste your CV content here..."
            )
            
            # Use text input or uploaded PDF text
            final_cv_text = cv_text_input if cv_text_input.strip() else cv_text
            
            if final_cv_text:
                cv_cleaned = self.text_cleaner.clean_cv_text(final_cv_text)
                st.session_state.cv_text = cv_cleaned
                
                # Show CV stats
                word_count = len(cv_cleaned.split())
                char_count = len(cv_cleaned)
                st.info(f"📊 CV Stats: {word_count} words, {char_count} characters")
        
        with col2:
            st.subheader("🎯 Target Job Description")
            
            jd_text_input = st.text_area(
                "Paste the job description:",
                value=st.session_state.get('jd_text', ''),
                height=300,
                placeholder="Paste the target job description here..."
            )
            
            if jd_text_input:
                jd_cleaned = self.text_cleaner.clean_job_description(jd_text_input)
                st.session_state.jd_text = jd_cleaned
                
                # Show JD stats
                word_count = len(jd_cleaned.split())
                char_count = len(jd_cleaned)
                st.info(f"📊 JD Stats: {word_count} words, {char_count} characters")
    
    def render_analysis_section(self):
        """Render the analysis section with agent results"""
        cv_text = st.session_state.get('cv_text', '')
        jd_text = st.session_state.get('jd_text', '')
        
        if not cv_text or not jd_text:
            st.warning("⚠️ Please provide both CV and Job Description to start analysis")
            return
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🚀 Analyze CV", type="primary", use_container_width=True):
                if not self.initialize_agents():
                    return
                
                # Log user input
                app_logger.log_user_input(len(cv_text), len(jd_text))
                
                # Run analysis
                self.run_full_analysis(cv_text, jd_text)
    
    def run_full_analysis(self, cv_text: str, jd_text: str):
        """Run full CV analysis with all agents"""
        start_time = time.time()
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = {}
        
        try:
            # Agent 1: CV Evaluator
            status_text.text("🔍 Evaluating CV for ATS compatibility...")
            progress_bar.progress(25)
            
            results['evaluation'] = self.agents['evaluator'].evaluate_cv(cv_text)
            
            # Agent 2: CV Improver
            status_text.text("🎯 Analyzing CV improvements...")
            progress_bar.progress(50)
            
            results['improvement'] = self.agents['improver'].improve_cv(cv_text, jd_text)
            
            # Agent 3: Skill Recommender
            status_text.text("📚 Identifying skill gaps and learning resources...")
            progress_bar.progress(75)
            
            results['skills'] = self.agents['skill_recommender'].recommend_skills(cv_text, jd_text)
            
            # Agent 4: Job Finder
            status_text.text("💼 Finding relevant job opportunities...")
            progress_bar.progress(100)
            
            results['jobs'] = self.agents['job_finder'].find_jobs(cv_text, jd_text)
            
            # Store results in session state
            st.session_state.analysis_results = results
            st.session_state.analysis_completed = True
            
            total_time = time.time() - start_time
            app_logger.log_crew_execution(4, total_time)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ Analysis completed in {total_time:.1f} seconds!")
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            app_logger.error(f"Full analysis failed: {str(e)}")
    
    def render_results_section(self):
        """Render analysis results"""
        if not st.session_state.get('analysis_completed', False):
            return
        
        results = st.session_state.get('analysis_results', {})
        
        st.header("📊 Analysis Results")
        
        # Create tabs for each agent's results
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 ATS Evaluation", 
            "🎯 CV Improvements", 
            "📚 Skill Development", 
            "💼 Job Opportunities"
        ])
        
        with tab1:
            st.markdown('<div class="agent-section">', unsafe_allow_html=True)
            st.subheader("🔍 ATS Compatibility Analysis")
            
            if 'evaluation' in results:
                # Try to extract score if present
                evaluation_text = results['evaluation']
                score_match = None
                import re
                score_pattern = r'(\d+)/100|Score:\s*(\d+)|ATS.*?(\d+)'
                score_match = re.search(score_pattern, evaluation_text, re.IGNORECASE)
                
                if score_match:
                    score = next(group for group in score_match.groups() if group)
                    st.markdown(f"""
                    <div class="score-box">
                        ATS Compatibility Score: {score}/100
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(evaluation_text)
            else:
                st.error("Evaluation results not available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="agent-section">', unsafe_allow_html=True)
            st.subheader("🎯 CV Improvement Recommendations")
            
            if 'improvement' in results:
                st.markdown(results['improvement'])
            else:
                st.error("Improvement results not available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="agent-section">', unsafe_allow_html=True)
            st.subheader("📚 Skill Gap Analysis & Learning Resources")
            
            if 'skills' in results:
                st.markdown(results['skills'])
            else:
                st.error("Skill analysis results not available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<div class="agent-section">', unsafe_allow_html=True)
            st.subheader("💼 Relevant Job Opportunities")
            
            if 'jobs' in results:
                st.markdown(results['jobs'])
            else:
                st.error("Job search results not available")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Download results option
        self.render_download_section(results)
    
    def render_download_section(self, results):
        """Render download section for results"""
        st.header("💾 Export Results")
        
        # Create downloadable report
        report_content = f"""
# CV Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ATS Evaluation
{results.get('evaluation', 'Not available')}

## CV Improvement Recommendations
{results.get('improvement', 'Not available')}

## Skill Development Analysis
{results.get('skills', 'Not available')}

## Job Opportunities
{results.get('jobs', 'Not available')}

---
Generated by CrewAI CV Assistant
        """
        
        col1, col2, col3 = st.columns(3)
        
        with col2:
            st.download_button(
                label="📄 Download Full Report",
                data=report_content,
                file_name=f"cv_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
    
    def run(self):
        """Main application entry point"""
        self.render_header()
        self.render_sidebar()
        self.render_input_section()
        
        st.divider()
        
        self.render_analysis_section()
        
        if st.session_state.get('analysis_completed', False):
            st.divider()
            self.render_results_section()

def main():
    """Main function to run the Streamlit app"""
    # Initialize session state
    if 'cv_text' not in st.session_state:
        st.session_state.cv_text = ''
    if 'jd_text' not in st.session_state:
        st.session_state.jd_text = ''
    if 'analysis_completed' not in st.session_state:
        st.session_state.analysis_completed = False
    
    # Create and run the app
    app = CVAssistantApp()
    app.run()

if __name__ == "__main__":
    main()
