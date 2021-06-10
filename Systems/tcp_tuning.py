"""
Date: 2020-06-09
Summary: The tcp_tuning.py provides the recommended system settings to get the 
maximum bandwidth from your network.
"""

def tcp_tuning():
    warning_screen = """
    ==================================================================================
    | WARNING: This works only on Linux, UNIX, and AIX systems. Run command          |
    |                                                                                |
    | sudo sysctl -a | egrep "[wr]mem" | egrep "core|tcp"                            |
    |                                                                                |
    | so you have a backup to restore the system to its original state.              |
    ==================================================================================
    """
    print(warning_screen)
    
    """ Provide display options and user to pick one. """
    opt1 = "1. I know my network speed."
    opt2 = "2. I know my system window size."

    print(f"Please selection option 1 or 2: \n{opt1}\n{opt2}\n")

    user_input = int(input("Option: "))

    try:
        if user_input == 1:
            """
            Calculate system window size base on network speed and latency.
            Window Size in Byte = Speed * 10^6 / 8 * Latency / 1000
            """
            try:
                net_speed = int(input("What is your network speed in Mbit/second: "))
                net_delay = int(input("What is your network latency in milliseconds: "))
                cal_win = int(net_speed * 10**6 / 8 * net_delay / 1000)
                print()
                print(f'"{cal_win}" Bytes is the Window Size for the network speed of "{net_speed} Mbits/sec" and "{net_delay}" milliseconds latency.')
                print("-" * 100)
                print("Recommended Commands to Change Your System Settings:")
                print("<Unchange> means do not modify this value.\n")
                print(f'sudo sysctl -w net.ipv4.tcp_wmem="<Unchange>    <Unchange>   {cal_win}"')
                print(f'sudo sysctl -w net.core.wmem_max={cal_win * 4}')
                print(f'sudo sysctl -w net.ipv4.tcp_wmem="<Unchange>    <Unchange>   {cal_win}"')
                print(f'sudo sysctl -w net.core.wmem_max={cal_win * 4}')
                print("-" * 100)
            except ValueError:
                print("Please enter a whole number with no comma or period.")
        elif user_input == 2:
            """
            Calculate network speed base on system window size and latency.
            Speed in Mbit/sec = Window Size * 8 / Latency / 1000
            """
            try:
                window = int(input("What is your system window size: "))
                net_delay = int(input("What is your network latency in milliseconds: "))
                cal_speed_bit = int(window * 8 / net_delay / 1000)
                # cal_speed_byte = int(window / net_delay / 1000)
                print()
                print(f'"{cal_speed_bit} Mbits/sec" is the maximum network speed for Window Size "{window}" bytes with "{net_delay}" milliseconds latency.')
            except ValueError:
                print("Please enter a whole number with no comma or period.")
        else:
            print("Exist Program ...")
            pass

    except ValueError:
        """ Error handling to catch non-integer 1 or 2 """
        print("Please enter number 1 or 2.")


if __name__ == "__main__":
    test = tcp_tuning()
