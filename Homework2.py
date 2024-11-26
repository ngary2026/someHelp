# ### Consider an Internet path over which data... ###
def solve_internet_path():
    # User inputs
    transmission_rate = float(input("Enter the transmission rate in megabits per second: ")) * 1e6  # convert Mbps to bits/sec
    distance_per_link = float(input("Enter the distance per link in kilometers: ")) * 1000  # convert km to meters
    propagation_speed = float(input("Enter the propagation speed in meters per second: ")) * 1e8
    num_links = int(input("Enter the number of links: "))
    packet_size_kb = float(input("Enter the packet size in kilobytes: ")) * 1024 * 8  # convert KB to bits
    page_size_kb = float(input("Enter the web page size in kilobytes: ")) * 1024 * 8  # convert KB to bits
    image_size_kb = float(input("Enter the image size in kilobytes: ")) * 1024 * 8  # convert KB to bits
    num_images = int(input("Enter the number of images: "))

    # Calculate one-way propagation delay for a single link
    one_way_propagation_delay = distance_per_link / propagation_speed  # Time for signal to travel over one link
    
    # Total propagation delay for all links (round-trip)
    propagation_delay_total = 2 * (num_links * one_way_propagation_delay)  # for RTT, we need to consider a round trip
    
    # Transmission delay for a single packet
    transmission_delay_packet = packet_size_kb / transmission_rate  # Time to transmit a single packet

    # RTT: Round Trip Time (Propagation delay + Transmission delay for one packet)
    rtt = 2 * (num_links * one_way_propagation_delay) + transmission_delay_packet

    # Time for the first packet to arrive at the router connected to server
    first_router_time = one_way_propagation_delay + transmission_delay_packet

    # Time for first packet to arrive at router two hops away
    second_router_time = 2 * one_way_propagation_delay + transmission_delay_packet

    # Time for first packet to reach the HTTP client (propagation to client + transmission of the first packet)
    client_receives_first_packet = num_links * one_way_propagation_delay + transmission_delay_packet

    # Time to download the whole web page (web page transmission time)
    page_transmission_time = page_size_kb / transmission_rate
    total_page_download_time = client_receives_first_packet + page_transmission_time

    # Non-persistent HTTP using a single TCP connection (first image arrival time)
    first_image_transmission_time = image_size_kb / transmission_rate
    first_image_arrival_time = total_page_download_time + rtt + first_image_transmission_time

    # Non-persistent HTTP (time for full download of page and all images with one TCP connection)
    all_images_transmission_time = num_images * image_size_kb / transmission_rate
    time_for_all_images_single_tcp = total_page_download_time + num_images * (rtt + first_image_transmission_time)

    # Non-persistent HTTP (multiple TCP connections simultaneously)
    time_for_all_images_multi_tcp = total_page_download_time + rtt + all_images_transmission_time

    # Persistent HTTP (one TCP connection for page and images)
    time_for_all_images_persistent_http = total_page_download_time + rtt + all_images_transmission_time

    # Display results rounded to the nearest thousandth
    print(f"{rtt:.3f},{first_router_time:.3f},{second_router_time:.3f},{client_receives_first_packet:.3f},"
          f"{total_page_download_time:.3f},{first_image_arrival_time:.3f},{time_for_all_images_single_tcp:.3f},"
          f"{time_for_all_images_multi_tcp:.3f},{time_for_all_images_persistent_http:.3f}")
    
