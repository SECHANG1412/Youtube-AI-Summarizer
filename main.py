import os
import re
import math

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

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

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

def get_prompt(transcript):
    return (
        "다음은 유튜브 영상 자막 일부입니다.\n\n"
        f"{transcript}\n\n"
        "위 내용을 핵심 의미만 유지하여 간결하게 요약해 주세요.\n"
        "불필요한 표현은 제거하고 핵심 정보를 구조적으로 정리하세요.\n"
        "출력은 최대 4문장으로 제한하세요."
    )

summaried_transcript = []
for index, transcript in enumerate(formatted_transcript):
    prompt = get_prompt(transcript)

    print(f'{index + 1}번 요약 시작')
    response = client.responses.create(
        model='gpt-3.5-turbo',
        input=prompt
    )
    summaried_transcript.append(response.output_text)

prompt = get_prompt(transcript="\n".join(summaried_transcript) + f"\n\n최종 요약은 최대 10문장으로 정리하세요.")
final_resp = client.responses.create(
    model='gpt-3.5-turbo',
    input=prompt
)
print(final_resp.output_text)
