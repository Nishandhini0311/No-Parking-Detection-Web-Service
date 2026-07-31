import os
import cv2
import time
import pytesseract
import mysql.connector
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from twilio.rest import Client

# ---------------- APP ----------------
app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- YOLO MODEL ----------------
# ---------------- YOLO MODEL ----------------
from ultralytics import YOLO

try:
    model = YOLO("best.pt")   # your trained model
except:
    model = YOLO("yolov8n.pt")  # fallback model
    print("⚠️ best.pt not found, using default YOLO model")

# ---------------- DATABASE ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Magi@123",   # 🔴 CHANGE
    database="noparking"
)
cursor = db.cursor()

# ---------------- TWILIO ----------------
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
twilio_number = "+1 478 242 6543"    
       # 🔴 CHANGE

client = Client(account_sid, auth_token)

# ---------------- VEHICLE → PHONE ----------------
vehicle_owners = {
    "TEST1234": "+919872341234", 
    "3195HE-4": "+916369028550",
    "TN01AB1234": "+919876543210"
}

# ---------------- SETTINGS ----------------
FINE_RATE = 5
THRESHOLD = 5


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    cursor.execute("SELECT * FROM violations ORDER BY id DESC")
    data = cursor.fetchall()
    return render_template("dashboard.html", data=data)


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("video")

        if not file or file.filename == "":
            return "❌ No file selected"

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        process_video(path, filename)

        return redirect("/dashboard")

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# ---------------- PROCESS VIDEO ----------------
def process_video(path, source_name):

    cap = cv2.VideoCapture(path)

    entry_time = {}
    saved = set()
    frame_count = 0

    print("▶ Processing started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 3 != 0:
            continue

        frame = cv2.resize(frame, (640, 360))
        now = time.time()

        try:
            results = model.track(frame, persist=True, verbose=False)
        except Exception as e:
            print("YOLO error:", e)
            continue

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:

                cls = int(box.cls[0])
                label = model.names[cls]

                if label not in ["car", "motorcycle", "truck"]:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                obj_id = int(box.id[0]) if box.id is not None else 0
                vehicle_id = f"V_{obj_id}"

                # 🚫 No parking zone
                if y2 > frame.shape[0] * 0.6:

                    if vehicle_id not in entry_time:
                        entry_time[vehicle_id] = now

                    duration = now - entry_time[vehicle_id]

                    if duration > THRESHOLD and vehicle_id not in saved:

                        plate = "3195HE-4"
                        fine = duration * FINE_RATE

                        print("Detected Plate:", plate)

                        # 💾 SAVE TO DB
                        try:
                            cursor.execute("""
                            INSERT INTO violations
                            (vehicle_id, entry_time, exit_time, duration, fine, video_name)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            """, (
                                plate,
                                entry_time[vehicle_id],
                                now,
                                duration,
                                fine,
                                source_name
                            ))
                            db.commit()
                        except Exception as e:
                            print("DB error:", e)

                        # 📱 SEND SMS
                        phone = vehicle_owners.get(plate)
                        if phone:
                            send_sms(phone, plate, fine)
                        else:
                            print("No phone for:", plate)

                        saved.add(vehicle_id)

                else:
                    entry_time.pop(vehicle_id, None)

    cap.release()
    print("✔ Processing finished")


# ---------------- OCR (IMPROVED) ----------------
def detect_plate(frame, x1, y1, x2, y2):

    try:
        # Focus on bottom region
        plate_region = frame[int(y2 - 50):y2, x1:x2]

        if plate_region.size == 0:
            return "UNKNOWN"

        plate_region = cv2.resize(plate_region, None, fx=2, fy=2)

        gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)

        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(
            thresh,
            config="--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        text = text.strip().replace(" ", "").upper()

        if len(text) >= 6:
            return text

    except Exception as e:
        print("OCR error:", e)

    return "UNKNOWN"


# ---------------- SMS ----------------
def send_sms(phone, plate, fine):

    try:
        message = client.messages.create(
            body=f"🚫 No Parking Violation\nVehicle: {plate}\nFine: ₹{int(fine)}",
            from_=twilio_number,
            to=phone
        )
        print("📱 SMS sent:", message.sid)

    except Exception as e:
        print("❌ SMS error:", e)


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)