"""
# #####################################################################

sample script to test ZCube API 
for zCUBE Engine Python extension module 
Copyright (c)2022-2025 by Zappadoc - All Rights Reserved.
https://www.eksimracing.org

This source code, module, lib and all information, data, and algorithms
associated with it are subject to change without notice.

Change history: 
               -- 2025.04.03: created - Zappadoc    
               
This example shows how to interact with Leo bodnar USB device using the Python.
Both the Full and Lite versions are supported.

Main Features:
- Device initialization and capability detection
- Input polling (Full version only)
- LED control (RPM, Warning)
- External LED control (Full version only)
- Display panel (3, 4, or 6 digits) control (limited charset in lite version)
- Gear indicator (limited charset in lite version)
- Brightness control (Full version)
- Wheel motor simulation on Bodnar Conversion kit - SLI-FTEC device (Full version)

To use:
- Plug in your device
- Choose either the Lite or Full version of the module
- Run the script directly to test available features

Note: Some features are not available in the Lite version.

Read the zCube Doc / API for more info:
https://www.eksimracing.org/zcube-developer-kit/
               
License:
https://www.eksimracing.org/terms-conditions

DISCLAIMER:
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

All product names are trademarks or registered trademarks of their respective holders.

# #####################################################################
"""

import threading
import z3slim_lite as sli    # Free Lite Version
#import z3slim as sli         # Full Version
import time

# instance of z3 engine
dev_unit1 = sli.z3engine() 
# Global variable to track thread status
thread_down = True
# full version vs lite
is_full_version = False
# Global dictionary to store device capabilities
device_info = {}

def initialize_device(dev):
    # Initialize the device
    if dev.init():
        print("Start Testing...")
        return True
    print("Device Error!\n- device not connected (connect your device)\n- or license not found (register your device)\n- or the default device is not found (change the script with the correct zCube extension!")
    return False

def get_device_info(dev):
    # Retrieve device information and capabilities
    dev_path = dev.get_device_info("device path")
    dev_sn = dev.get_device_info("serial number")    
    dev_name = dev.get_device_info("name")
    dev_version = dev.get_device_info("version")
    dev_vendid = dev.get_device_info("vendor id")
    dev_prodid = dev.get_device_info("product id")
    btns = dev.get_device_info("digital")
    sw = dev.get_device_info("analog")
    max_rpm_leds = dev.get_device_info("max rpm led")
    max_warn_leds = dev.get_device_info("max warning led")
    max_ext_leds = dev.get_device_info("max external led")
    max_brightness = dev.get_device_info("brightness")
    is_gear_present = dev.get_device_info("gear")
    max_digits = dev.get_device_info("digits") if dev.get_device_info("panel count") >= 1 else 0
    max_rumble_motor = dev.get_device_info("rumble motor")
    

    dev_info = {
        "name": dev_name,
        "version": dev_version,
        "vendor_id": dev_vendid,
        "product_id": dev_prodid,
        "serial_num": dev_sn,
        "path": dev_path, 
        "buttons": btns,
        "switches": sw,
        "max_rpm_leds": max_rpm_leds,
        "max_warn_leds": max_warn_leds,
        "max_ext_leds": max_ext_leds,
        "max_brightness": max_brightness,
        "is_gear_present": is_gear_present,
        "max_digits": max_digits,
        "max_rumble_motor": max_rumble_motor
        
    }
   
    return dev_info

# ---------------------------------------------------------

def input_watcher(dev, stop_event, dev_name):
    # Monitor input events from the device
    if "_lite" in dev_name:
        print("Not Implemented in Lite Version - Use the Full Version")
        return

    print("Thread Start: Poll Inputs...\n")
    while not stop_event.is_set():
        try:
            dv, type_, pos, val, is_new = dev.get_input_data()
            if is_new:
                print(f"Device: {dv}, Type: {type_}, Pos: {pos}, Value: {val}, isNew: {bool(is_new)}")
        except Exception as e:
            print(f"Error reading input data: {e}")
        time.sleep(0.1)
    print("Thread Down...\n")

def start_input_thread(dev, dev_name, btns):
    # Start the input monitoring thread if conditions are met
    global thread_down
    if btns > 0 and "_lite" not in dev_name:
        dev.start_input_listener()
        stop_event = threading.Event()
        t = threading.Thread(target=input_watcher, args=(dev, stop_event, dev_name), daemon=True)
        t.start()
        thread_down = False
        return stop_event, t
    return None, None

