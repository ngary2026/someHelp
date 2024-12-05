# # This is for Li's Homework 1, read the questions and run the code, everything will work out after
# ###### WE GOT THIS ######
import math
import numpy as np
from decimal import Decimal

###### ISP & PROBABILITY ######
def binomial_probability(n, k, p):
        return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

# Function to calculate the probability that at least N users are accessing the network
def probability_at_least_N(n, N, p):
    P_less_than_N = sum(binomial_probability(n, k, p) for k in range(N))
    return 1 - P_less_than_N

# Function to calculate binomial coefficient (n choose k)
def binomial_coefficient(n, k):
    return math.comb(n, k)

# Function to calculate binomial probability for P(X = k)
def ISP_Problem():
    # Ask the user for all input values at once
    total_bandwidth = float(input("Enter the total bandwidth of the network (in Mbps): \n"))
    user_bandwidth = float(input("Enter the bandwidth each user requires when active (in Mbps): \n"))
    user_activity_percentage = float(input("Enter the percentage of time each user is active (as a decimal): \n"))
    num_users_part2 = int(input("Enter the total number of users subscribed to the network for part 2: \n"))
    p_access = float(input("Enter the probability that a user is accessing the network (as a decimal): \n"))
    num_users_part3 = int(input("Enter the total number of users subscribed to the network for part 3: \n"))
    target_probability = float(input("Enter the target congestion-free probability for part 4 (as a decimal, e.g., 0.9999): \n"))

    # Part 1: Calculate maximum number of users for given bandwidth
    active_bandwidth_per_user = user_bandwidth  # No need to scale by active percentage here
    max_num_users = int(total_bandwidth // active_bandwidth_per_user)

    # Part 2: Probability calculations with 26 users (example data)
    P_no_user = (1 - p_access) ** num_users_part2
    P_one_particular_user = p_access
    P_exactly_one_user = binomial_coefficient(num_users_part2, 1) * (p_access ** 1) * ((1 - p_access) ** (num_users_part2 - 1))
    P_two_particular_users = p_access ** 2
    P_exactly_two_users = binomial_coefficient(num_users_part2, 2) * (p_access ** 2) * ((1 - p_access) ** (num_users_part2 - 2))

    # Part 3: Probability of congestion with 100 users (N from part 1 + 1)
    N_part3 = max_num_users + 1  # max_num_users was 17, so N is 18
    P_at_least_N_part3 = probability_at_least_N(num_users_part3, N_part3, p_access)

    # Part 4: Maximum number of users for target congestion-free probability
    N_max = 1
    congestion_probability = 1 - target_probability
    while True:
        P_at_least_N_max = probability_at_least_N(N_max, N_max, p_access)
        if P_at_least_N_max <= congestion_probability:
            break
        N_max += 1

    # Output all answers in the requested format
    print(f"{max_num_users:.0f},{P_no_user:.5f},{P_one_particular_user:.5f},{P_exactly_one_user:.5f},{P_two_particular_users:.5f},{P_exactly_two_users:.5f},{P_at_least_N_part3:.5f},{N_max:.0f}")
    

##### END TO END ##### (CORRECT)
def end_to_end_delay():
  packet_size = int(input("Packet size: ")) # bytes
  propagation_speed = float(input("\n Propagation speed: ")) * 10**8 # m/s (input float only)
  transmission_rate_1 = int(input("\n Transmission rate of 1st link: ")) # Mbps
  transmission_rate_2 = int(input("\n Transmission rate of 2nd link: ")) # Mbps
  router_processing = int(input("\n Packet processing time on router: ")) # microseconds per kilobyte
  link_1 = int(input("\n Length of 1st link: ")) # km
  link_2 = int(input("\n Length of 2nd link: ")) # km 

  transmission_delay_1 = (packet_size * 8) / (transmission_rate_1 * 10**6) * 10**6
  rounded_transmission_delay_1 = round(transmission_delay_1, 1)
  print(f"Transmission delay 1: {rounded_transmission_delay_1}")

  propagation_delay_1 = (link_1 * 10**3) / (propagation_speed) * 10**6
  rounded_propagation_delay_1 = round(propagation_delay_1, 1)
  print(f"Propagation delay 1: {rounded_propagation_delay_1}")

  router_processing_delay = (packet_size / 1000) * router_processing
  rounded_router_processing_delay = round(router_processing_delay, 1)
  print(f"Router processing delay: {rounded_router_processing_delay}\n")

  first_link_delay = transmission_delay_1 + propagation_delay_1 + router_processing_delay
  rounded_first_link_delay = round(first_link_delay, 1)
  print(f"1) Total delay from source to router: {rounded_first_link_delay}\n")

  transmission_delay_2 = (packet_size * 8) / (transmission_rate_2 * 10**6) * 10**6
  rounded_transmission_delay_2 = round(transmission_delay_2, 1)
  print(f"Transmission delay 2: {rounded_transmission_delay_2}")

  propagation_delay_2 = (link_2 * 10**3) / (propagation_speed) * 10**6
  rounded_propagation_delay_2 = round(propagation_delay_2, 1)
  print(f"Propagation delay 2: {rounded_propagation_delay_2}\n")

  end_to_end_delay_1 = transmission_delay_1 + propagation_delay_1 + router_processing_delay + transmission_delay_2 + propagation_delay_2
  rounded_end_to_end_delay_1 = round(end_to_end_delay_1, 1)
  print(f"2) End-to-End delay of first packet: {rounded_end_to_end_delay_1}")

  x = transmission_delay_2 - transmission_delay_1
  # formula: total_delay + ((n - 1) * x)
  end_to_end_delay_2 = end_to_end_delay_1 + ((2 - 1) * x)
  rounded_end_to_end_delay_2 = round(end_to_end_delay_2, 1)
  print(f"3) End-to-End delay of second packet: {rounded_end_to_end_delay_2}")

  end_to_end_delay_3 = end_to_end_delay_1 + ((3 - 1) * x)
  rounded_end_to_end_delay_3 = round(end_to_end_delay_3, 1)
  print(f"4) End-to-End delay of third packet: {rounded_end_to_end_delay_3}")

  end_to_end_delay_100 = end_to_end_delay_1 + ((100 - 1) * x)
  rounded_end_to_end_delay_100 = round(end_to_end_delay_100, 1)
  print(f"5) End-to-End delay of 100th packet: {rounded_end_to_end_delay_100}")

  print(f"{rounded_first_link_delay},{rounded_end_to_end_delay_1},{rounded_end_to_end_delay_2},{rounded_end_to_end_delay_3},{rounded_end_to_end_delay_100}")

##### SEGMENTATION ##### (Gets 3rd wrong?)
def calculate_packet_transfer():
    message_size = int(input("\n Message size: ")) # bytes
    bandwidth = int(input("\n Bandwidth: ")) * 10**3 # Kbps -> bps
    number_of_routers = int(input("\n Number of routers: "))
    number_of_links = number_of_routers + 1
    number_of_packets = int(input("\n Number of packets with segmentation: "))
    bit_error_probability = 10 ** -5

    '''
    Solution 1: Total time without segmentation
    '''

    # Find message size in bits
    message_size_bits = message_size * 8
    # Find transmission time per link
    transmission_time = message_size_bits / bandwidth
    # Find total time across all links (store-and-forward)
    total_time = number_of_links * transmission_time
    rounded_total_time = round(total_time, 2)

    print(f"Time to move message from source to destination: {rounded_total_time}")

    '''
    Solution 2a: Total time with segmentation into X packets
    '''

    # Find time to move the whole message
    # Find packet size without headers
    packet_size = message_size_bits / number_of_packets
    # Find Transmission Time per Link per Packet
    transmission_time_per_packet = packet_size / bandwidth
    # Find Total Time Across All Links per Packet (Store-and-Forward)
    total_time_with_segmentation = number_of_links * transmission_time_per_packet
    # Find time for other packets to arrive
    total_time_for_other_packets = transmission_time_per_packet * (number_of_packets - 1)
    # Find overall total time
    overall_total_time = total_time_with_segmentation + total_time_for_other_packets
    rounded_overall_total_time = round(overall_total_time, 2)

    print(f"Time to move segmented message from source to destination: {rounded_overall_total_time}")

    '''
    Solution 2b: Minimum header size that eliminates benefit of segmentation
    '''

    header_size = ((total_time * bandwidth) / (number_of_links + number_of_packets - 1)) - packet_size

    print(f"\nMinimum header size that eliminates benefit of segmentation: {header_size}")

    '''
    Solution 3: Average number of retransmissions
    '''
    # Without message segmentation
    # Probability of successful transmission (no bit errors)
    exponent = (-1*message_size_bits) * bit_error_probability
    p_success = np.exp(exponent)
    # Expected number of transmissions
    transmissions = 1 / p_success
    # Average number of retransmissions
    avg_retransmissions = transmissions - 1
    rounded_avg_retransmissions = round(avg_retransmissions, 2)

    print(f"Average number of retransmissions: {rounded_avg_retransmissions}")

    # With message segmentation
    # Probability of successful transmission per packet
    exponent = (-1 * packet_size) * bit_error_probability
    p_success_pkt = np.exp(exponent)
    # Expected number of transmissions per packet
    transmissions_pkt = 1 / p_success_pkt
    # Average number of retransmissions
    avg_retransmissions_pkt = transmissions_pkt - 1
    total_avg_retransmissions = number_of_packets * avg_retransmissions_pkt
    rounded_total_avg_retransmissions = round(total_avg_retransmissions, 2)

    print(f"Average number of retransmissions: {rounded_total_avg_retransmissions}")

    print(f"\n{rounded_total_time},{rounded_overall_total_time},{round(header_size, 2)},{rounded_avg_retransmissions},{rounded_total_avg_retransmissions}")

##### PACKET LOSS ##### (CORRECT)
def calculate_packet_loss():
    pkt_size_in_bytes = int(input("Packet size: ")) # bytes
    # Convert packet size to bits for calculations
    s = pkt_size_in_bytes * 8 # There are 8 bits per byte
    propagation_speed = float(input("\nPropagation speed on both links: ")) * 10**8 # enter the main number only (leave 10^8 out)
    transmission_rate_1 = int(input("\nTransmission rate of first link: ")) # Mbps
    transmission_rate_2 = int(input("\nTransmission rate of second link: ")) # Mbps
    # Convert transmission rates to bits per second for calculations
    r_1 = transmission_rate_1 * 10**6
    r_2 = transmission_rate_2 * 10**6
    pkt_proc = int(input("\nPacket processing on router: ")) # microseconds per kilobyte
    length_1 = int(input("\nLength of first link: ")) # km
    length_2 = int(input("\nLength of second link: ")) # km
    buffer_size = int(input("\nRouter buffer size: ")) # MB

    # 1. Calculate fundamental parameters
    # Transmission times
    t_t1 = (s/r_1) * 10**6 # microsec
    t_t2 = (s/r_2) * 10**6 # microsec
    # Processing time at router
    t_proc = pkt_proc * (pkt_size_in_bytes/1000) # microsec

    # Print for debugging
    # print(f"Packet size in bits: {s} bits.\nTransmission rate for first link: {r_1} bps.\nTransmission rate for second link: {r_2} bps.\nTransmission time for first link: {t_t1} microseconds.\nTransmission time for second link: {t_t2} microseconds.\n Processing time at router: {t_proc} microseconds.")

    # 2. Determine key event times
    # Time when router starts transmitting the first packet
    t_start = t_t1 + t_proc # microsec

    # 3. Calculate the amount of data buffered at the router at time t >= t_start
    # Difference in transmission rates (delta_r)
    delta_r = r_1 - r_2 # bps
    # Convert delta_r to bits per microsec
    delta_r = delta_r / 10**6
    # print(f"\nDelta R: {delta_r}")
    # Calculate constant term c
    c = (r_2 * t_start) / 10**6 # bits
    # print(f"constant C: {c} bits")

    # 4. Calculate the earliest time when the available buffer space is zero
    # Total Buffer size b
    b = buffer_size * 8*10**6 # bits
    # print(f"buffer size: {b} bits")
    # Condition for available buffer space being zero

    t_microsecs = (b - c) / delta_r
    t_secs = t_microsecs / 10**6

    # print(t_secs)

    # 5. Number of packets received by the router at time t
    data_arrived = math.floor(r_1 * t_secs)

    # Number of packets received
    number_of_packets = math.ceil(data_arrived / s)
    print(f"\nThe first packet to be lost is packet number {number_of_packets}.")


# Run the function
question = int(input("Which question do you need? \n1 = ISP \n2 = Lost Packet \n3 = Segmentation \n4 = End to End Delay\n"))

if question == 1:
    ISP_Problem()

elif question == 2:
    calculate_packet_loss()

elif question == 3:
    calculate_packet_transfer()

elif question == 4:
    end_to_end_delay()

# import math
# ''' Problem 1 Solution '''

# # Change this the total bandwidth for you problem
# bandwidth = 160
# user_bandwidth = 8.9
# max_users = bandwidth // user_bandwidth
# print("Solution 1:")
# print(f"- Maximum number of users: {max_users}\n")
# ''' 
#   Problem 2 Solution 
#   THIS WILL ONLY GET YOU 6/8 POINTS
# '''
# # Number of users (CHANGE THIS FOR YOUR PROBLEM)
# n = 26

# # Probability of a single user accessing the network
# # User subscribed for {p} percent of time
# p = 0.15


# def binomial_coefficient(n, k):
#   return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


# def binomial_distribution(n, k):
#   return binomial_coefficient(n, k) * (p**k) * ((1 - p)**(n - k))


# # Calculate the probabilities
# probability_0_users = round(binomial_distribution(n, 0), 5)
# probability_1_user = 1 - probability_0_users
# probability_exactly_1_user = round(binomial_distribution(n, 1), 5)
# probability_2_users = 1 - probability_0_users + probability_exactly_1_user
# probability_exactly_2_users = round(binomial_distribution(n, 2), 5)

# # Print the results
# print("Solution 2:")
# print(
#     f"- Probability that no user is accessing the network: {probability_0_users}"
# )
# print(
#     f"- Probability that one particular user is accessing the network: {probability_1_user}"
# )
# print(
#     f"- Probability that exactly one user (any one) is accessing the network: {probability_exactly_1_user}"
# )
# print(
#     f"- Probability that two particular users are accessing the network: {probability_2_users}"
# )
# print(
#     f"- Probability that exactly two users (any two) are accessing the network: {probability_exactly_2_users}\n"
# )
# ''' Problem 3 Solution '''
# # Number of users (CHANGE THIS FOR PROBLEM 3)
# n_3 = 100


# def binomial_coefficient1(n_3, k):
#   return math.factorial(n_3) / (math.factorial(k) * math.factorial(n_3 - k))


# def calculate_probability1(N):
#   probability = 0
#   for k in range(0, N + 1):
#     probability += binomial_coefficient1(n_3, k) * (p**k) * (
#         (1 - p)**(n_3 - k))

#   probability = 1 - probability
#   return round(probability, 5)


# # Calculate the probability for at least 18 users accessing the network
# N = int(max_users) + 1
# probability_at_least_18_users = calculate_probability1(N)

# # Print the result
# print("Solution 3:")
# print(
#     f"- Probability that at least {N} users are accessing the network: {probability_at_least_18_users}\n"
# )
# ''' Problem 4 Solution '''
# low = N
# high = n_3
# while calculate_probability1(N) > 0.0001:
#   n_3 -= 1

# print("Solution 4:")
# print(f"- Maximum number of users for 99.99% congestion free: {n_3}")

# question = int(input("Which question?\n 1 = Selective Repeat Protocol\n 2 = Synack - 3 Parts\n 3 = Synack - 4 Parts\n 4 = TCP Procedure for Estimating RTT\n 5 = Ssthresh value\n"))
# if question == 1:
#     pass

# elif question == 2:
#     pass

# elif question == 3:
#     pass

# elif question == 4:
#     pass

# elif question == 5:
#     pass