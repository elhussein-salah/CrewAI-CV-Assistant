import PyPDF2
import io
from typing import Optional

class PDFReader:
    """Utility class for reading PDF files"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Optional[str]:
        """
        Extract text from uploaded PDF file
        
        Args:
            pdf_file: Streamlit file upload object
            
        Returns:
            Extracted text as string or None if extraction fails
        """
        try:
            # Reset file pointer to beginning
            pdf_file.seek(0)
            
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return None
    
    @staticmethod
    def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Optional[str]:
        """
        Extract text from PDF bytes
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Extracted text as string or None if extraction fails
        """
        try:
            # Create a BytesIO object from bytes
            pdf_file = io.BytesIO(pdf_bytes)
            
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            print(f"Error extracting text from PDF bytes: {str(e)}")
            return None
    
    @staticmethod
    def validate_pdf_file(pdf_file) -> bool:
        """
        Validate if the uploaded file is a valid PDF
        
        Args:
            pdf_file: Streamlit file upload object
            
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # Try to access the first page to validate
            if len(pdf_reader.pages) > 0:
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_pdf_info(pdf_file) -> dict:
        """
        Get PDF metadata information
        
        Args:
            pdf_file: Streamlit file upload object
            
        Returns:
            Dictionary with PDF information
        """
        try:
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            info = {
                'num_pages': len(pdf_reader.pages),
                'file_size': len(pdf_file.getvalue()) if hasattr(pdf_file, 'getvalue') else None,
                'title': pdf_reader.metadata.get('/Title', 'Unknown') if pdf_reader.metadata else 'Unknown',
                'author': pdf_reader.metadata.get('/Author', 'Unknown') if pdf_reader.metadata else 'Unknown'
            }
            
            return info
            
        except Exception as e:
            return {'error': f"Failed to get PDF info: {str(e)}"}
