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

# RETRANSMISSION (WRONG)
def calculate_collision_and_retransmission():
    # Input values from the user
    frame_size_bytes = int(input("Enter the frame size (in bytes): "))  # Size of the frame
    propagation_delay_bit_times = int(input("Enter the propagation delay (in bit times): "))  # Propagation delay

    # Constants
    frame_size_bits = frame_size_bytes * 8  # Convert bytes to bits

    # Collision detection time
    collision_detection_time = propagation_delay_bit_times  # Time when both nodes detect the collision

    # When A starts retransmission
    # A will start retransmission after detecting the collision
    retransmission_start_A = collision_detection_time + frame_size_bits + propagation_delay_bit_times

    # When B starts retransmission
    # B will detect the collision after it has transmitted its frame and the signal has propagated back
    retransmission_start_B = collision_detection_time + frame_size_bits + propagation_delay_bit_times

    # Print results
    print(f"{collision_detection_time},{retransmission_start_A},{retransmission_start_B}")

# ETHERNET PROBABILITY (WRONG)
def ethernet_probability():
    num_nodes = int(input("Enter the num of nodes: "))
    k = int(input("Num of nodes that sense the channel again: "))
    p = k / num_nodes

    probability = comb(num_nodes, k) * (p ** k) * ((1 - p) ** (num_nodes - k))

    print(f"round{probability, 1}")

question = int(input("Which question?\n 1 = Cyclic Redundancy\n 2 = Effective Throughput Rate\n 3 = Retransmission\n"))
if question == 1:
    calculate_crc()

elif question == 2:
    calculate_effective_throughput()

elif question == 3:
    calculate_collision_and_retransmission()

elif question == 4:
    ethernet_probability()