import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Log file path
log_file = "daviti_datunashvili_1_server.log"

# Regular expression to extract IP, timestamp, and request type
log_pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] \"(\w+) ")

# Parsing log file
data = []
with open(log_file, "r", encoding="utf-8") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            ip, timestamp, method = match.groups()
            data.append((ip, timestamp, method))

# Convert to DataFrame
df = pd.DataFrame(data, columns=["IP", "Timestamp", "Method"])

df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y-%m-%d %H:%M:%S%z")

df.set_index("Timestamp", inplace=True)
time_counts = df.resample("T").count()["IP"]

# პოტენციური შეტევების დრო და რაოდენობა
ddos_time = time_counts.idxmax()
ddos_count = time_counts.max()
print(f"შეტევის ხანგრძლივობა: {ddos_time}, შეტევების რაოდენობა: {ddos_count}")

# ტოპ 5 IP 
top_ips = Counter(df["IP"]).most_common(5)
print(top_ips)

# ტრაფიკის დროზე დამოკიდებულების გრაფიკი

plt.figure(figsize=(12, 6))
time_counts.plot()
plt.axvline(ddos_time, color='r', linestyle='--', label="პოტენციური შეტევა")
plt.title("რექვესტები და დრო")
plt.xlabel("დრო")
plt.ylabel("რექვესტები")
plt.legend()
plt.show()

