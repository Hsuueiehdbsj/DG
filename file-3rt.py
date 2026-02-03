import io
from typing import Tuple, Optional
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
from config import Config


class FileProcessor:
    @staticmethod
    def process_file(uploaded_file) -> Tuple[str, str]:
        """
        Process uploaded file and extract content.
        Returns: (content, file_type)
        """
        filename = uploaded_file.name.lower()
        
        # Text files
        if any(filename.endswith(ext) for ext in Config.SUPPORTED_TEXT_FORMATS):
            content = uploaded_file.read().decode('utf-8')
            return content, "text"
        
        # PDF files
        elif filename.endswith('.pdf'):
            content = FileProcessor._extract_pdf(uploaded_file)
            return content, "pdf"
        
        # Word documents
        elif filename.endswith('.docx'):
            content = FileProcessor._extract_docx(uploaded_file)
            return content, "docx"
        
        # Images
        elif any(filename.endswith(ext) for ext in Config.SUPPORTED_IMAGE_FORMATS):
            return uploaded_file.read(), "image"
        
        else:
            return "", "unsupported"
    
    @staticmethod
    def _extract_pdf(file) -> str:
        """Extract text from PDF."""
        try:
            reader = PdfReader(file)
            text_parts = []
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
            return "\n\n".join(text_parts)
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"
    
    @staticmethod
    def _extract_docx(file) -> str:
        """Extract text from DOCX."""
        try:
            doc = Document(file)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return "\n\n".join(paragraphs)
        except Exception as e:
            return f"Error extracting DOCX: {str(e)}"
    
    @staticmethod
    def validate_file_size(file, max_mb: int = None) -> bool:
        """Check if file size is within limits."""
        max_size = (max_mb or Config.MAX_FILE_SIZE_MB) * 1024 * 1024
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        return size <= max_size
    
    @staticmethod
    def get_file_info(file) -> dict:
        """Get file metadata."""
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        
        return {
            "name": file.name,
            "size_bytes": size,
            "size_readable": FileProcessor._format_size(size),
            "extension": file.name.split('.')[-1].lower()
        }
    
    @staticmethod
    def _format_size(bytes_size: int) -> str:
        """Format bytes to human readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} TB"