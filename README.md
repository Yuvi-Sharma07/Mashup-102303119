# Mashup-102303119

Mashup-102303119 is a web-based Mashup Creator application that downloads multiple songs of a given singer from YouTube, extracts a fixed duration from each song, merges them into a single mashup, and sends the final output as a ZIP file to the user via email.

Live Deployment:
https://mashup-102303119.onrender.com/

------------------------------------------------------------

## Project Overview

This project consists of:

1. A core mashup generation script
2. A Flask-based web service
3. Email integration using Gmail SMTP
4. Deployment on Render cloud platform

The system works as follows:

User Input → Flask Backend → YouTube Download → Audio Processing → Mashup Creation → ZIP Generation → Email Delivery

------------------------------------------------------------

## Project Structure

Mashup-102303119/
│
├── 102303119.py
├── mashup_script.py
├── app.py
├── requirements.txt
├── Procfile
└── runtime.txt

------------------------------------------------------------

## File Descriptions

### 1. 102303119.py

This is the original command-line version of the Mashup Creator.

It:
- Takes singer name, number of videos, duration, and output filename as command-line arguments
- Downloads videos from YouTube
- Converts video to audio
- Cuts fixed duration from each audio file
- Merges audio clips
- Creates final mashup MP3

Usage:

python 102303119.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>

Example:

python 102303119.py "arijit singh" 5 20 mashup.mp3

------------------------------------------------------------

### 2. mashup_script.py

This file contains the reusable mashup logic used by both:

- The CLI version
- The Flask web application

It includes:
- download_videos()
- convert_to_audio()
- cut_audio()
- merge_audio()
- run_from_web()

The function run_from_web() is specifically used by the Flask backend to generate mashups dynamically.

------------------------------------------------------------

### 3. app.py

This is the Flask web service.

Features:
- Accepts user input (Singer name, number of videos, duration, email)
- Calls run_from_web()
- Creates ZIP file
- Sends email using Gmail SMTP
- Deployed using Gunicorn

------------------------------------------------------------

## Deployment Platform

Hosted on Render:

https://mashup-102303119.onrender.com/

Deployment configuration:

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app

Environment Variables:
MAIL_USERNAME
MAIL_PASSWORD

------------------------------------------------------------

## Requirements

requirements.txt contains:

flask
flask-mail
pytubefix
moviepy
email-validator
gunicorn

------------------------------------------------------------

## Gmail Configuration

To enable email functionality:

1. Enable 2-Step Verification in Google Account.
2. Generate an App Password.
3. Add the following environment variables in Render:

MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your_app_password

Normal Gmail password must not be used.

------------------------------------------------------------

## How It Works

1. User enters:
   - Singer Name
   - Number of Videos
   - Duration
   - Email ID

2. The backend:
   - Searches YouTube
   - Downloads audio streams
   - Converts and trims audio
   - Merges clips
   - Creates mashup.mp3
   - Compresses it into mashup.zip

3. The ZIP file is sent to the provided email address.

------------------------------------------------------------

## Technical Stack

Backend:
Python
Flask
Gunicorn

Audio Processing:
MoviePy

YouTube Integration:
pytubefix

Email Service:
SMTP (Gmail)

Hosting:
Render

------------------------------------------------------------

## Important Notes

- This project is intended for academic use.
- YouTube downloads may fail if network restrictions apply.
- Render free tier may experience cold start delays.
- Gmail App Password is required for email functionality.

------------------------------------------------------------

## Author

Yuvraj Sharma

Project: Mashup-102303119
Roll Number: 102303119

------------------------------------------------------------
