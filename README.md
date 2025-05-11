
# Anbu Surveillance System

&#x20;*Figure: Example surveillance cameras (placeholder).*
Anbu is a Python-based smart home security system developed by V Anbu Chelvan. It leverages computer vision for **real-time person detection** using an Ultralytics YOLO model (e.g. YOLOv5). The system monitors **multiple camera** feeds simultaneously and alerts the user via email whenever a person (intruder) is detected. A Tkinter-based GUI provides an easy way to register/login, add camera streams, and view live video with detection overlays. Detected events (snapshots or video clips) are recorded for later review, and all sensitive settings (like SMTP credentials) are stored in a JSON file encrypted with Fernet.

## Features

* **Real-time Person Detection:** Uses Ultralytics YOLO (e.g. a PyTorch-based YOLOv5/YOLOv8 model) for fast, high-accuracy detection of people.
* **Multi-Camera Support:** Can capture and process multiple video streams in parallel. (Implementation typically uses threading or Tkinter frames to read each camera without blocking).
* **Graphical User Interface:** Tkinter GUI for user interaction. Users can register, log in, add camera sources, and start/stop monitoring via the GUI.
* **Email Alerts:** Sends instant email notifications to the configured address when an intruder is detected. (For example, a Python `Notification` class can use SMTP to send an email with an image attachment on detection.)
* **Event Recording:** Saves snapshots or video of detection events to disk using OpenCV’s `VideoWriter`. Each recorded file includes the timestamp and camera ID.
* **User Authentication:** Built-in register/login/forgot-password system with user credentials stored in a local SQLite database.
* **Encrypted Configuration:** Application settings (e.g. email credentials, camera URLs) are stored in `config.json` encrypted with Fernet, so they cannot be read or tampered with without the secret key.
* **Flexible Settings:** Configurable detection thresholds, recording counts, and support for different YOLO model files.

## Technologies Used

* **Python 3** – primary language.
* **Ultralytics YOLO (PyTorch)** – for object detection. YOLOv5/v8 is chosen for its speed and accuracy.
* **OpenCV** – for video capture, image processing, multi-camera handling, and writing output to file.
* **Tkinter** – for building the desktop GUI interface.
* **smtplib & email.mime** – Python libraries for sending email alerts via SMTP.
* **SQLite3** – lightweight database for user credentials. (Note: SQLite has no built-in auth/encryption, so file security is important.)
* **cryptography (Fernet)** – for symmetric encryption of the config file.
* **Threading/Multiprocessing** – to handle multiple camera I/O without blocking the GUI.
* **Others:** `Pillow` for image handling in GUI, standard Python libraries, etc.

## Setup Instructions

### Windows

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ZANYANBU/Anbu-Surveillance.git
   cd Anbu-Surveillance
   ```
2. **Install dependencies:** Ensure Python 3.x is installed. Then run:

   ```bash
   pip install -r requirements.txt
   ```
3. **Download YOLO Model:** Download a pretrained model (e.g. `yolov5s.pt`) from [Ultralytics YOLOv5 releases](https://github.com/ultralytics/yolov5/releases) and place it in this project folder.
4. **Configure Email:** Edit `config.json` or set environment variables for your SMTP email and password. For Gmail, generate a 16-digit App Password (since it does not allow normal passwords) as shown in the Ultralytics guide.
5. **Run the app:**

   ```bash
   python anbu.py
   ```

   *(If multiple Python versions are installed, you may need `python3`.)*

### Linux

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ZANYANBU/Anbu-Surveillance.git
   cd Anbu-Surveillance
   ```
2. **Install Python3 and dependencies:**

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   ```
3. **Download YOLO Model:** Place the `yolov5s.pt` (or equivalent) in this directory.
4. **Configure Email:** Same as Windows (use a Gmail App Password, or provide SMTP settings).
5. **Run the app:**

   ```bash
   python3 anbu.py
   ```

## Model Requirements

* **YOLO Weights:** The system requires a YOLO model file (e.g. `yolov5s.pt`). Download this from the official source and ensure it is accessible in the project directory. The application will load the model via the Ultralytics API.
* **Configuration:** The `config.json` file holds settings like camera URLs and email credentials. This file is encrypted; use the provided key or the GUI’s **Settings** panel to update it.
* **Dependencies:** All required Python libraries are listed in `requirements.txt` (e.g. `opencv-python`, `ultralytics`, `cryptography`, `pillow`, etc.).

## Usage Guide

1. **Launch the Application:** After setup, run `anbu.py`. The login window will appear.
2. **Register/Login:** If running for the first time, click *Register* to create a new account (this saves your username in the local SQLite DB). Then log in with your credentials.
3. **Add Cameras:** In the GUI, use the *Add Camera* option to enter camera sources. These can be device indices (like `0`, `1`, for webcams) or video stream URLs (e.g. RTSP). Each added camera will appear in the list.
4. **Start Monitoring:** Click the *Start* button. Live feeds from all configured cameras will display, with detected persons outlined.
5. **Alerts & Recording:** When a person is detected, the system will automatically:

   * **Send an email alert** to the configured address (with an image attachment).
   * **Save the event** (snapshot or clip) to the `events/` directory using OpenCV’s `VideoWriter`.
6. **Stopping:** Click *Stop* to end surveillance, or close the window. You can then log out or exit the app.

## Screenshots / Demo

&#x20;*Figure: Example of a security camera (placeholder).*
This placeholder image is not the actual GUI but an example. In practice, include **screenshots** of the Tkinter interface (e.g. login screen, live view with detections) and any **demo video** links (for example, a YouTube video) to illustrate the application in action.

## Security Considerations

* **Credentials:** Do **not** hard-code passwords or API keys. Use environment variables or a secure `.env` file so that sensitive data stays out of the codebase. For example, set your SMTP username/password in the OS or use a protected config.
* **Email Security:** Use app-specific passwords for email. For Gmail, enable 2FA and use the 16-digit App Password (instead of your regular password) as recommended. This prevents exposing your main account password.
* **Encryption:** The `config.json` is encrypted with Fernet; without the key, attackers cannot read or alter the settings. Keep the encryption key safe (not in source control).
* **Database Safety:** SQLite has no built-in encryption or user auth. Secure the `users.db` file via operating-system permissions so that only authorized users can read it. Consider encrypting it externally (e.g. using SQLCipher) if storing very sensitive data.
* **Dependencies:** Keep libraries up-to-date. Note that Ultralytics YOLOv5 is continuously tested across platforms. Regularly update to patch any security issues.
* **Input Validation:** Be cautious when adding cameras or other inputs. Validate URLs and paths to prevent injections or crashes.
* **Network:** If cameras or email operate over the internet, ensure network security (firewalls, VPNs, etc.) to prevent unauthorized access.

## Contributing

Contributions are welcome! To contribute:

* Fork the repository and create your branch (`git checkout -b feature/my-feature`).
* Commit your changes with clear messages.
* Submit a Pull Request describing your improvement or bug fix.
* For issues or suggestions, please open an issue on GitHub.

Please follow Python best practices (PEP 8) and include tests if possible. You can also suggest new features or improvements.

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

**References:** Ultralytics YOLO documentation; YOLO security alarm guides; Python email/Tkinter tutorials; SQLite and Fernet official docs.


