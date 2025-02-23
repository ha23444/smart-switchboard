import random
import time
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
from threading import Thread
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings

# Suppress warnings (optional, can be removed if you want to see warnings)
warnings.filterwarnings("ignore", category=UserWarning)

# Simulated smart home devices
devices = {
    "lights": {"power": 60, "state": False, "last_used": None},
    "hvac": {"power": 1500, "state": False, "last_used": None},
    "oven": {"power": 2000, "state": False, "last_used": None},
    "tv": {"power": 150, "state": False, "last_used": None},
    "refrigerator": {"power": 250, "state": False, "last_used": None},
    "ac": {"power": 1200, "state": False, "last_used": None},
}

# Simulated usage history for ML (time, device, state, hour_of_day)
usage_history = []

# Time scale: 1 second = 1 hour
TIME_SCALE = 3600  # Seconds per simulated hour

# MQTT setup (simulated for now)
mqtt_client = mqtt.Client(clean_session=True)  # Updated to use latest API
mqtt_client.connect("localhost", 1883, 60)  # Replace with real broker if available
mqtt_client.subscribe("home/#")  # Subscribe to home topics

def on_message(client, userdata, msg):
    print(f"MQTT Message: {msg.topic} - {msg.payload.decode()}")

mqtt_client.on_message = on_message
mqtt_client.loop_start()

# Machine Learning setup
scaler = StandardScaler()
model = LogisticRegression()

# Simulate training data (to be replaced with real data later)
def train_ml_model():
    global usage_history
    if len(usage_history) < 10:  # Need some data to train
        return
    df = pd.DataFrame(usage_history, columns=["time", "device", "state", "hour"])
    X = df[["hour"]].values  # Convert to NumPy array
    y = df["state"].astype(int)
    X_scaled = scaler.fit_transform(X)  # Scale features properly
    model.fit(X_scaled, y)

# Predict device state using ML
def predict_device_state(device, current_hour):
    if len(usage_history) < 10:
        return devices[device]["state"]  # Fallback to current state
    X_new = [[current_hour]]  # Ensure it's a 2D array
    X_new_scaled = scaler.transform(X_new)
    prediction = model.predict(X_new_scaled)[0]
    return bool(prediction)

# Simulate device usage
def simulate_usage(simulated_time):
    for device, info in devices.items():
        if random.random() < 0.3:  # 30% chance to toggle
            info["state"] = not info["state"]
            info["last_used"] = simulated_time
            hour = simulated_time.hour
            usage_history.append((simulated_time, device, info["state"], hour))
            mqtt_client.publish(f"home/{device}", "ON" if info["state"] else "OFF")
            if len(usage_history) >= 10:  # Only train if enough data is collected
                train_ml_model()

# Calculate energy usage
def calculate_energy_usage():
    return sum(info["power"] for device, info in devices.items() if info["state"])

# AI optimization with ML
def optimize_energy(simulated_time):
    current_hour = simulated_time.hour
    total_power = calculate_energy_usage()
    for device, info in devices.items():
        predicted_state = predict_device_state(device, current_hour)
        if info["state"] and not predicted_state and total_power > 1500:
            info["state"] = False
            mqtt_client.publish(f"home/{device}", "OFF")
            print(f"AI: Turning off {device} (ML prediction)")

# GUI with Tkinter
class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Energy Manager")
        self.running = True

        # Dashboard
        self.label = ttk.Label(root, text="Smart Home Energy Dashboard")
        self.label.pack(pady=10)

        self.status_text = tk.Text(root, height=10, width=50)
        self.status_text.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(pady=5)

        # Start simulation in a thread
        self.sim_thread = Thread(target=self.run_simulation)
        self.sim_thread.start()

    def update_dashboard(self, simulated_time):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, f"Simulated Time: {simulated_time}\n")
        self.status_text.insert(tk.END, "Device Status:\n")
        for device, info in devices.items():
            self.status_text.insert(tk.END, f"  {device}: {'ON' if info['state'] else 'OFF'} ({info['power']}W)\n")
        self.status_text.insert(tk.END, f"Total Energy Usage: {calculate_energy_usage()}W\n")
        self.status_text.insert(tk.END, "Recent History:\n")
        for entry in usage_history[-3:]:
            self.status_text.insert(tk.END, f"  {entry[0]}: {entry[1]} {'ON' if entry[2] else 'OFF'}\n")
        self.root.after(1000, self.run_simulation)  # Schedule the next simulation step after 1 second

    def run_simulation(self):
        start_time = datetime.now()
        while self.running:
            elapsed_seconds = (datetime.now() - start_time).total_seconds()
            simulated_time = start_time + timedelta(seconds=elapsed_seconds * TIME_SCALE)
            simulate_usage(simulated_time)
            optimize_energy(simulated_time)
            self.update_dashboard(simulated_time)
            time.sleep(1)  # 1 real second = 1 simulated hour

    def stop(self):
        self.running = False
        self.sim_thread.join()
        mqtt_client.loop_stop()
        self.root.quit()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()
