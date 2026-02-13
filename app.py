from flask import Flask, request
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
from mashup_script import run_from_web
import shutil
import zipfile
import os

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")


mail = Mail(app)

@app.route('/')
def home():
    return '''
    <h2>Mashup Creator</h2>
    <form method="POST" action="/submit">
        Singer Name: <input type="text" name="singer" required><br><br>
        Number of Videos: <input type="number" name="videos" required><br><br>
        Duration (sec): <input type="number" name="duration" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        <button type="submit">Submit</button>
    </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    singer = request.form['singer']
    videos = request.form['videos']
    duration = request.form['duration']
    email = request.form['email']

    try:
        validate_email(email)
    except EmailNotValidError:
        return "Invalid Email"

    output_file = "mashup.mp3"

    try:
        mp3_path, temp_dir = run_from_web(singer, videos, duration, output_file)

        zip_path = os.path.join(temp_dir, "mashup.zip")

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(mp3_path, "mashup.mp3")

        msg = Message(
            subject="Your Mashup",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        msg.body = "Mashup attached."

        with open(zip_path, "rb") as f:
            msg.attach("mashup.zip", "application/zip", f.read())

        mail.send(msg)

        shutil.rmtree(temp_dir)

        return "Mashup sent successfully!"

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


