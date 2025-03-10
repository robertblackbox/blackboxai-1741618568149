from youtube_transcript_api import YouTubeTranscriptApi
import sys
import re

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    # Try to find video ID in different URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Regular URLs
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',  # Shortened URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url  # Return the input if it's already a video ID

def get_transcript(video_id_or_url):
    """Fetch and format the transcript for a YouTube video."""
    video_id = extract_video_id(video_id_or_url)
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript
        formatted_transcript = []
        for entry in transcript_list:
            # Convert timestamp to HH:MM:SS format
            seconds = int(entry['start'])
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Add formatted line to transcript
            formatted_transcript.append(f"[{timestamp}] {entry['text']}")
        
        return "\n".join(formatted_transcript)
    
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python youtube_scraper.py <youtube_url_or_video_id>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    transcript = get_transcript(video_url)
    
    # Print to console
    print(transcript)
    
    # Save to file
    video_id = extract_video_id(video_url)
    with open(f"{video_id}_transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"\nTranscript saved to {video_id}_transcript.txt")

if __name__ == "__main__":
    main()