# ---------------------------------------------------------

def toggle_rpm_leds(dev, dev_info, state):
    # Toggle RPM LEDs
    if dev_info["max_rpm_leds"] > 0:
        for i in range(1, dev_info["max_rpm_leds"] + 1):
            dev.set_rpm_led(i, state)
        dev.show_me()

def toggle_warn_leds(dev, dev_info, state):
    # Toggle warning LEDs
    if dev_info["max_warn_leds"] > 0:
        for i in range(1, dev_info["max_warn_leds"] + 1):
            dev.set_warning_led(i, state)
        dev.show_me()

def toggle_ext_leds(dev, dev_info, state):
    # Toggle external LEDs
    if not is_full_version:
        return
    if dev_info["max_ext_leds"] > 0:
        for i in range(1, dev_info["max_ext_leds"] + 1):
            dev.set_external_led(i, state)
        dev.show_me()

def toggle_all_leds(dev, dev_info, state):
    # Toggle all LEDs
    toggle_rpm_leds(dev, dev_info, state)
    toggle_warn_leds(dev, dev_info, state)
    toggle_ext_leds(dev, dev_info, state)

def clear_display(dev, dev_info):
    # Clear the display and turn off LEDs
    if dev_info["is_gear_present"] > 0:
        dev.set_gear(" ", False)
    if dev_info["max_digits"] == 3:
        dev.set_central_panel("   ")
    elif dev_info["max_digits"] == 4:
        dev.set_left_panel("    ")
        dev.set_right_panel("    ")
    elif dev_info["max_digits"] == 6:
        dev.set_left_panel("      ")
        dev.set_right_panel("      ")
    toggle_all_leds(dev, dev_info, 0)
    dev.show_me()

def time_to_7seg_string(mn, sc, ms, side=1):
    # Convert time to 7-segment display string
    if mn == 0 and sc == 0 and ms == 0:
        return "-:--.---" if side == 1 else "-.--.---"
    elif mn < 10:
        return f"{mn}:{sc:02d}.{ms:03d}" if side == 1 else f"{mn}.{sc:02d}.{ms:03d}"
    elif mn >= 60:
        hr = mn // 60
        mn = mn % 60
        return f" {hr:02d}.{mn:02d} "
    else:
        return f" {mn:02d}.{sc:02d}.{ms:01d}"

def simulate_lap_time(dev, dev_info):
    # Simulate lap time display
    print("Simulate the lap time (1:12.542)")
    max_time = 72.542
    start_time = time.time()

    if not is_full_version:
        print("**Limited** charset in Lite Version - Use the Full Version")

    if dev_info["max_digits"] == 6:
        dev.set_left_panel("  LAP ")
                     
        dev.set_right_panel("-:--.---")
    if dev_info["max_digits"] == 4:
        dev.set_left_panel("LAP ")
        dev.set_right_panel("-:--.-")
    if dev_info["max_digits"] == 3:
        dev.set_central_panel("---")
    dev.set_gear(" ")
    dev.show_me()

    while True:
        current_time = (time.time() - start_time) + 59
        if current_time >= max_time:
            break

        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        milliseconds = int((current_time * 1000) % 1000)

        lap_time_str = time_to_7seg_string(minutes, seconds, milliseconds)

        if dev_info["max_digits"] == 6:
            dev.set_left_panel("  LAP ")
            dev.set_right_panel(lap_time_str)    
                         
        if dev_info["max_digits"] == 4:
            dev.set_left_panel("LAP ")
            dev.set_right_panel(lap_time_str)
        if dev_info["max_digits"] == 3:
            dev.set_central_panel(lap_time_str)
        dev.show_me()

        elapsed_ticks = time.time() - start_time
        time.sleep(max(0.0, (elapsed_ticks - current_time)))

