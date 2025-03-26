### Key Points
- It seems likely that this home security system script uses a single camera to detect people with YOLO, sends email alerts with a 60-second cooldown, and offers a user-friendly Tkinter GUI.
- Research suggests it’s designed for DIY use, with improvements like environment variables for email security and a stop button for better control.
- The evidence leans toward it being a solid foundation for open-sourcing, with potential for community enhancements due to its modular structure.

---

### Detailed Overview of the Home Security System Code

This script is a Python-based home security system that uses a single camera to detect people via the YOLO (You Only Look Once) object detection model, sends email notifications when a person is detected, and includes a Tkinter-based graphical user interface (GUI) for setup and control. Below is a comprehensive overview of its functionality, structure, and potential, as of March 26, 2025.

#### General Purpose and Functionality
The program, named "Anbu - Home Security," is designed for DIY home or small business surveillance. It:
- Captures video from a user-selected camera.
- Uses the YOLOv5s model to detect objects, specifically identifying people.
- Sends an email alert to a specified receiver when a person is detected, with a 60-second cooldown to avoid spam.
- Provides a GUI with start, stop, and exit buttons, plus a splash screen for branding.
- Aims for reliability with error handling and user feedback.

This makes it suitable for individuals seeking an affordable, customizable security solution without subscription fees.

#### Code Structure and Key Components

1. **Imports and Dependencies**
   - **Libraries Used:**
     - `cv2` (OpenCV): For camera capture and video display.
     - `smtplib`, `email.mime.text`, `email.mime.multipart`: For sending email notifications via Gmail’s SMTP server.
     - `os`: To access environment variables for email credentials.
     - `tkinter`, `ttk`: For the GUI, including dialogs and buttons.
     - `ultralytics`: For the YOLO object detection model.
     - `threading`: To run email sending in a separate thread.
     - `time`: For timing the 60-second cooldown.
   - **Dependencies:** Requires `opencv-python`, `ultralytics`, and a working Tkinter installation (standard with Python).

2. **Global Variables and Initialization**
   - **Email Credentials:** `SENDER_EMAIL` and `SENDER_PASSWORD` are loaded from environment variables (`os.getenv`), enhancing security by avoiding hardcoded or user-entered credentials.
   - **Model:** Loads `yolov5s.pt` as the default YOLO model, a lightweight version optimized for speed and accuracy on CPU-based systems.
   - **State Variables:**
     - `person_detected`: Tracks if a person is currently detected (Boolean).
     - `last_detection_time`: Records the time of the last detection for the cooldown.
     - `running`: Controls the surveillance loop (Boolean).

3. **Email Notification Function (`send_email`)**
   - **Purpose:** Sends an "Intruder Alert!" email when a person is detected.
   - **Mechanism:** Uses Gmail’s SMTP server (`smtp.gmail.com`, port 587) with TLS encryption, requiring sender credentials from environment variables.
   - **Error Handling:** Checks for missing credentials and prints errors if the email fails to send (e.g., network issues or invalid credentials).
   - **Output:** Logs success (`✅ Email Sent!`) or failure (`❌ Email error: {e}`) to the console.

4. **Camera Detection Function (`detect_available_cameras`)**
   - **Purpose:** Identifies available camera indices (0 to 4) by attempting to open each with OpenCV.
   - **Implementation:** Returns a list of integers representing valid camera indices.
   - **Limitation:** Tests only up to 5 cameras, which is reasonable for most personal setups but could be expanded for broader compatibility.

5. **Surveillance Loop Function (`start_surveillance`)**
   - **Setup:**
     - Creates a hidden Tkinter root window (`root.withdraw()`) for dialogs.
     - Prompts for receiver email via `simpledialog.askstring`.
     - Lists available cameras and asks for an index via `simpledialog.askinteger`, validating the input.
     - Opens the selected camera with OpenCV, setting resolution to 1280x720.
   - **Loop:**
     - Reads frames continuously while `running` is True.
     - Uses YOLO to detect objects, drawing bounding boxes and labels on the frame.
     - Triggers email notification if a person is detected and wasn’t previously, respecting the 60-second cooldown.
     - Displays the feed in an OpenCV window (`cv2.imshow`).
   - **Error Handling:** Reconnects if the camera disconnects, shows error messages for invalid selections or camera failures.
   - **Exit:** Stops when `running` is False (via stop button) or 'q' is pressed.

