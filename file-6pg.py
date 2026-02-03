import base64
from typing import Optional
import openai
import anthropic
from config import Config


class AISummarizer:
    def __init__(self):
        self.provider = Config.AI_PROVIDER
        
        if self.provider == "openai":
            self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    
    def summarize_text(self, text: str, style: str = "concise") -> str:
        """Summarize text content."""
        prompts = {
            "concise": "Provide a brief, concise summary of the following text in 2-3 paragraphs:",
            "detailed": "Provide a comprehensive summary with key points and insights:",
            "bullet": "Summarize the following text as bullet points highlighting main ideas:",
            "executive": "Write an executive summary suitable for stakeholders:"
        }
        
        prompt = f"{prompts.get(style, prompts['concise'])}\n\n{text}"
        
        return self._call_ai(prompt)
    
    def analyze_image(self, image_bytes: bytes, prompt: str = "Describe and summarize this image") -> str:
        """Analyze and summarize image content."""
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        else:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image
                                }
                            },
                            {"type": "text", "text": prompt}
                        ]
                    }
                ]
            )
            return response.content[0].text
    
    def summarize_code(self, code: str, language: str = "python") -> str:
        """Summarize and explain code."""
        prompt = f"""Analyze and summarize this {language} code:
        
```{language}
{code}