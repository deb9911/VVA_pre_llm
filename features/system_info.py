import subprocess
import bluetooth

def list_discoverable_bluetooth_devices():
    print("Searching for discoverable Bluetooth devices...")
    devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
    print("Found {} devices.".format(len(devices)))
    for addr, name in devices:
        print("  {} - {}".format(addr, name))

def list_paired_bluetooth_devices():
    print("Listing paired Bluetooth devices...")
    try:
        result = subprocess.check_output("powershell Get-PnpDevice -Class Bluetooth", shell=True).decode()
        devices = result.splitlines()
        for device in devices:
            print(device)
    except subprocess.CalledProcessError as e:
        print("Failed to list paired Bluetooth devices.")
        print(e)

if __name__ == "__main__":
    list_discoverable_bluetooth_devices()
    print("\n")
    list_paired_bluetooth_devices()
