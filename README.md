# smart-switchboard
"Smart home energy optimization system using AI"
Smart Switchboard System

A smart switchboard system designed to optimize energy usage, manage devices based on schedules, detect human presence using a webcam, and send daily electricity usage reports via email. This project combines IoT, AI, and energy management in a smart home system.

Features
- Device Management: Automatically turns devices ON/OFF based on schedules and usage patterns.
- Human Detection: Uses a webcam to detect human presence. If no person is detected, the system turns off lights and unnecessary devices.
- Energy Optimization: Optimizes energy usage by turning off unused devices and limiting the load when the total power usage is too high.
- Email Reports: Sends daily email reports with electricity usage and estimated costs.

Prerequisites
To run this project, you'll need the following:

- Python 3.x
- OpenCV
- NumPy
- Pandas

Installation
1. Clone the repository:

    git clone https://github.com/yourusername/smart-switchboard.git
    cd smart-switchboard

2. Install the required dependencies:

    You can install the required libraries using pip:

    pip install opencv-python numpy pandas

3. Update Email Settings:

    In the code, there’s an email report functionality. Please update the send_email_report() function with your email credentials:

    sender_email = "your_email@gmail.com"
    receiver_email = "recipient_email@gmail.com"
    password = "your_password"

    Note: You may need to enable "Less secure apps" in your Gmail account for the email sending functionality to work, or use an App Password if 2-step verification is enabled.

How to Run
1. Run the program:

    In the terminal, navigate to the directory where you saved the project, and run the script:

    python smart_switchboard.py

    The program will start and continuously monitor device usage, human presence, and send daily email reports at 8 PM.

2. Expected Output:

    - It will print a dashboard showing device status (ON/OFF), power consumption, and recent usage logs.
    - If no human is detected, it will turn off the lights.
    - The system will send a daily email report at 8 PM with electricity usage and estimated cost.

Configuration
You can modify the following parameters to suit your needs:

1. Device Schedules:
   - Modify the schedules for each device in the user_preferences dictionary:

     user_preferences = {
         "hvac": {"schedule": [(8, 22)]},  # HVAC ON from 8 AM to 10 PM
         "lights": {"schedule": [(18, 23)]},  # Lights ON from 6 PM to 11 PM
     }

2. Device Power Consumption:
   - Adjust the power consumption for each device in the devices dictionary:

     devices = {
         "lights": {"power": 60, "state": False},
         "hvac": {"power": 1500, "state": False},
         "oven": {"power": 2000, "state": False},
         "refrigerator": {"power": 200, "state": True},  # Always ON
     }

3. Email Report Settings:
   - Modify the send_email_report function to match your email settings for sending daily reports.

Example Output
The system will print periodic information to the console, such as:

    🔹 Starting Smart Switchboard System...
    👤 Human detected! Keeping devices ON.
    --- Smart Home Energy Dashboard ---
    Current Time: 2025-02-23 20:05:00
      lights: OFF (60W)
      hvac: ON (1500W)
      oven: OFF (2000W)
      refrigerator: ON (200W)
    Total Energy Usage: 1700 W
    Recent Usage History:
      2025-02-23 19:59:00: lights OFF
      2025-02-23 19:59:00: hvac ON
      ...
    ---------------------------------

At 8 PM, the program will send an email like:

    Subject: Daily Electricity Usage Report

    Hello,

    Your daily electricity usage report:
    - Total Power Consumption: 1700 W
    - Estimated Cost: ₹8.5

    Best,
    Smart Switchboard AI

Contributing
Feel free to fork the repository, make improvements, and submit pull requests. If you find any bugs or have suggestions for new features, feel free to open an issue.

License
This project is licensed under the MIT License - see the LICENSE file for details.

---

Note: Make sure to properly handle your email credentials and avoid sharing sensitive information in public repositories. You can use environment variables or external configuration files for more secure handling of credentials.
