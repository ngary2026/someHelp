from math import comb

# CYCLIC REDUNDANCY (CORRECT)
def calculate_crc():
    """
    Calculate the CRC for given data and generator.
    :param data: Original data as a string of bits
    :param generator: Generator polynomial as a string of bits
    :return: Total bits sent, CRC bits, and all bits sent
    """
    data = input("Enter the original data (binary string): ")
    generator = input("Enter the generator polynomial (binary string): ")

    # Degree of generator
    degree = len(generator) - 1

    # Append zeros to the data equal to the degree of the generator
    padded_data = data + '0' * degree

    # Convert strings to lists for bitwise operations
    padded_data = list(padded_data)
    generator = list(generator)

    # Perform modulo-2 division (XOR) to get the remainder (CRC)
    for i in range(len(data)):  # Process only up to the original data length
        if padded_data[i] == '1':  # Only XOR when the bit is 1
            for j in range(len(generator)):
                padded_data[i + j] = str(int(padded_data[i + j]) ^ int(generator[j]))

    # Remainder is the last 'degree' bits of the padded_data
    crc = ''.join(padded_data[-degree:])

    # Final transmitted data is the original data + CRC
    transmitted_data = data + crc

    # Total bits sent
    total_bits = len(transmitted_data)

    # Output the results
    print(f"Total Bits Sent: {total_bits}")
    print(f"CRC Bits: {crc}")
    print(f"All Bits Sent: {transmitted_data}")
    print("\n")
    print(f"{total_bits},{crc},{transmitted_data}")

# EFFECTIVE THROUGHPUT RATE (CORRECT)
def calculate_effective_throughput():
    # Input values from the user
    num_nodes = float(input("Enter the number of nodes: "))
    transmission_rate_mbps = float(input("Enter the transmission rate (in Mbps): ")) * 10**6
    token_size_bytes = float(input("Enter the token size (in bytes): ")) * 8
    max_data_bytes = float(input("Enter the maximum data a node can transmit (in bytes): ")) * 8
    effective_throughput = float(input("Q3: Enter the effective throughput rate (in Mbps): ")) * 10**6

    #Part A
    Time_Transmit_Token_Node = token_size_bytes / transmission_rate_mbps
    Time_Data_Transmission_Round = max_data_bytes / transmission_rate_mbps
    Time_Token_Passing = num_nodes * Time_Transmit_Token_Node
    Throughput_Rate = max_data_bytes / (Time_Data_Transmission_Round + Time_Token_Passing)
    Throughput_Rate = Throughput_Rate/10**6

    #Part B
    Time_Data_Transmission_Round = max_data_bytes * num_nodes / transmission_rate_mbps
    Time_Token_Passing = num_nodes * Time_Transmit_Token_Node
    Throughput_Rate_B = (max_data_bytes * num_nodes) / (Time_Data_Transmission_Round + Time_Token_Passing)
    Throughput_Rate_B = Throughput_Rate_B/10**6

    #Part C
    Min_Number_Bytes = (token_size_bytes/8 * effective_throughput) / (transmission_rate_mbps - effective_throughput)

    print(f"{round(Throughput_Rate, 1)}, {round(Throughput_Rate_B, 1)}, {round(Min_Number_Bytes, 1)}")

# RETRANSMISSION (CORRECT)
def calculate_collision_and_retransmission():
    # Get inputs from the user
    propagation_delay = int(input("Enter the propagation delay (in bit times): "))
    frame_size = int(input("Enter the frame size (in bytes): ")) * 8
    Ethernet_Bus = 100 * 10**6

    t = 0

    #Works for Ethernet Bus = 100 Mbps

    #Part A
    print(propagation_delay)

    #Part B
    Time = t #A and B start transmitting
    Time += propagation_delay #Detect Collision
    Time += 48 #A and B Jam Signal
    Time2 = Time
    Time += propagation_delay #B's last jam signal at A, A detects idle channel
    Time += (96) #A starts retransmission, channels needs to be idle for 96 bit times before B can retransmit. Now, if B senses signal on or before Time2 + 512 + 96, it will not retransmit
    print(Time)

    #Part C
    Time += propagation_delay #A's retransmission signals reaches B
    if Time < Time2 + 512 + 96:
        Time += frame_size #B detects idle channel after A retransmission signal arrives at B
        Time += 96 #B behind transmission
        print(Time)

    else:
        print(Time) #B behind transmission

