from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# URL of the backend container inside Docker network
BACKEND_URL = "http://backend:5001"

@app.route("/", methods=["GET"])
def index():
    """
    TODO:
    - Send a GET request to BACKEND_URL + "/api/message"
    - Extract the message from the JSON response
    - Render index.html and pass the message as "current_message"
    """
    current_message = ""
    timestamp = ""
 
    try:
        response = requests.get(f"{BACKEND_URL}/api/message")
        if response.status_code == 200:
            full_msg = response.json().get("message", "")
            
            if "(updated at " in full_msg:
                parts = full_msg.split("(updated at ")
                current_message = parts[0].strip()
                timestamp = parts[1].replace(")", "").strip()
            else:
                current_message = full_msg
                timestamp = "N/A"
        else:
            current_message = "Error: Backend returned error"
    except Exception:
        current_message = "Error: Cannot connect to backend"

    return render_template("index.html", 
                           current_message=current_message, 
                           timestamp=timestamp)

@app.route("/update", methods=["POST"])
def update():
    """
    TODO:
    - Get the value from the form field named "new_message"
    - Send a POST request to BACKEND_URL + "/api/message"
      with JSON body { "message": new_message }
    - Redirect back to "/"
    """
    new_message = request.form.get("new_message")
    
    try:
        requests.post(f"{BACKEND_URL}/api/message", json={"message": new_message})
    except Exception as e:
        pass
        
    return redirect("/")

# v2 TODO:
# - Change page title (in HTML)
# - Parse timestamp from backend message
# - Show "Last updated at: <timestamp>" in the template

if __name__ == "__main__":
    # Do not change the host or port
    app.run(host="0.0.0.0", port=5000)