6. **Stop Function (`stop_surveillance`)**
   - **Purpose:** Safely terminates the surveillance loop by setting `running` to False.
   - **Integration:** Called by the GUI stop button, improving user control over the previous 'q'-only exit.

7. **GUI Function (`run_app`)**
   - **Splash Screen:** Displays a branded splash screen for 3 seconds with "Anbu Security Services" and a tagline.
   - **Main Window:** A 500x500 dark-themed window with:
     - Title and subtitle labels.
     - Buttons for "Start Surveillance" (green), "Stop Surveillance" (orange), and "Exit" (red).
     - A footer with a copyright notice.
   - **Execution:** Runs in the main thread, using `Thread` to start surveillance without blocking the GUI.

#### How It Runs
- **Startup:** Launching `run_app()` shows the splash screen, then the main GUI.
- **Surveillance Start:** Clicking "Start Surveillance" prompts for email and camera input, then opens a video feed window showing detected objects.
- **Detection:** If a person is detected, an email is sent (first time or after 60 seconds), with bounding boxes on the feed.
- **Control:** Stop via the GUI button or 'q', exit via the GUI button.
- **Feedback:** Console logs email status; Tkinter dialogs handle errors.

An unexpected detail is that the video feed remains in a separate OpenCV window rather than being integrated into the Tkinter GUI, which might surprise users expecting a unified interface.

#### Technical Details
- **Performance:** Runs on CPU by default (no GPU check), suitable for lightweight systems. YOLOv5s is efficient, processing frames in real-time on modest hardware.
- **Resolution:** Fixed at 1280x720, which might not suit all cameras; some may default to lower resolutions if unsupported.
- **Dependencies Installation:** Users need to install `opencv-python` and `ultralytics` via pip; Tkinter is typically included with Python, though Linux users might need `python3-tk`.

#### Strengths
- **Security:** Environment variables for email credentials reduce exposure compared to plain text input.
- **User-Friendly:** GUI with start/stop buttons and clear prompts improves accessibility.
- **Reliability:** Handles camera disconnection and invalid inputs with retries and error messages.
- **Modularity:** Functions are well-separated, making it easy to modify or extend.

#### Potential Areas for Improvement (as Previously Noted)**
- **Model Path Handling:** Hardcoded "yolov5s.pt" could fail if missing; allow user selection or include the file.
- **Camera Resolution:** Fixed 1280x720 limits compatibility; make it configurable.
- **Detection Sensitivity:** No confidence threshold adjustment; add a slider or config option.
- **Notification Strategy:** Fixed 60-second cooldown; allow user customization.
- **Logging:** No event logging; add file or database logging for history.
- **GUI Enhancements:** Integrate video feed into Tkinter or show real-time status.
- **Multiple Notifications:** Only email supported; add SMS or push options.
- **Camera Disconnection:** Retries but doesn’t alert users; add a GUI notification.

#### Suitability for Open-Sourcing
- **Community Appeal:** Its DIY focus, use of open-source tools (OpenCV, YOLO), and clear structure make it attractive for hobbyists and developers on GitHub.
- **Contribution Potential:** Modular design allows contributors to add features like multi-camera support or cloud storage.
- **Educational Value:** As a student project, it demonstrates practical use of Python, computer vision, and GUI programming, ideal for a portfolio.

#### Tables for Clarity

**Key Functions and Their Roles:**

| Function               | Role                                                                    |
|-----------------------|-------------------------------------------------------------------------|
| `send_email`          | Sends email notifications using Gmail SMTP                             |
| `detect_available_cameras` | Identifies available camera indices                                   |
| `start_surveillance`  | Runs the main detection loop with YOLO and video display                |
| `stop_surveillance`   | Stops the surveillance loop via a global flag                           |
| `run_app`             | Launches the Tkinter GUI with splash screen and control buttons         |

