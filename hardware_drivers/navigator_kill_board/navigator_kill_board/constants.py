'''
Navigator's kill board communicates over serial using the hex codes listed below.

This should be the same as the codes on:
    http://docs.mil.ufl.edu/pages/viewpage.action?spaceKey=NAV&title=Kill+Communication+Commands

The board can operate both in a request / response way, or it can be
periodically pinged and will respond with many bytes indicating the status
of all addresses.

For the ping/Async method, send PING, than continue to read the buffer
and parse the various response bytes below.

For the sync / request method, send the REQUEST byte for whatever addresses you
are interested in, then read a 1 byte response for either RESPONSE_FALSE or RESPONSE_TRUE

The computer can also command a kill (for example, if ROS notices a criticaly low battery)
by sending the COMPUTER.KILL.REQUEST and undone with COMPUTER.CLEAR.REQUEST
'''
constants = {
    'TIMEOUT_SECONDS': 8.0,  # How often board must be pinged to not set REMOTE to True
                             # Note: not official documented, this is just a guess
    'RESPONSE_FALSE': '\x00',  # True status for synchronous requests of individual addresses
    'RESPONSE_TRUE': '\x01',   # False status for synchronous requests of individual addresses

    'PING': {
        'REQUEST': '\x20',
        'RESPONSE': '\x30'
    },

    'KILLS': ['OVERALL', 'BUTTON_FRONT_PORT', 'BUTTON_AFT_PORT', 'BUTTON_FRONT_STARBOARD',\
              'BUTTON_AFT_STARBOARD', 'REMOTE', 'COMPUTER'],
    'OVERALL': {  # Should be True if any of the over are True
        'REQUEST': '\x21',
        'TRUE': '\x10',
        'FALSE': '\x11'
    },
    'BUTTON_FRONT_PORT': {
        'REQUEST': '\x22',
        'TRUE': '\x12',
        'FALSE': '\x13'
    },
    'BUTTON_AFT_PORT': {
        'REQUEST': '\x23',
        'TRUE': '\x14',
        'FALSE': '\x15'
    },
    'BUTTON_FRONT_STARBOARD': {
        'REQUEST': '\x24',
        'TRUE': '\x16',
        'FALSE': '\x17'
    },
    'BUTTON_AFT_STARBOARD': {
        'REQUEST': '\x25',
        'TRUE': '\x18',
        'FALSE': '\x19'
    },
    'REMOTE': {  # Will return True if board is not pinged often enough
        'REQUEST': '\x26',
        'TRUE': '\x1A',
        'FALSE': '\x1B'
    },
    'COMPUTER': {  # Allows board to be killed over serial (like through ROS)
        'KILL': {
            'REQUEST': '\x45',
            'RESPONSE': '\x55'
        },
        'CLEAR': {
            'REQUEST': '\x46',
            'RESPONSE': '\x56'
        },
        'REQUEST': '\x27',
        'TRUE': '\x1C',
        'FALSE': '\x1D'
    },
    'CONNECTED': {
        'TRUE': '\x1E',
        'FALSE': '\x1F'
    },
    'LIGHTS': {  # Note: YELLOW turns off GREEN and visa versa
        'OFF_REQUEST': '\x40',
        'OFF_RESPONSE': '\x50',
        'YELLOW_REQUEST': '\x41',
        'YELLOW_RESPONSE': '\x51',
        'GREEN_REQUEST': '\x42',
        'GREEN_RESPONSE': '\x52',
    },
    'CONTROLLER': '\xA0',  # Signifies the start of a controller message (joysticks & buttons)
                           # Immediately followed by 8 bytes: 6 joystick bytes, 2 button bytes
                           # Joystick message is 3 signed ints from -2048 to 2047
                           # Button message is 16 bits signifying up to 16 buttons on/off
    'CTRL_STICKS': ['UD', 'LR', 'TQ'],  # Up/Down, Left/Right, Torque
    'CTRL_BUTTONS': ['X', 'Y', 'A', 'B', 'DL', 'DR', 'START'],
    'CTRL_BUTTONS_VALUES': {  # Amount of buttons and labels will be changed in the future
                              # This currently mimics xbox controller labels and numbering
        'X': '\x00\x04',  # Button 2
        'Y': '\x00\x08',  # Button 3
        'A': '\x00\x01',  # Button 0
        'B': '\x00\x02',  # Button 1
        'DL': '\x08\x00',  # Dpad Left (Button 11)
        'DR': '\x10\x00',  # Dpad Right (Button 12)
        'START': '\x00\x80',  # Start (Button 7)
    }
}
