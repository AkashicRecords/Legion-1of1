import schedule
import time
import datetime
import pyaudio
import wave
import cv2
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from jnius import autoclass
import os

Environment = autoclass('android.os.Environment')
File = autoclass('java.io.File')

Base = declarative_base()

class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    text_content = Column(String)
    audio_content = Column(LargeBinary)
    video_content = Column(LargeBinary)

def get_storage_path():
    if Environment.getExternalStorageState() == Environment.MEDIA_MOUNTED:
        return Environment.getExternalStorageDirectory().getAbsolutePath()
    else:
        return PythonActivity.mActivity.getFilesDir().getAbsolutePath()

storage_path = get_storage_path()
db_path = os.path.join(storage_path, 'journal.db')
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Android classes we'll need
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
AlarmManager = autoclass('android.app.AlarmManager')
Calendar = autoclass('java.util.Calendar')

def set_alarm(hour, minute):
    context = PythonActivity.mActivity
    alarm_manager = context.getSystemService(Context.ALARM_SERVICE)

    # Create an intent for the alarm
    intent = Intent(context, PythonActivity)
    intent.setAction("JOURNAL_PROMPT")
    pending_intent = PendingIntent.getBroadcast(context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT)

    # Set the alarm time
    calendar = Calendar.getInstance()
    calendar.setTimeInMillis(System.currentTimeMillis())
    calendar.set(Calendar.HOUR_OF_DAY, hour)
    calendar.set(Calendar.MINUTE, minute)

    # Schedule the alarm
    alarm_manager.setRepeating(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(),
                               AlarmManager.INTERVAL_DAY, pending_intent)

def prompt_journal():
    print("Time for your journal entry!")
    text_entry = input("Enter your text journal: ")
    
    # Audio recording
    audio = record_audio()
    
    # Video recording
    video = record_video()
    
    # Save to database
    session = Session()
    new_entry = JournalEntry(text_content=text_entry, audio_content=audio, video_content=video)
    session.add(new_entry)
    session.commit()
    session.close()

def record_audio(duration=10):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("Recording audio...")
    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Audio recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return b''.join(frames)

def record_video(duration=10):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('temp_video.avi', fourcc, 20.0, (640, 480))
    
    print("Recording video...")
    start_time = time.time()
    while(int(time.time() - start_time) < duration):
        ret, frame = cap.read()
        out.write(frame)
    
    print("Video recording finished.")
    cap.release()
    out.release()
    
    with open('temp_video.avi', 'rb') as f:
        video_data = f.read()
    
    return video_data

def run_agent():
    # Set alarms for 9 AM and 9 PM
    set_alarm(9, 0)
    set_alarm(21, 0)

    # This part needs to be handled in the Android app's main activity
    # to respond to the "JOURNAL_PROMPT" action
    # When the alarm triggers, it should call prompt_journal()

if __name__ == "__main__":
    run_agent()