"""
Date: 2020-06-09
Summary: The tcp_tuning.py provides the recommended system settings to get the 
maximum bandwidth from your network.
"""

def tcp_tuning():
    warning_screen = """
    ==================================================================================
    | WARNING: This works only on Linux, UNIX, and AIX systems. Run the command      | 
    | sudo sysctl -a | egrep "[wr]mem" | egrep "core|tcp"                            |
    | so you know your current system settings to restore it back to original state. |
    ==================================================================================
    """
    print(warning_screen)

    opt1 = "1. I know my network speed."
    opt2 = "2. I know my system window size."
    print(f"Please selection option 1 or 2: \n{opt1}\n{opt2}\n")

    user_input = int(input("Option: "))

    try:
        if user_input == 1:
            """
            Window Size in Byte = Speed * 10^6 / 8 * Latency / 1000

            """
            # print("I know my network speed.")
            try:
                net_speed = int(input("What is your network speed in Mbit/second: "))
                net_delay = int(input("What is your network latency in milliseconds: "))
                print(net_speed)
                print(type(net_speed))
                cal_win = int(net_speed * 10**6 / 8 * net_delay / 1000)
                print(cal_win)
            except ValueError:
                print("Please enter a whole number with no comma or period.")
        elif user_input == 2:
            print("I know my system window size.")
            try:
                window = int(input("What is your system window size: "))
                net_delay = int(input("What is your network latency in milliseconds: "))
                cal_speed = int(window * 8 / net_delay / 1000)
                print(cal_speed)
            except ValueError:
                print("Please enter a whole number with no comma or period.")
        else:
            exit()

    except ValueError:
        print("Please enter number 1 or 2.")

    # print(user_input)


a = tcp_tuning()
print(a)