def check_charset(dev, dev_info):
    # Check and display character set on the device
    if is_full_version:
        print("Test charset (full version) on panel display and gear")
        words = ["ABS", "GrOUP", "PIt", "bAtt", "FUEL", "CHArG", "StOP", "LAP", "SPEEd", "tEMP", "OIL", "Err", "LO", "HI", "CLr", "On", "OFF", "GO", "rdy", "End"]
        words_3chars = ["ABS", "LAP", "PIT", "OIL", "TMP", "BAT", "SPD", "FUE", "ON ", "OFF", "END", "GO ", "ERR", "HI ", "LO ", "CLr", "RDY", "AIR", "ENG", "TRN"]

        if dev_info["max_digits"] == 6:
            for word in words:
                centered = word.center(dev_info["max_digits"])
                dev.set_left_panel(centered)
                dev.set_right_panel(centered)
                dev.show_me()
                time.sleep(0.2)

        if dev_info["max_digits"] == 4:
            for word in words_3chars:
                centered = word.center(dev_info["max_digits"])
                dev.set_left_panel(centered)
                dev.set_right_panel(centered)
                dev.show_me()
                time.sleep(0.2)

        if dev_info["max_digits"] == 3:
            for word in words_3chars:
                centered = word.center(dev_info["max_digits"])
                dev.set_central_panel(centered)
                dev.show_me()
                time.sleep(0.2)
    else:
        print("Skip charset test on panel display in lite version")

    if dev_info["is_gear_present"] > 0:
        max_num = 154 if is_full_version else 10
        for i in range(max_num):
            ch = chr(i)
            try:
                if dev_info["max_digits"] > 3:
                    dev.set_left_panel(" Char ")
                    dev.set_right_panel(f"  {i:03d} ")
            
                dev.set_gear(i)
                dev.show_me()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")

def initialize_brightness(dev, dev_info):
    # Initialize brightness
    if not is_full_version:
        print("Skip brightness initialization on lite version")
        return
    
    if dev_info["max_brightness"] >= 100:
        if "ftec" in dev_info["name"]:
            brightness_level = 100
        else:
            brightness_level = 200
        dev.set_brightness(brightness_level)

def initialize_gear(dev, dev_info):
    # Initialize gear
    if dev_info["is_gear_present"] > 0:
        dev.set_gear("-")
        dev.show_me()

def test_rpm_leds(dev, dev_info):
    # Test RPM LEDs
    for i in range(1, dev_info["max_rpm_leds"] + 1):
        dev.set_rpm_led(i, 1)
        if dev_info["is_gear_present"] > 0:
            if i <= 9:
                dev.set_gear(i, True)
            else:
                dev.set_gear(i - 10, True)
        dev.show_me()
        time.sleep(0.2)

    for i in range(dev_info["max_rpm_leds"], 0, -1):
        dev.set_rpm_led(i, 0)
        if dev_info["is_gear_present"] > 0:
            if i <= 9:
                dev.set_gear(i, True)
            else:
                dev.set_gear(i - 10, True)
        dev.show_me()
        time.sleep(0.2)

def test_brightness(dev, dev_info):
    # Test brightness
    if dev_info["max_brightness"] > 0 and is_full_version:
        dev.set_brightness(dev_info["max_brightness"])
        if dev_info["is_gear_present"] > 0:
            dev.set_gear("_", True)
            dev.show_me()

        print("Decrease Brightness...")
        for i in range(dev_info["max_brightness"], 0, -1):
            if dev_info["max_digits"] == 3:
                dev.set_central_panel(f"{i:03d}")
            elif dev_info["max_digits"] == 4:
                dev.set_left_panel(f"{i:03d} ")
                dev.set_right_panel("DOWN")
            elif dev_info["max_digits"] == 6:
                dev.set_left_panel(f"  {i:03d} ")
                dev.set_right_panel("888888")
            dev.set_brightness(i)
            dev.show_me()
            time.sleep(0.01)

        time.sleep(1)

        if dev_info["is_gear_present"] > 0:
            if "z3sli" in dev_info["name"]:
                dev.set_gear(chr(126), True)
            else:
                dev.set_gear("-", True)
            dev.show_me()

        print("Increase Brightness...")
        for i in range(1, dev_info["max_brightness"] + 1):
            if dev_info["max_digits"] == 3:
                dev.set_central_panel(f"{i:03d}")
            elif dev_info["max_digits"] == 4:
                dev.set_left_panel(f"{i:03d} ")
                dev.set_right_panel(" UP ")
            elif dev_info["max_digits"] == 6:
                dev.set_left_panel(f"  {i:03d} ")
                dev.set_right_panel("--UP--")
            dev.set_brightness(i)
            dev.show_me()
            time.sleep(0.01)

        if "ftec" in dev_info["name"]:
            dev.set_brightness(100)
        else:
            dev.set_brightness(200)

    clear_display(dev, dev_info)

