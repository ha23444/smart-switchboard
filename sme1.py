import random
import time
import smtplib
import cv2
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Device power consumption in watts
devices = {
    "lights": {"power": 60, "state": False, "last_used": None},
    "hvac": {"power": 1500, "state": False, "last_used": None},
    "oven": {"power": 2000, "state": False, "last_used": None},
    "refrigerator": {"power": 200, "state": True, "last_used": None},  # Always on
}

usage_history = []  # Store usage logs
electricity_cost_per_kwh = 5  # Cost per kWh in INR

# User preferences (Auto ON/OFF schedules)
user_preferences = {
    "hvac": {"schedule": [(8, 22)]},  # 8 AM - 10 PM
    "lights": {"schedule": [(18, 23)]},  # 6 PM - 11 PM
}

# Camera-based human detection
def detect_human():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)  # Open camera
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    cap.release()
    return len(faces) > 0

# Simulate device usage (random toggling)
def simulate_usage():
    current_time = datetime.now()
    for device, info in devices.items():
        if random.random() < 0.3:  # 30% chance to toggle
            info["state"] = not info["state"]
            info["last_used"] = current_time
            usage_history.append((current_time, device, info["state"]))

# Calculate current energy usage
def calculate_energy_usage():
    return sum(info["power"] for info in devices.values() if info["state"])

# Check and enforce user-defined schedules
def check_schedules():
    current_hour = datetime.now().hour
    for device, prefs in user_preferences.items():
        for start, end in prefs["schedule"]:
            devices[device]["state"] = start <= current_hour < end

# AI Optimization: Turn off unused devices & limit power usage
def optimize_energy():
    current_time = datetime.now()
    total_power = calculate_energy_usage()

    for device, info in devices.items():
        if device == "lights" and info["state"] and info["last_used"]:
            if (current_time - info["last_used"]).total_seconds() > 600:
                info["state"] = False
                print(f"AI: Turning off {device} (unused for 10+ minutes)")

    if total_power > 2000 and devices["hvac"]["state"]:
        devices["hvac"]["state"] = False
        print("AI: Turning off HVAC to reduce load")

# Predict future energy usage (Basic Time-Series Forecasting)
def predict_energy_usage():
    data = [random.randint(500, 2500) for _ in range(7)]  # Simulated past usage
    avg_usage = sum(data) / len(data)
    return avg_usage * 1.05  # Assume 5% increase

# Generate and send an electricity usage email report
def send_email_report():
    sender_email = "your_email@gmail.com"
    receiver_email = "recipient_email@gmail.com"
    password = "your_password"

    total_power = calculate_energy_usage()
    estimated_cost = (total_power / 1000) * electricity_cost_per_kwh

    subject = "Daily Electricity Usage Report"
    body = f"""Hello,

Your daily electricity usage report:
- Total Power Consumption: {total_power} W
- Estimated Cost: ₹{round(estimated_cost, 2)}

Predicted usage for tomorrow: {round(predict_energy_usage(), 2)} W

Best,
Smart Switchboard AI
"""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("📧 Email report sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Display energy dashboard
def display_dashboard():
    print("\n--- Smart Home Energy Dashboard ---")
    print(f"Current Time: {datetime.now()}")
    for device, info in devices.items():
        print(f"  {device}: {'ON' if info['state'] else 'OFF'} ({info['power']}W)")
    print(f"Total Energy Usage: {calculate_energy_usage()} W")
    print("Recent Usage History:")
    for entry in usage_history[-5:]:
        print(f"  {entry[0]}: {entry[1]} {'ON' if entry[2] else 'OFF'}")
    print("---------------------------------")

# Main loop to run the smart switchboard system
def run_prototype():
    print("🔹 Starting Smart Switchboard System...")
    email_sent_today = False

    while True:
        current_hour = datetime.now().hour
        check_schedules()
        simulate_usage()
        optimize_energy()
        
        if detect_human():
            print("👤 Human detected! Keeping devices ON.")
        else:
            devices["lights"]["state"] = False
            print("🚫 No person detected! Turning lights OFF.")

        display_dashboard()

        # Send email report at 8 PM daily
        if current_hour == 20 and not email_sent_today:
            send_email_report()
            email_sent_today = True

        if current_hour == 21:  # Reset email flag after 9 PM
            email_sent_today = False

        time.sleep(5)  # Simulate time passing

if __name__ == "__main__":

    try:
        run_prototype()
    except KeyboardInterrupt:
        print("\n⏹ System stopped by user.")