# ETHERNET PROBABILITY (CORRECT)
def ethernet_probability():
    # Get inputs from the user
    num_nodes = int(input("Enter the number of nodes: "))
    failed_attempts = int(input("Enter the number of consecutive failed attempts: "))
    target_nodes = int(input("Enter the number of nodes to sense the channel again (x): "))

    # Calculate the probability of any single node sensing the channel again
    # After `failed_attempts` consecutive failed attempts, backoff window is 2^failed_attempts.
    backoff_window = 2 ** failed_attempts
    p = 1 / backoff_window  # Probability of a single node sensing the channel

    # Calculate the probability that exactly one node senses the channel
    # Formula: P(exactly x) = (C(n, x) * p^x * (1-p)^(n-x))
    # For x = 1: C(n, 1) * p^1 * (1-p)^(n-1)
    from math import comb
    probability = comb(num_nodes, target_nodes) * (p ** target_nodes) * ((1 - p) ** (num_nodes - target_nodes))

    # Round the result to 3 decimal places
    probability_rounded = round(probability, 3)

    # Print the result
    print(f"{probability_rounded:.3f}")

# IP AND MAC ADDRESS (Yea idk yet)
def simulate_network_frames():
    # User inputs IP and MAC tables
    def get_network_table():
        print("Enter the network table (Interface, IP Address, MAC Address). Type 'done' when finished:")
        network_table = {}
        while True:
            entry = input("Interface, IP Address, MAC Address: ").strip()
            if entry.lower() == "done":
                break
            interface, ip, mac = entry.split()
            network_table[interface.strip()] = (ip.strip(), mac.strip())
        return network_table

    def resolve_frames(network_table, source, dest):
        frames = []
        
        # Step 1: Check if ARP is needed, broadcast to resolve MAC address
        if source[1] != dest[1]:  # If the MAC address is different
            # ARP Request Frame (broadcast)
            frames.append(f"0,0,{source[1]},FF-FF-FF-FF-FF-FF")
            # ARP Reply Frame (target responds with MAC address)
            frames.append(f"0,0,{dest[1]},{source[1]}")

        # Step 2: Create data frame for IP packet transmission
        frames.append(f"{source[0]},{dest[0]},{source[1]},{dest[1]}")
        
        return frames

    network_table = get_network_table()
    
    # User input for source and destination interfaces
    source_interface = input("Enter source interface (e.g., B): ").strip()
    dest_interface = input("Enter destination interface (e.g., F): ").strip()

    source = network_table[source_interface]
    dest = network_table[dest_interface]
    
    # Step 1: Frames from source to destination (B -> F)
    frames_from_source_to_dest = resolve_frames(network_table, source, dest)
    
    # Now resolve frames from destination to another interface (F -> E)
    source_interface2 = input("Enter next source interface (e.g., F): ").strip()
    dest_interface2 = input("Enter next destination interface (e.g., E): ").strip()
    
    source2 = network_table[source_interface2]
    dest2 = network_table[dest_interface2]
    
    # Step 2: Frames from F to E
    frames_from_source2_to_dest2 = resolve_frames(network_table, source2, dest2)
    
    # Combine all frames
    all_frames = frames_from_source_to_dest + frames_from_source2_to_dest2
    
    # Print all frames in order
    print("\nFrames received at destination interface:")
    for frame in all_frames:
        print(frame)

question = int(input("Which question?\n 1 = Cyclic Redundancy\n 2 = Effective Throughput Rate\n 3 = Retransmission\n 4 = Ethernet Bus Probability\n 5 = IP MAC ARP Switching\n"))
if question == 1:
    calculate_crc()

elif question == 2:
    calculate_effective_throughput()

elif question == 3:
    calculate_collision_and_retransmission()

elif question == 4:
    ethernet_probability()

elif question == 5:
    simulate_network_frames()
