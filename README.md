# auto-reivernet

Obtain unlimited free Reivernet sessions by MAC spoofing.

## Description

Reivernet provides free 30 minute Internet sessions. However, only one free
session is allowed per MAC address per 24 hours. By changing the MAC address,
the 24-hour restriction is bypassed.

This module randomizes the specified interface's MAC address. Then, the
Reivernet portal is logged into with the specified guest name and room
number. Finally, the free 30 minute plan is selected and submitted.

Optionally, the process can be automatically initiated periodically. That is,
as the free sessions expire.

Only Mac OS X is supported.

## Usage

Run with sudo, otherwise the MAC address cannot be changed.
The `auto_reivernet.py` module has the following arguments and options.

    usage: auto_reivernet.py [-h] [-a] [-m MINUTES]
                             interface guest_name room_number

    Renew Reivernet internet session.

    positional arguments:
      interface             network interface
      guest_name            registered guest's name
      room_number           guest's room number

    optional arguments:
      -h, --help            show this help message and exit
      -a, --auto            automatically renew the session periodically
      -m MINUTES, --minutes MINUTES
                            specify how many minutes to wait before automatically
                            renewing the session (default 28 minutes)

## Requirements

This module requires the Requests Python module.


