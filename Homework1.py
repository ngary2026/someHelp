# # This is for Li's Homework 1, read the questions and run the code, everything will work out after
# ###### WE GOT THIS ######

# ##### Question 1: An ISP has a packet-switched network of ___Mbps ..... #####
# import math
# def binomial_probability(n, k, p):
#         return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

# # Function to calculate the probability that at least N users are accessing the network
# def probability_at_least_N(n, N, p):
#     P_less_than_N = sum(binomial_probability(n, k, p) for k in range(N))
#     return 1 - P_less_than_N

# # Function to calculate binomial coefficient (n choose k)
# def binomial_coefficient(n, k):
#     return math.comb(n, k)

# # Function to calculate binomial probability for P(X = k)
# def ISP_Problem():
#     # Ask the user for all input values at once
#     total_bandwidth = float(input("Enter the total bandwidth of the network (in Mbps): \n"))
#     user_bandwidth = float(input("Enter the bandwidth each user requires when active (in Mbps): \n"))
#     user_activity_percentage = float(input("Enter the percentage of time each user is active (as a decimal): \n"))
#     num_users_part2 = int(input("Enter the total number of users subscribed to the network for part 2: \n"))
#     p_access = float(input("Enter the probability that a user is accessing the network (as a decimal): \n"))
#     num_users_part3 = int(input("Enter the total number of users subscribed to the network for part 3: \n"))
#     target_probability = float(input("Enter the target congestion-free probability for part 4 (as a decimal, e.g., 0.9999): \n"))

#     # Part 1: Calculate maximum number of users for given bandwidth
#     active_bandwidth_per_user = user_bandwidth  # No need to scale by active percentage here
#     max_num_users = int(total_bandwidth // active_bandwidth_per_user)

#     # Part 2: Probability calculations with 26 users (example data)
#     P_no_user = (1 - p_access) ** num_users_part2
#     P_one_particular_user = p_access
#     P_exactly_one_user = binomial_coefficient(num_users_part2, 1) * (p_access ** 1) * ((1 - p_access) ** (num_users_part2 - 1))
#     P_two_particular_users = p_access ** 2
#     P_exactly_two_users = binomial_coefficient(num_users_part2, 2) * (p_access ** 2) * ((1 - p_access) ** (num_users_part2 - 2))

#     # Part 3: Probability of congestion with 100 users (N from part 1 + 1)
#     N_part3 = max_num_users + 1  # max_num_users was 17, so N is 18
#     P_at_least_N_part3 = probability_at_least_N(num_users_part3, N_part3, p_access)

#     # Part 4: Maximum number of users for target congestion-free probability
#     N_max = 1
#     congestion_probability = 1 - target_probability
#     while True:
#         P_at_least_N_max = probability_at_least_N(N_max, N_max, p_access)
#         if P_at_least_N_max <= congestion_probability:
#             break
#         N_max += 1

#     # Output all answers in the requested format
#     print(f"{max_num_users:.0f},{P_no_user:.5f},{P_one_particular_user:.5f},{P_exactly_one_user:.5f},{P_two_particular_users:.5f},{P_exactly_two_users:.5f},{P_at_least_N_part3:.5f},{N_max:.0f}")
    
# ##### Question 2: In a packet switched network, a source host transmits packets of ___ bytes each... #####



# ##### Question 3: In modern packet-switched networks, the source host splits long application-layer messages.... #####
# def calculate_packet_transfer():
#     # Given values
#     message_size_bytes = int(input("Enter the message size in bytes (e.g., 6000): "))
#     link_speed_bps = int(input("Enter the link speed in kilobits per second (e.g., 220): ")) * 1e3
#     num_routers = int(input("Enter the number of routers (e.g., 3): "))
#     num_packets = int(input("Enter the number of packets for segmentation (e.g., 100): "))
#     corruption_probability = float(input("Enter the probability of bit corruption (e.g., 1e-5): "))

#     # Convert message size to bits
#     message_size_bits = message_size_bytes * 8

#     # 1. Total time without message segmentation
#     transmission_time_no_segmentation = message_size_bits / link_speed_bps
#     total_time_no_segmentation = (num_routers + 1) * transmission_time_no_segmentation

#     # 2. Total time with message segmentation
#     packet_size_bytes = message_size_bytes / num_packets
#     packet_size_bits = packet_size_bytes * 8
#     transmission_time_per_packet = packet_size_bits / link_speed_bps
#     total_time_with_segmentation = (num_routers + 1) * num_packets * transmission_time_per_packet

#     # 3. Minimum header size to eliminate the benefit of segmentation
#     # Solve for h in 4 * 100 * (480 + h) / link_speed_bps = total_time_no_segmentation
#     h = (total_time_no_segmentation * link_speed_bps / (num_routers + 1) / num_packets) - packet_size_bits

#     # 4. Average number of retransmissions needed
#     average_retransmissions_no_segmentation = 1 / (1 - corruption_probability)
#     average_retransmissions_with_segmentation = num_packets * average_retransmissions_no_segmentation

#     # Round results
#     total_time_no_segmentation = round(total_time_no_segmentation, 2)
#     total_time_with_segmentation = round(total_time_with_segmentation, 2)
#     h = round(h)
#     average_retransmissions_no_segmentation = round(average_retransmissions_no_segmentation)
#     average_retransmissions_with_segmentation = round(average_retransmissions_with_segmentation)

#     # Prepare output
#     output = f"{total_time_no_segmentation},{total_time_with_segmentation},{h},{average_retransmissions_no_segmentation},{average_retransmissions_with_segmentation}"
#     print(output)

