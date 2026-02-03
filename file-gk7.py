import re
from typing import Optional, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


class VideoHandler:
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract YouTube video ID from URL."""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/shorts\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def get_transcript(video_url: str) -> Dict:
        """
        Get transcript from YouTube video.
        Returns dict with transcript text and metadata.
        """
        video_id = VideoHandler.extract_video_id(video_url)
        
        if not video_id:
            return {
                "success": False,
                "error": "Invalid YouTube URL",
                "transcript": ""
            }
        
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get manual transcript first, then auto-generated
            try:
                transcript = transcript_list.find_manually_created_transcript(['en'])
            except NoTranscriptFound:
                transcript = transcript_list.find_generated_transcript(['en'])
            
            transcript_data = transcript.fetch()
            
            # Combine transcript parts
            full_text = " ".join([entry['text'] for entry in transcript_data])
            
            # Calculate duration
            if transcript_data:
                duration_seconds = transcript_data[-1]['start'] + transcript_data[-1].get('duration', 0)
                duration_minutes = int(duration_seconds // 60)
                duration_secs = int(duration_seconds % 60)
            else:
                duration_minutes = duration_secs = 0
            
            return {
                "success": True,
                "transcript": full_text,
                "video_id": video_id,
                "duration": f"{duration_minutes}:{duration_secs:02d}",
                "word_count": len(full_text.split()),
                "segments": len(transcript_data)
            }
            
        except TranscriptsDisabled:
            return {
                "success": False,
                "error": "Transcripts are disabled for this video",
                "transcript": ""
            }
        except NoTranscriptFound:
            return {
                "success": False,
                "error": "No English transcript found for this video",
                "transcript": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error fetching transcript: {str(e)}",
                "transcript": ""
            }
    
    @staticmethod
    def get_video_thumbnail(video_id: str) -> str:
        """Get YouTube video thumbnail URL."""
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"