def calculate_dns_times():
    # Define constants
    time_per_request = int(input("time in milliseconds for one-way communication:"))  # time in milliseconds for one-way communication
    round_trip_time = 2 * time_per_request  # time for a full round trip
    
    # Cache expiration times (in milliseconds)
    cache_expiration_1 = int(input("first request: "))  # First cache expiration time in ms
    cache_expiration_2 = int(input("second request: "))  # Second cache expiration time in ms

    # Step 1: Local DNS receives query from local host
    t_local_dns_receives_query = time_per_request
    print(f"Local DNS receives query from local host at {t_local_dns_receives_query} ms")
    
    # Step 2: Local DNS sends query to root server and receives response
    t_local_dns_receives_root_response = t_local_dns_receives_query + round_trip_time
    print(f"Local DNS receives response from root server at {t_local_dns_receives_root_response} ms")
    
    # Step 3: Local DNS sends query to TLD server and receives response
    t_local_dns_receives_tld_response = t_local_dns_receives_root_response + round_trip_time
    print(f"Local DNS receives response from TLD server at {t_local_dns_receives_tld_response} ms")
    
    # Step 4: Local DNS sends query to authoritative server
    t_local_dns_sends_authoritative_request = t_local_dns_receives_tld_response
    # print(f"Local DNS sends request to authoritative server at {t_local_dns_sends_authoritative_request} ms")
    
    # Step 5: Local DNS receives response from authoritative server
    t_local_dns_receives_authoritative_response = t_local_dns_sends_authoritative_request + round_trip_time
    print(f"Local DNS receives response from authoritative server at {t_local_dns_receives_authoritative_response} ms")
    
    # Step 6: Local DNS sends final response to local host
    t_local_host_receives_response = t_local_dns_receives_authoritative_response + time_per_request
    print(f"Local host receives response from local DNS server at {t_local_host_receives_response} ms")

    
    print(f"First cache expiration happens at {cache_expiration_1 + t_local_host_receives_response} ms")
    print(f"Second cache expiration happens at {cache_expiration_2 + t_local_host_receives_response/4} ms")

def calculate_response_times():
    # Given data
    access_link_bandwidth = 6 * 10**6  # in bits per second (15 Mbps)
    object_size = 150 * 10**3  # in bits (110 Kbits)
    request_rate = 30  # requests per second
    internet_delay = 1.3 * 1000  # in milliseconds (1.1 seconds = 1100 ms)

    # Proxy-related data
    cache_hit_rate = 0.50  # 55% of objects are cached
    cache_stale_rate = 0.15  # 15% of cached objects are out-of-date

    # Calculate Δ (time to send one object over the access link)
    delta = (object_size / access_link_bandwidth) * 1000  # Convert to milliseconds
    beta = request_rate  # Arrival rate of objects (30 requests per second)

    # Calculate the average access delay without a proxy
    access_delay = delta / (1 - (delta * beta / 1000))

    # Calculate the total average response time without a proxy
    total_response_time_no_proxy = access_delay + internet_delay

    # Calculate the average access delay with a proxy
    # Cache hit rate * (1 - cache stale rate) are objects served locally
    fraction_from_cache = cache_hit_rate * (1 - cache_stale_rate)
    fraction_from_internet = 1 - fraction_from_cache

    # Access delay with proxy (locally cached objects have no access delay)
    access_delay_with_proxy = (fraction_from_internet * access_delay)

    # Calculate the total average response time with a proxy
    total_response_time_with_proxy = (fraction_from_internet * total_response_time_no_proxy) + \
                                     (fraction_from_cache * access_delay_with_proxy)

    # Return the results rounded to nearest tenth
    return round(access_delay, 1), round(total_response_time_no_proxy, 1), \
           round(access_delay_with_proxy, 1), round(total_response_time_with_proxy, 1)


# Run the function
question = int(input("Which question do you need? 1 = internet path, 2 = dns, 3 = response time\n"))

if question == 1:
    solve_internet_path()

elif question == 2:
    calculate_dns_times()

elif question == 3:
    calculate_response_times()

# class InternetPathSolution:
#     def __init__(self, transmission_rate: int,
#                  number_of_links: int,
#                  number_of_routers: int,
#                  length_of_link: int,
#                  signal_propagation_speed: int,
#                  webpage_size: int,
#                  number_of_images: int,
#                  image_size: int,
#                  max_pkt_size: int):
#         self.transmission_rate = transmission_rate
#         self.number_of_links = number_of_links
#         self.number_of_routers = number_of_routers
#         self.length_of_link = length_of_link
#         self.signal_propagation_speed = signal_propagation_speed
#         self.webpage_size = webpage_size
#         self.number_of_images = number_of_images
#         self.image_size = image_size
#         self.max_pkt_size = max_pkt_size

