from __future__ import print_function

import argparse
import random
import re
import subprocess
import sys
import time

import requests


PORTAL_URL = 'https://portal.reivernet.com/'


def set_mac(interface, mac):
    """Set `interface`'s MAC address to `mac`.

    Return False if an error occurred (permission denied).
    """
    try:
        subprocess.check_call(['ifconfig', interface, 'ether', mac])
    except subprocess.CalledProcessError:
        return False


def get_default_mac(interface):
    """Return the 'burned-in' MAC address."""
    output = subprocess.check_output(
        ['networksetup', '-getmacaddress', interface], universal_newlines=True)
    match_object = re.search(
        r'^Ethernet Address: ([\w:]+)'.format(interface), output)
    if match_object:
        return match_object.group(1)


def generate_mac(mac):
    """Return `mac` with the last 24 bits randomized."""
    # Split the MAC address into hexadecimal bytes.
    mac_bytes = mac.split(':')
    # Generate some random hex bytes.
    random_hex_bytes = [
        '{:02x}'.format(random.randint(0, 255)) for _ in range(3)]
    # Replace the last three MAC bytes with random bytes.
    return ':'.join(mac_bytes[:3] + random_hex_bytes)


def toggle_interface_status(interface):
    """Set `interface` down, then up."""
    time.sleep(1)
    subprocess.call(['ifconfig', interface, 'down'])
    time.sleep(1)
    subprocess.call(['ifconfig', interface, 'up'])


def change_mac(interface):
    """Modify `interface`'s MAC, then toggle `interface`."""
    default_mac = get_default_mac(interface)
    new_mac = generate_mac(default_mac)
    # Exit if permission was denied.
    if set_mac(interface, new_mac) is False:
        sys.exit('Could not set MAC address. Run with sudo.')
    toggle_interface_status(interface)
    print("Set {interface}'s MAC to {mac}".format(
        interface=interface, mac=new_mac))


def start_trial_session(guest_name, room_number):
    """Start a new Reivernet 30-minute trial session."""
    s = requests.Session()
    s.get(PORTAL_URL)
    s.get(PORTAL_URL, params='useLogin')
    s.post(PORTAL_URL, params={
        'guestname': guest_name,
        'room': room_number,
        'authUser': '',
        'portID': '1'
    })
    s.post(PORTAL_URL + 'Accept.php', params={
        'radio_plan': '17',
        'room': room_number,
        'guestname': guest_name,
        'reservation': '',
        'authUser': '',
        'Accept': 'accept',
        'connect_btn': 'Connect'
    })
    print('Logged in as {}, room {}.'.format(guest_name, room_number))


def renew_session(interface, guest_name, room_number):
    """Renew the internet session."""
    change_mac(interface)
    # Allow time for the interface to come back.
    time.sleep(10)
    start_trial_session(guest_name, room_number)


def main():
    # Parse command line arguments.
    parser = argparse.ArgumentParser(
        description='Renew Reivernet internet session.')
    parser.add_argument('interface', help='network interface')
    parser.add_argument('guest_name', help="registered guest's name")
    parser.add_argument('room_number', help="guest's room number")
    parser.add_argument('-a', '--auto', action='store_true',
                        help='automatically renew the session periodically')
    parser.add_argument('-m', '--minutes', default=28, type=int,
                        help='specify how many minutes to wait before '
                             'automatically renewing the session (default '
                             '%(default)s minutes)')
    args = parser.parse_args()
    interface = args.interface
    guest_name = args.guest_name
    room_number = args.room_number
    auto = args.auto
    minutes = args.minutes
    sleep_time = minutes * 60
    # Renew the session.
    renew_session(interface, guest_name, room_number)
    # If auto mode was enabled, renew the session periodically.
    if auto:
        print('Press Ctrl-C to exit.')
        try:
            while True:
                # Sleep for some time.
                print('Sleeping for {} minutes (until {}).'.format(
                    minutes, time.ctime(time.time() + sleep_time)))
                time.sleep(sleep_time)
                renew_session(interface, guest_name, room_number)
        except KeyboardInterrupt:
            print('Exiting.')


if __name__ == '__main__':
    main()