# ##### Question 4: In a packet switched network, ... which packet is the first one to be lost? #####
# def calculate_packet_loss():
#     # Get inputs from the user
#     packet_size = int(input("Enter the packet size in bytes (e.g., 1400): "))
#     propagation_speed = float(input("Enter the propagation speed in m/s (e.g., 1.9e8): "))
#     transmission_rate_first_link = float(input("Enter the transmission rate of the first link in Mbps (e.g., 180): ")) * 1e6
#     transmission_rate_second_link = float(input("Enter the transmission rate of the second link in Mbps (e.g., 130): ")) * 1e6
#     processing_delay_per_kb = float(input("Enter the processing delay per kilobyte in microseconds (e.g., 5): ")) * 1e-6
#     length_first_link_km = float(input("Enter the length of the first link in km (e.g., 1100): ")) * 1e3
#     length_second_link_km = float(input("Enter the length of the second link in km (e.g., 1300): ")) * 1e3
#     buffer_size_mb = float(input("Enter the router buffer size in MB (e.g., 64): ")) * 1e6

#     # Calculate the transmission and propagation delays
#     transmission_time_first_link = (packet_size * 8) / transmission_rate_first_link
#     transmission_time_second_link = (packet_size * 8) / transmission_rate_second_link

#     propagation_delay_first_link = length_first_link_km / propagation_speed
#     propagation_delay_second_link = length_second_link_km / propagation_speed

#     # Step 2: Calculate the processing delay at the router (in seconds)
#     processing_delay = processing_delay_per_kb * (packet_size / 1024)  # packet size in kilobytes

#     # Step 3: Total time for a packet to travel from source to destination
#     total_time_per_packet = (transmission_time_first_link + propagation_delay_first_link +
#                              processing_delay + transmission_time_second_link +
#                              propagation_delay_second_link)

#     # Step 4: Calculate how many packets can fit in the buffer
#     packets_in_buffer = buffer_size_mb / packet_size

#     # Step 5: Calculate the packet that will be lost
#     # The first packet to be lost is when the time taken exceeds the buffer capacity
#     packet_number_lost = int(packets_in_buffer) + 1

#     print(f"The first packet to be lost is packet number: {packet_number_lost}")


# # Run the function
# question = int(input("Which question do you need? 1 = ISP 2 = Lost Packet 3 = Segmentation \n"))

# if question == 1:
#     ISP_Problem()

# elif question == 2:
#     calculate_packet_loss()

# elif question == 3:
#     calculate_packet_transfer()
import math
''' Problem 1 Solution '''

# Change this the total bandwidth for you problem
bandwidth = 160
user_bandwidth = 8.9
max_users = bandwidth // user_bandwidth
print("Solution 1:")
print(f"- Maximum number of users: {max_users}\n")
''' 
  Problem 2 Solution 
  THIS WILL ONLY GET YOU 6/8 POINTS
'''
# Number of users (CHANGE THIS FOR YOUR PROBLEM)
n = 26

# Probability of a single user accessing the network
# User subscribed for {p} percent of time
p = 0.15


def binomial_coefficient(n, k):
  return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def binomial_distribution(n, k):
  return binomial_coefficient(n, k) * (p**k) * ((1 - p)**(n - k))


# Calculate the probabilities
probability_0_users = round(binomial_distribution(n, 0), 5)
probability_1_user = 1 - probability_0_users
probability_exactly_1_user = round(binomial_distribution(n, 1), 5)
probability_2_users = 1 - probability_0_users + probability_exactly_1_user
probability_exactly_2_users = round(binomial_distribution(n, 2), 5)

# Print the results
print("Solution 2:")
print(
    f"- Probability that no user is accessing the network: {probability_0_users}"
)
print(
    f"- Probability that one particular user is accessing the network: {probability_1_user}"
)
print(
    f"- Probability that exactly one user (any one) is accessing the network: {probability_exactly_1_user}"
)
print(
    f"- Probability that two particular users are accessing the network: {probability_2_users}"
)
print(
    f"- Probability that exactly two users (any two) are accessing the network: {probability_exactly_2_users}\n"
)
''' Problem 3 Solution '''
# Number of users (CHANGE THIS FOR PROBLEM 3)
n_3 = 100


def binomial_coefficient1(n_3, k):
  return math.factorial(n_3) / (math.factorial(k) * math.factorial(n_3 - k))


def calculate_probability1(N):
  probability = 0
  for k in range(0, N + 1):
    probability += binomial_coefficient1(n_3, k) * (p**k) * (
        (1 - p)**(n_3 - k))

  probability = 1 - probability
  return round(probability, 5)


# Calculate the probability for at least 18 users accessing the network
N = int(max_users) + 1
probability_at_least_18_users = calculate_probability1(N)

# Print the result
print("Solution 3:")
print(
    f"- Probability that at least {N} users are accessing the network: {probability_at_least_18_users}\n"
)
''' Problem 4 Solution '''
low = N
high = n_3
while calculate_probability1(N) > 0.0001:
  n_3 -= 1

print("Solution 4:")
print(f"- Maximum number of users for 99.99% congestion free: {n_3}")

question = int(input("Which question?\n 1 = Selective Repeat Protocol\n 2 = Synack - 3 Parts\n 3 = Synack - 4 Parts\n 4 = TCP Procedure for Estimating RTT\n 5 = Ssthresh value\n"))
if question == 1:
    pass

elif question == 2:
    pass

elif question == 3:
    pass

elif question == 4:
    pass

elif question == 5:
    pass