**Execution Flow:**

| Step                  | Action                                                                 |
|-----------------------|------------------------------------------------------------------------|
| Startup               | Show splash screen, then main GUI                                      |
| Start Surveillance    | Prompt for email and camera, begin detection loop                      |
| Detection             | Identify people, send email if conditions met, draw boxes on feed      |
| Stop                  | End loop via GUI button or 'q', close windows                          |
| Exit                  | Close application via GUI button                                       |

#### Conclusion
This home security system script is a robust, user-friendly solution for DIY surveillance, leveraging YOLO for accurate detection and Tkinter for an accessible interface. Its use of environment variables, error handling, and GUI controls mark it as an improvement over previous iterations, making it a strong candidate for open-sourcing on GitHub. With community input, it could evolve into a more feature-rich tool, aligning with the user’s goals as a student exploring open-source development.

#### Key Citations
- [YOLO Object Detection Models](https://docs.ultralytics.com/models/yolo/)
- [OpenCV Documentation](https://docs.opencv.org/4.x/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [SMTP Email Sending with Python](https://docs.python.org/3/library/smtplib.html)

Guide To SetUp
### Detailed Setup Guide for the Home Security System Code

This guide provides a step-by-step process to set up and run the provided Python script for the "Anbu - Home Security" system, which uses a single camera to detect people with the YOLOv5s model, sends email notifications via Gmail, and features a Tkinter GUI. The setup is designed for users with basic technical knowledge, covering installation of dependencies, configuration, and execution as of March 26, 2025. Instructions are tailored for Windows, macOS, and Linux, with troubleshooting tips included.

#### Prerequisites
Before starting, ensure you have:
- A computer with Windows, macOS, or a Linux distribution (e.g., Ubuntu).
- A working webcam or USB camera connected to your computer.
- Internet access for email notifications and dependency downloads.
- Administrator or sudo privileges for installing software.

---

### Step-by-Step Setup Guide

#### Step 1: Install Python
- **Why:** The script requires Python 3.x to run, as it uses modern libraries like `ultralytics` and `tkinter`.
- **How:**
  - **Windows:**
    1. Download the latest Python installer from [python.org](https://www.python.org/downloads/).
    2. Run the installer, checking "Add Python to PATH" during installation.
    3. Verify installation by opening Command Prompt (`cmd`) and typing `python --version`. You should see something like `Python 3.11.x`.
  - **macOS:**
    1. Python is pre-installed on macOS, but it’s often Python 2.x. Install Python 3 via Homebrew: Open Terminal and run `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` to install Homebrew, then `brew install python`.
    2. Verify with `python3 --version`.
  - **Linux (Ubuntu):**
    1. Open Terminal and update package lists: `sudo apt update`.
    2. Install Python 3: `sudo apt install python3 python3-pip`.
    3. Verify with `python3 --version`.

#### Step 2: Install Required Dependencies
- **Why:** The script relies on external libraries for camera access, object detection, GUI, and email functionality.
- **How:**
  1. **Open a Terminal or Command Prompt:**
     - Windows: Use Command Prompt (`cmd`) or PowerShell.
     - macOS/Linux: Use Terminal.
  2. **Install pip (if not already installed):**
     - Windows/macOS/Linux: `python -m ensurepip --upgrade` then `python -m pip install --upgrade pip`.
  3. **Install Libraries:**
     - Run the following commands one by one:
       ```
       pip install opencv-python
       pip install ultralytics
       ```
     - **Notes:**
       - `opencv-python` provides camera and video processing capabilities. On some systems, you might need `opencv-python-headless` if GUI support isn’t required, but the script uses `cv2.imshow`, so the full version is necessary.
       - `ultralytics` provides the YOLO model functionality. It downloads the `yolov5s.pt` model file automatically on first use, assuming internet access.
       - `tkinter` is included with Python, but on Linux, you may need to install it separately: `sudo apt install python3-tk` (Ubuntu).
       - `smtplib` and other email libraries are part of Python’s standard library, requiring no additional installation.

#### Step 3: Download or Verify the YOLO Model File
- **Why:** The script uses the `yolov5s.pt` model file for object detection, which is referenced directly in the code.
- **How:**
  - The `ultralytics` library typically downloads `yolov5s.pt` automatically when you first run the script with an internet connection. It’s stored in a cache directory (e.g., `~/.cache/torch/hub` on Linux/macOS or `%USERPROFILE%\.cache\torch\hub` on Windows).
  - To ensure it’s available offline:
    1. Run a test script to trigger the download:
       ```python
       from ultralytics import YOLO
       model = YOLO("yolov5s.pt")
       ```
    2. Alternatively, manually download it from the [Ultralytics GitHub releases](https://github.com/ultralytics/yolov5/releases) and place it in your project directory alongside the script.
  - **Note:** The model is licensed under CC BY-NC 4.0, allowing non-commercial use. Ensure compliance if distributing or modifying.

#### Step 4: Configure Email Credentials
- **Why:** The script sends email notifications using Gmail, requiring sender credentials stored as environment variables for security.
- **How:**
  1. **Generate an App Password for Gmail:**
     - Go to your Google Account settings ([myaccount.google.com](https://myaccount.google.com)).
     - Enable 2-Step Verification if not already active.
     - Navigate to “Security” > “App passwords,” select “Mail” and “Other (Custom name),” name it (e.g., “Anbu Security”), and generate a 16-character password.
     - Copy this password; you’ll need it for the next step.
  2. **Set Environment Variables:**
     - **Windows:**
       1. Open Command Prompt and set temporary variables (these reset on reboot):
          ```
          set EMAIL_USER=your-email@gmail.com
          set EMAIL_PASS=your-app-password
          ```
       2. For permanence, right-click “This PC” > “Properties” > “Advanced system settings” > “Environment Variables,” add new user variables `EMAIL_USER` and `EMAIL_PASS` with your email and app password.
     - **macOS/Linux:**
       1. Open Terminal and set temporary variables:
          ```
          export EMAIL_USER=your-email@gmail.com
          export EMAIL_PASS=your-app-password
          ```
       2. For permanence, edit `~/.bashrc` or `~/.zshrc` (depending on your shell) with `nano ~/.bashrc`, add the lines above, save (Ctrl+O, Enter, Ctrl+X), and run `source ~/.bashrc`.
  3. **Verify:** Run `echo $EMAIL_USER` (Linux/macOS) or `echo %EMAIL_USER%` (Windows) to confirm the variable is set.

#### Step 5: Save and Name the Script
- **Why:** The script needs to be saved as a `.py` file to execute.
- **How:**
  1. Create a new directory for your project, e.g., `AnbuSecurity`.
  2. Open a text editor (e.g., Notepad, VS Code, or nano) and paste the script.
  3. Save it as `anbu_security.py` in the `AnbuSecurity` directory.
  4. If you manually downloaded `yolov5s.pt`, place it in the same directory (optional, as `ultralytics` handles this).

#### Step 6: Test Your Camera
- **Why:** Ensure your camera works with OpenCV before running the full script.
- **How:**
  1. Create a test script, `test_camera.py`, in the same directory:
     ```python
     import cv2
     cap = cv2.VideoCapture(0)  # Try index 0 first
     while cap.isOpened():
         ret, frame = cap.read()
         if ret:
             cv2.imshow("Camera Test", frame)
             if cv2.waitKey(1) & 0xFF == ord('q'):
                 break
         else:
             print("Camera not working!")
             break
     cap.release()
     cv2.destroyAllWindows()
     ```
  2. Run it: `python test_camera.py` (Windows) or `python3 test_camera.py` (macOS/Linux).
  3. If you see your camera feed, it works. If not, try indices 1, 2, etc., by changing the number in `cv2.VideoCapture(0)`.

#### Step 7: Run the Script
- **Why:** Execute the full system to start surveillance.
- **How:**
  1. Open a terminal in the `AnbuSecurity` directory:
     - Windows: `cd path\to\AnbuSecurity`
     - macOS/Linux: `cd /path/to/AnbuSecurity`
  2. Run the script:
     - Windows: `python anbu_security.py`
     - macOS/Linux: `python3 anbu_security.py`
  3. **What Happens:**
     - A splash screen appears for 3 seconds.
     - The main GUI opens with Start, Stop, and Exit buttons.
     - Click “Start Surveillance” to prompt for a receiver email and camera index (based on available cameras detected).
     - The video feed opens, showing detected objects with bounding boxes; emails are sent if a person is detected.
     - Stop with the “Stop Surveillance” button or 'q'; exit with “Exit.”

#### Troubleshooting
- **Python Not Found:** Ensure Python is added to PATH (Windows) or use `python3` (macOS/Linux).
- **Module Not Found:** Re-run `pip install` commands; check internet connection.
- **Camera Issues:** Verify camera connection; test with multiple indices if index 0 fails.
- **Email Not Sending:** Check environment variables with `echo` commands; ensure App Password is correct and 2-Step Verification is enabled.
- **Tkinter Errors:** Install `python3-tk` on Linux; ensure Python installation includes Tkinter.
- **Model Download Fails:** Manually download `yolov5s.pt` if `ultralytics` can’t fetch it due to network issues.

#### Additional Notes
- **Operating System Variations:**
  - Windows: Command Prompt or PowerShell works; GUI elements might render slightly differently.
  - macOS: Terminal is standard; ensure XQuartz isn’t interfering with Tkinter (rare).
  - Linux: May need additional packages like `libopencv-dev` for OpenCV if building from source, though `pip` usually handles this.
- **Performance:** Runs on CPU; expect slight lag on older systems. Higher resolutions (1280x720) might not work on all cameras—edit `cap.set` lines if needed.
- **Legal Compliance:** Users should ensure camera use complies with local privacy laws (e.g., GDPR in Europe).

#### Tables for Clarity

**Setup Steps Overview:**

| Step                     | Action                                                                 |
|-------------------------|------------------------------------------------------------------------|
| Install Python          | Download and install Python 3.x                                        |
| Install Dependencies    | Use pip to install `opencv-python`, `ultralytics`                      |
| Download YOLO Model     | Ensure `yolov5s.pt` is available via `ultralytics` or manually         |
| Configure Email         | Set `EMAIL_USER` and `EMAIL_PASS` environment variables with Gmail App Password |
| Save Script             | Save as `anbu_security.py` in a project directory                      |
| Test Camera             | Run a test script to confirm camera works with OpenCV                  |
| Run Script              | Execute `python anbu_security.py` to start the system                  |

**Platform-Specific Commands:**

| Task                    | Windows                        | macOS                          | Linux (Ubuntu)                 |
|-------------------------|-------------------------------|-------------------------------|-------------------------------|
| Check Python Version    | `python --version`            | `python3 --version`           | `python3 --version`           |
| Install Dependencies    | `pip install <package>`       | `pip3 install <package>`      | `pip3 install <package>`      |
| Set Env Variables       | `set EMAIL_USER=...`          | `export EMAIL_USER=...`       | `export EMAIL_USER=...`       |
| Run Script              | `python anbu_security.py`     | `python3 anbu_security.py`    | `python3 anbu_security.py`    |

#### Conclusion
This setup guide ensures users can install, configure, and run the Anbu Home Security system with minimal hurdles. By following these steps, you’ll have a functional surveillance system that detects people and sends alerts, ready for personal use or open-sourcing on GitHub.

#### Key Citations
- [Python Installation](https://www.python.org/downloads/)
- [OpenCV Installation Guide](https://docs.opencv.org/4.x/d0/d2e/tutorial_py_table_of_contents_install.html)
- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [Google App Passwords](https://support.google.com/accounts/answer/185833)
