import cv2
import smtplib
import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Label, StringVar, OptionMenu
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ultralytics import YOLO
from threading import Thread
import time

# Initialize YOLO model
model = YOLO("yolov5s.pt")

def send_email(sender_email, sender_password, receiver_email):
    """Send an email notification when a person is detected."""
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "🚨 Intruder Alert!"
        msg.attach(MIMEText("A person has been detected in the surveillance area!", "plain"))

        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email notification sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def detect_available_cameras(max_cameras=5):
    """Detect available camera indices."""
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(str(i))
            cap.release()
    return available_cameras

def get_camera_selection(root):
    """Show a dropdown menu to select cameras."""
    available_cameras = detect_available_cameras()
    if not available_cameras:
        messagebox.showerror("Camera Error", "No available cameras found.")
        return None

    camera_selection = StringVar(root)
    camera_selection.set(available_cameras[0])  # Default selection

    popup = Toplevel(root)
    popup.title("Select Camera")
    Label(popup, text="Choose a camera:", font=("Arial", 12)).pack(pady=10)
    OptionMenu(popup, camera_selection, *available_cameras).pack(pady=5)
    
    def confirm():
        popup.destroy()

    tk.Button(popup, text="OK", command=confirm).pack(pady=10)
    root.wait_window(popup)  # Wait for user to make selection
    return int(camera_selection.get())

def start_surveillance():
    """Start the surveillance system."""
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter main window

    sender_email = simpledialog.askstring("Email Setup", "Enter Sender Email (Gmail):", parent=root)
    sender_password = simpledialog.askstring("Email Setup", "Enter App Password (Google App Password):", parent=root, show="*")
    receiver_email = simpledialog.askstring("Email Setup", "Enter Receiver Email:", parent=root)

    if not sender_email or not sender_password or not receiver_email:
        messagebox.showerror("Error", "Email setup incomplete!")
        return

    camera_index = get_camera_selection(root)
    if camera_index is None:
        return

    root.destroy()

    # Open camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Failed to open selected camera!")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    person_detected = False
    last_detection_time = time.time()

    while True:
        success, frame = cap.read()
        if not success:
            print("❌ Error: Failed to read frame")
            break

        results = model(frame)[0]
        person_found = False

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = f"{model.names[cls]} {conf:.2f}"
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
            
            if model.names[cls] == 'person':
                person_found = True

        # Handle person detection logic
        if person_found:
            if not person_detected:
                person_detected = True
                last_detection_time = time.time()
                Thread(target=send_email, args=(sender_email, sender_password, receiver_email)).start()
        else:
            if time.time() - last_detection_time > 60:
                person_detected = False

        cv2.imshow("Anbu Surveillance Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_app():
    """Launch the GUI."""
    root = tk.Tk()
    root.title("Anbu - Home Security Surveillance")
    root.geometry("500x500")
    root.configure(bg="#121212")

    tk.Label(root, text="Anbu Surveillance System", font=("Arial", 18, "bold"), fg="white", bg="#121212").pack(pady=20)
    tk.Label(root, text="Your Smart Home Security Solution", font=("Arial", 12), fg="gray", bg="#121212").pack(pady=5)

    tk.Button(root, text="▶ Start Surveillance", command=lambda: Thread(target=start_surveillance).start(),
              height=2, width=25, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=15)

    tk.Button(root, text="❌ Exit", command=root.quit, height=2, width=25, bg="#D32F2F", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_app()

