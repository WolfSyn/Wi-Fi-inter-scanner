import pyshark
import csv
import matplotlib.pyplot as plt

def capture_wifi_packets(interface, packet_count):
    print(f"Capturing {packet_count} Wi-Fi packets on interface {interface}...")
    capture = pyshark.LiveCapture(interface=interface)
    capture.sniff(packet_count=packet_count)
    return capture

def analyze_packets(capture):
    interference_channels = {}
    packet_count = 0
    wlan_radio_count = 0
    for packet in capture:
        packet_count += 1
        try:
            if hasattr(packet,'wlan_radio') and hasattr(packet.wlan_radio, 'channel'):
                wlan_radio_count += 1
                channel = int(packet.wlan_radio.channel)
                if channel not in interference_channels:
                    interference_channels[channel] = 0
                interference_channels[channel] += 1
        except Exception as e:
            print(f"Error analyzing packet: {e}")
            continue

    print(f"Total packets analyzed: {packet_count}")
    print(f"Packets with wlan_radio layer: {wlan_radio_count}")
    print("Interference analysis completed.")
    return interference_channels


def save_to_csv(interference_channels, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Channel", "Packet Count"])
        for channel, count in sorted(interference_channels.items()):
            writer.writerow([channel, count])
    print(f"Data saved to {filename}")

def plot_interference(interference_channels):
    if not interference_channels:
        print("No interference data to plot.")
        return

    try:
        channels = list(interference_channels.keys())
        packet_counts = list(interference_channels.values())
        plt.bar(channels, packet_counts, color='skyblue')
        plt.xlabel('Channel')
        plt.ylabel('Packet Count')
        plt.title('Wi-Fi Interference Analysis')
        plt.xticks(channels)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error plotting interference analysis: {e}")

def main():
    interface = "Wi-Fi" #Replace with your wifi interface name
    packet_count = 1000 #Number of packets to capture
    csv_filename = 'wifi_interference.csv' #Name of CSV file

    #capture = capture_wifi_packets(interface, duration)
    #interference_channels = analyze_packets(capture)
    #save_to_csv(interference_channels, csv_filename)
    #plot_interference(interference_channels)

    print("Starting packet capture...")
    capture = capture_wifi_packets(interface, packet_count)
    print("Packet capture completed.")

    if not capture:
        print("No packets captured. Please ensure that your interface is connected")
        return

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
if __name__ == "__main__":
    main()
