import re
from youtube_transcript_api import YouTubeTranscriptApi
import math

def extract_video_id(url):
    pattern = r"(?:v=|\/v\/|youtu\.be\/|\/embed\/)([A-Za-z0-9_-]{11})"
    m = re.search(pattern, url)

    if m:
        video_id = m.group(1)
        return video_id
    
    raise ValueError('유효한 유튜브 비디오 URL을 입력해주세요')


def fetch_transcript(video_id):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=('ko',))
    return transcript


video_url = input('유튜브 영상을 입력해주세요:')
video_id = extract_video_id(video_url)
print('추출된 video_id', video_id)

transcript = fetch_transcript(video_id)
print(transcript)

chunk_size = 50
total_chunks = math.ceil(len(transcript) / chunk_size)

chucked_transcript = []
for index in range(total_chunks):
    start_idx = index * chunk_size
    sliced = transcript[start_idx:start_idx + chunk_size]
    chucked_transcript.append(sliced)

formatted_transcript = []
for transcript in chucked_transcript:
    merged_lines = []
    for item in transcript:
        start_time = f"{item.start:.2f}s"
        merged_lines.append(f"{start_time}: {item.text}")
    merged_text = "\n".join(merged_lines)
    formatted_transcript.append(merged_text)


for content in formatted_transcript:
     print(content)
     print('--------------------------')