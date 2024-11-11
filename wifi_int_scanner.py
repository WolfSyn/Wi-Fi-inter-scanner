import pyshark
import csv
import matplotlib.pyplot as plt
import time

def capture_wifi_packets(interface, duration):
    print(f"Capturing Wi-Fi packets on interface {interface} for {duration} seconds...")
    capture = pyshark.LiveCapture(interface=interface)
    capture.sniff(timeout=duration)
    return capture

def analyze_packets(capture, timeout=30):
    interference_channels = {}
    start_time = time.time()
    packet_count = 0
    for packet in capture:
        packet_count += 1
        try:
            if 'wlan_radio' in packet:
                channel = packet.wlan_radio.channel
                if channel not in interference_channels:
                    interference_cahnnels[channel] = 0
                interference_channels[channel] += 1
        except Exception as e:
            print(f"Error analyzing packet: {e}")

            #log process
            if packet_count % 100 == 0:
                print(f"Analyzed {packet_count} packets...")

            #check for timeout
            if time.time() - start_time > timeout:
                print("Analysis timeout reached")
                break

    print(f"Interference analysis completed.")
    return interference_channels

def save_to_csv(interference_channels, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(interference_channels.items())
        for channel, count in sorted(interference_channels.items()):
            writer.writerow([channel, count])
    print(f"Data saved to {filename}")

def plot_interference(interference_channels):
    channels = list(interference_channels.keys())
    packet_counts = list(interference_channels.values())

    plt.bar(channels, packet_counts, color='skyblue')
    plt.xlabel('Channel')
    plt.ylabel('Packet Count')
    plt.title('Wi-Fi Interference Analysis')
    plt.xticks(channels)
    plt.grid(True)
    plt.show()

def main():
    interface = "Wi-Fi" #Replace with your wifi interface name
    duration = 60 #Duration in seconds
    csv_filename = 'wifi_interference.csv' #Name of CSV file

    #capture = capture_wifi_packets(interface, duration)
    #interference_channels = analyze_packets(capture)
    #save_to_csv(interference_channels, csv_filename)
    #plot_interference(interference_channels)

    print("Starting packet capture...")
    capture = capture_wifi_packets(interface, duration)
    print("Packet capture completed.")

    print("Analyzing packets...")
    interference_channels = analyze_packets(capture)
    print("Analysis completed.")

    print("Saving data to CSV...")
    save_to_csv(interference_channels, csv_filename)
    print("Data saved to CSV.")

    print("Plotting interference analysis...")
    plot_interference(interference_channels)

    print("Interference Analysis:")
    for channel, count in sorted(interference_channels.items()):
        print(f"Channel {channel}: {count} packets")

    print("Interference Analysis:")
    for channel, count in sorted(interference_channels.items()):
        print(f"Channel {channel}: {count} packets")
if __name__ == "__main__":
    main()