#         self.round_trip_time = self._calculate_round_trip_time()

#     def _calculate_round_trip_time(self) -> float:
#         total_length_of_links = self.number_of_links * self.length_of_link
#         propagation_delay = total_length_of_links / self.signal_propagation_speed
#         return propagation_delay * 2
    
#     def _calculate_first_packet_arrival_time(self) -> float:
#         time_for_tcp_connection = self._calculate_round_trip_time()
#         time_for_request = time_for_tcp_connection / 2
#         first_transmission_delay = self.max_pkt_size / self.transmission_rate
#         first_propagation_delay_till_router = self.length_of_link / self.signal_propagation_speed
#         return time_for_tcp_connection + time_for_request + \
#             first_transmission_delay + first_propagation_delay_till_router
    

#     def _calculate_first_packet_arrival_time_two_hops(self) -> float:
#         time_till_one_hop_away = self._calculate_first_packet_arrival_time()
#         second_transmission_delay = self.max_pkt_size / self.transmission_rate
#         second_propagation_delay_till_router = self.length_of_link / self.signal_propagation_speed
#         extra_time = second_propagation_delay_till_router + second_transmission_delay
#         total_time_two_hops = extra_time + time_till_one_hop_away
#         return total_time_two_hops
    
#     def _calculate_time_http_client_receives_first_packet(self) -> float:
#         time_for_tcp_connection = self.round_trip_time
#         time_for_request = time_for_tcp_connection / 2
#         propagation_delay = self.number_of_links * \
#             (self.length_of_link / self.signal_propagation_speed)
#         transmission_delay_for_first_packet = (
#             self.number_of_routers + 1) * (self.max_pkt_size / self.transmission_rate)
#         return time_for_tcp_connection + time_for_request + \
#             propagation_delay + transmission_delay_for_first_packet
    
#     def _calculate_time_to_receive_the_whole_web_page(self) -> float:
#         time_for_tcp_connection = self.round_trip_time
#         time_for_request = time_for_tcp_connection / 2
#         propagation_delay = self.number_of_links * (self.length_of_link /
#                                                self.signal_propagation_speed)

#         num_packets_of_max_size = self.webpage_size // self.max_pkt_size
#         transmission_delay_for_packets_of_max_size = (
#             num_packets_of_max_size + self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
#         num_packets_of_rem_bytes = self.webpage_size % self.max_pkt_size
#         transmission_delay_for_rem_bytes = num_packets_of_rem_bytes / self.transmission_rate
#         return time_for_tcp_connection + time_for_request + propagation_delay + \
#             transmission_delay_for_packets_of_max_size + transmission_delay_for_rem_bytes
    
#     def _calculate_time_elapses_to_receive_first_image(self) -> float:
#         time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
#         time_for_tcp_connection = self.round_trip_time
#         time_for_request = time_for_tcp_connection / 2
#         propagation_delay = self.number_of_links * (self.length_of_link /
#                                                self.signal_propagation_speed)

#         num_packets_for_images_of_max_size = self.image_size // self.max_pkt_size
#         transmission_delay = (num_packets_for_images_of_max_size +
#                               self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
#         num_packets_of_rem_bytes = self.image_size % self.max_pkt_size
#         transmission_delay_for_rem_bytes = num_packets_of_rem_bytes / self.transmission_rate
#         time_to_receive_first_image = time_for_tcp_connection + time_for_request + \
#             propagation_delay + transmission_delay + transmission_delay_for_rem_bytes
#         return time_to_receive_first_image + time_to_get_webpage
    
#     def _calculate_time_for_webpage_to_be_displayed(self) -> float:
#         time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
#         time_for_tcp_connection = self.round_trip_time
#         time_for_request = time_for_tcp_connection / 2
#         propagation_delay = self.number_of_links * \
#             (self.length_of_link / self.signal_propagation_speed)