def test_warning_leds(dev, dev_info):
    # Test warning/FLAG LEDs
    if dev_info["max_warn_leds"] > 0:
        print("Warning/FLAG LED...")
        mwl = dev_info["max_warn_leds"] // 2
        for i in range(1, mwl + 1):
            dev.set_warning_led(i, 1)
            dev.set_warning_led((dev_info["max_warn_leds"] + 1) - i, 1)
            dev.show_me()
            time.sleep(0.4)
        for i in range(1, mwl + 1):
            dev.set_warning_led((mwl + 1) - i, 0)
            dev.set_warning_led(mwl + i, 0)
            dev.show_me()
            time.sleep(0.4)

def test_external_leds(dev, dev_info):
    # Test external/optinal LEDs
    if dev_info["max_ext_leds"] > 0 and is_full_version:
        print("External LED...")
        for i in range(1, dev_info["max_ext_leds"] + 1):
            dev.set_external_led(i, 1)
            dev.show_me()
            time.sleep(0.4)
        for i in range(dev_info["max_ext_leds"], 0, -1):
            dev.set_external_led(i, 0)
            dev.show_me()
            time.sleep(0.4)
    else:
        if "sliftec" not in dev_info["name"]: print("Skip External LED test in lite version")

def test_rumble_motors(dev, dev_info):
    # Test rumble/rim motors
    if dev_info["max_rumble_motor"] == 2 and is_full_version:
        print("Alternate Rim Motors")
        for i in range(0, 10):
            if i % 2 == 0:
                dev.load_rumble_motor(1, 255)
                dev.load_rumble_motor(2, 0)
            else:
                dev.load_rumble_motor(2, 255)
                dev.load_rumble_motor(1, 0)
            dev.show_me()
            time.sleep(0.5)
        dev.load_rumble_motor(1, 0)
        dev.load_rumble_motor(2, 0)
        dev.show_me()
    else:
        if "sliftec" in dev_info["name"]: print("Skip Rumble motors test in lite version")

def initialize_panels(dev, dev_info):
    # Initialize panel displays
    if dev_info["max_digits"] == 3:
        dev.set_central_panel("888")
    elif dev_info["max_digits"] == 4:
        dev.set_left_panel("8888")
        dev.set_right_panel("-Z3-")
    elif dev_info["max_digits"] == 6:
        dev.set_left_panel("888888")
        dev.set_right_panel(" ZCubE")
    dev.show_me()


def run_all_functions(dev, dev_info):
    stop_event, t = start_input_thread(dev, dev_info["name"], dev_info["buttons"])

    initialize_brightness(dev, dev_info)
    initialize_gear(dev, dev_info)
    test_rpm_leds(dev, dev_info)
    toggle_rpm_leds(dev, dev_info, 1)
    time.sleep(0.1)
    initialize_panels(dev, dev_info)
    time.sleep(0.25)
    test_brightness(dev, dev_info)
    test_warning_leds(dev, dev_info)
    test_external_leds(dev, dev_info)
    toggle_all_leds(dev, dev_info, 0)
    test_rumble_motors(dev, dev_info)
    simulate_lap_time(dev, dev_info)
    check_charset(dev, dev_info)
    clear_display(dev, dev_info)

    if not thread_down and is_full_version:
        stop_event.set()
        t.join()

    if is_full_version:
        dev.stop_input_listener()

    dev.terminate()

def main():
    # Main function to run the device test
    isDev1 = initialize_device(dev_unit1)
    if isDev1:
        global device_info, device2_info, is_full_version
        device_info = get_device_info(dev_unit1)
        if "_lite" not in device_info["name"]:
            is_full_version = True

        # Create thread for the device
        thread1 = threading.Thread(target=run_all_functions, args=(dev_unit1, device_info,))
 
        # Start the thread
        thread1.start()

        # Wait for thread to finish
        thread1.join()

        print("Test Done!")

if __name__ == "__main__":
    main()
