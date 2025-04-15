import streamlit as st 
from transformers import pipeline 
from youtube_transcript_api import YouTubeTranscriptApi 
 
def get_transcript(video_id): 
    transcript = YouTubeTranscriptApi.get_transcript(video_id) 
    result = "" 
    for i in transcript: 
        result += ' ' + i['text'] 
    return result 
 
 
def summarize_text(text, summarizer): 
    num_iters = int(len(text) / 1000) 
    summarized_text = [] 
 
    for i in range(0, num_iters + 1): 
        start = i * 1000 
        end = (i + 1) * 1000 
        out = summarizer(text[start:end]) 
        out = out[0]['summary_text'] 
        summarized_text.append(out) 
     
    return ' '.join(summarized_text) 
 
st.title("YouTube Video Summarizer") 
 
youtube_url = st.text_input("Enter YouTube video URL:", "https://www.youtube.com/watch?v=A4OmtyaBHFE") 
 
if youtube_url: 
    video_id = youtube_url.split("=")[1] 
 
    st.video(youtube_url) 
 
    st.write("Fetching transcript...") 
    try: 
        transcript = get_transcript(video_id) 
        st.write("Transcript fetched successfully!") 
        st.write(f"Transcript length: {len(transcript)} characters") 
 
        # Buttons for user to choose between summary and full transcript 
        summarize = st.button("Summarize") 
        show_full_text = st.button("Show Full Transcript") 
 
 
        if summarize or show_full_text: 
            st.write("Processing text...") 
            summarizer = pipeline('summarization') 
 
 
            if summarize: 
                summary = summarize_text(transcript, summarizer) 
                st.write("Summary:") 
                st.text_area("Summarized Text", summary, height=300) 
            elif show_full_text: 
                st.write("Full Transcript:") 
                st.text_area("Transcript Text", transcript, height=300) 
    except Exception as e: 
        st.write(f"Error fetching transcript: {e}") 