#         number_of_pkts = self.image_size // self.max_pkt_size
#         transmission_delay = (number_of_pkts + self.number_of_routers) * (
#             self.max_pkt_size / self.transmission_rate)
#         num_packets_of_rem_bytes = self.image_size % self.max_pkt_size
#         transmission_delay_for_rem_bytes = num_packets_of_rem_bytes / self.transmission_rate
#         time_to_get_all_images = (time_for_tcp_connection + time_for_request + propagation_delay +
#                                   transmission_delay +
#                                   transmission_delay_for_rem_bytes) * self.number_of_images
#         return time_to_get_webpage + time_to_get_all_images
    
#     def _calculate_time_elapsed_to_display_webpage_all_tcp_connections(self) -> float:
#         time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
#         time_for_tcp_connection = self.round_trip_time
#         time_for_request = time_for_tcp_connection / 2
#         propagation_delay = self.number_of_links * \
#             (self.length_of_link / self.signal_propagation_speed)

#         total_packets_formed_from_all_images_of_max_size = (
#             self.image_size * self.number_of_images) // self.max_pkt_size
#         total_transmission_delay = (total_packets_formed_from_all_images_of_max_size +
#                                     self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
#         packets_formed_of_less_than_max_size = (
#             self.image_size * self.number_of_images) % self.max_pkt_size
#         transmission_delay_for_packets_formed_of_less_than_max_size = packets_formed_of_less_than_max_size / self.transmission_rate
#         time_to_receive_all_images_simultaneously = time_for_tcp_connection + time_for_request + \
#             propagation_delay + total_transmission_delay + \
#             transmission_delay_for_packets_formed_of_less_than_max_size
#         return time_to_get_webpage + \
#             time_to_receive_all_images_simultaneously
    
#     def _calculate_time_to_display_entire_webpage(self) -> float:
#         time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
#         time_for_tcp_connection = self.round_trip_time
#         time_for_request = time_for_tcp_connection / 2
#         propagation_delay = self.number_of_links * \
#             (self.length_of_link / self.signal_propagation_speed)
#         total_packets_formed_from_all_images_of_max_size = (
#             self.image_size * self.number_of_images) // self.max_pkt_size
#         total_transmission_delay = (total_packets_formed_from_all_images_of_max_size +
#                                     self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
#         packets_formed_of_less_than_max_size = (
#             self.image_size * self.number_of_images) % self.max_pkt_size
#         transmission_delay_for_packets_formed_of_less_than_max_size = packets_formed_of_less_than_max_size / self.transmission_rate
#         time_to_receive_all_images_simultaneously = time_for_request + propagation_delay + \
#             total_transmission_delay + transmission_delay_for_packets_formed_of_less_than_max_size
#         return time_to_get_webpage + \
#             time_to_receive_all_images_simultaneously
      


#     def solve(self) -> str:
#         return f"{round(self._calculate_round_trip_time(), 3)},{round(self._calculate_first_packet_arrival_time(), 3)},{round(self._calculate_first_packet_arrival_time_two_hops(), 3)},{round(self._calculate_time_http_client_receives_first_packet(), 3)},{round(self._calculate_time_to_receive_the_whole_web_page(), 3)},{round(self._calculate_time_elapses_to_receive_first_image(), 3)},{round(self._calculate_time_for_webpage_to_be_displayed(), 3)},{round(self._calculate_time_elapsed_to_display_webpage_all_tcp_connections(), 3)},{round(self._calculate_time_to_display_entire_webpage(), 3)}"



# class InstitutionalNetworkResponseTimeSolution:
#     def __init__(self, network_bandwidth: float, access_link_bandwidth: float, web_object_size: float, average_request_rate: float, response_time: float, cache_percentage: float, invalid_cache_percentage: float):
#         self.network_bandwidth = network_bandwidth
#         self.access_link_bandwidth = access_link_bandwidth
#         self.web_object_size = web_object_size
#         self.average_request_rate = average_request_rate
#         self.response_time = response_time
#         self.cache_percentage = cache_percentage
#         self.invalid_cache_percentage = invalid_cache_percentage

#         # Delta: time to send an object over the access link in seconds
#         self.delta = self.web_object_size / self.access_link_bandwidth

#         self.access_delay = self.delta / \
#             (1 - (self.average_request_rate * self.delta))  # in seconds

#         self.transmission_delay = self.web_object_size / \
#             self.network_bandwidth  # in seconds

#         self.total_response_time = self.access_delay + \
#             self.transmission_delay + self.response_time  # in seconds

#         self.valid_cache = self.cache_percentage * \
#             (1 - self.invalid_cache_percentage / 100) / 100  # convert to decimal

#         self.arrival_rate = self.average_request_rate * \
#             (1 - self.valid_cache)  # objects per second

#         self.access_delay_with_proxy = self.delta / \
#             (1 - (self.arrival_rate * self.delta))  # in seconds

#         self.response_time_one = self.web_object_size / \
#             self.network_bandwidth  # time for a cached object in seconds
#         self.response_time_two = self.access_delay_with_proxy + self.response_time + \
#             self.response_time_one  # time for a non-cached object in seconds

#         self.average_response_time_with_proxy = (self.valid_cache * self.response_time_one) + (
#             (1 - self.valid_cache) * self.response_time_two)  # in seconds

#         self.access_delay_ms = self.access_delay * 1000  # milliseconds
#         self.total_response_time_ms = self.total_response_time * 1000  # milliseconds
#         self.access_delay_with_proxy_ms = self.access_delay_with_proxy * 1000  # milliseconds
#         self.average_response_time_with_proxy_ms = self.average_response_time_with_proxy * \
#             1000  # milliseconds

#     def solve(self) -> str:
#         return f"{self.access_delay_ms:.1f},{self.total_response_time_ms:.1f},{self.access_delay_with_proxy_ms:.1f},{self.average_response_time_with_proxy_ms:.1f}"



# if __name__ == "__main__":
#     # calculate_dns_times()
#     # print("\n")

#     network_bandwidth = float(input("network bandwidth: ")) * 10 ** 9  # Gbps to bits
#     access_link_bandwidth = int(input("access link bandwidth: ")) * 10 ** 6  # Mbps to bits
#     web_object_size = int(input("web object size link bandwidth: ")) * 10 ** 3  # Kbits to bits
#     average_request_rate = int(input("avg request rate: "))  # requests per second
#     response_time = float(input("response time: "))  # seconds
#     cache_percentage = int(input("percent in cache: (whole number) "))  # percentage of objects in cache
#     invalid_cache_percentage = int(input("percent in cache invalid: (whole number) "))  # percentage of cached objects that are invalid

#     response_time = InstitutionalNetworkResponseTimeSolution(network_bandwidth,
#                                                              access_link_bandwidth,
#                                                              web_object_size,
#                                                              average_request_rate,
#                                                              response_time,
#                                                              cache_percentage,
#                                                              invalid_cache_percentage)
#     print(response_time.solve())

#     transmission_rate = 15 * 10**6  # megabits per second
#     number_of_links = 3
#     number_of_routers = 2
#     length_of_link = 1000 * 10**3  #  kilometers in meters
#     signal_propagation_speed = 1.5 * 10**8  #  meters per second
#     webpage_size = 21 * 8 * 10**3  #  kilobytes in bits
#     number_of_images = 23
#     image_size = 150 * 8 * 10**3  #  kilobytes in bits
#     max_pkt_size = 7 * 8 * 10**3  # In bits

    
#     internet_path = InternetPathSolution(transmission_rate,
#                                          number_of_links,
#                                          number_of_routers,
#                                          length_of_link,
#                                          signal_propagation_speed,
#                                          webpage_size,
#                                          number_of_images,
#                                          image_size, max_pkt_size)
#     print(internet_path.solve())