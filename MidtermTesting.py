import math

####### GO-BACK-N #######
class GoBackN:
  def __init__(self):

    self.rtt = int(input("rtt: "))
    
    self.beginning = int(input("first sequence number: "))
    self.sending_window = int(input("window sized: "))
    self.timeout = int(input("timeout value: "))
    self.packets_num = int(input("packets amount: "))
    self.sender_lost = input("sender lost: ")
    self.sender_lost = self.sender_lost.split(",")
    self.sender_lost = [int(i) for i in self.sender_lost]
    self.reciever_lost = input("reciever lost: ")
    self.reciever_lost = self.reciever_lost.split(",")
    self.reciever_lost = [int(i) for i in self.reciever_lost]

    self.curr = 0
    self.send_ind = 1
    self.r_ind = 1
    self.r_exp = self.beginning
    self.count = 0
    self.packets_to_send = [i for i in range(self.beginning, self.beginning+self.packets_num)]

    self.sent_by_sender = []
    self.sent_by_reciever = []
    self.myL = []
    self.i = 0
    # self.j = self.i + self.sending_window
    self.j = 0

    self.send()
    return

  def send(self, isRepeat = True):
    if self.count >= self.packets_num:
      self.stop()
      return

    
    tempJ = self.j
    self.j = self.i + self.sending_window
    print(tempJ, self.j)
    if isRepeat:
      self.packets_window = [i for i in self.packets_to_send[self.i:self.j]]
    else:
      print("hi", self.packets_window)
      self.packets_window = [i for i in self.packets_to_send[tempJ:self.j]]
    to_send = []
    for i in self.packets_window:
      to_send.append((i, self.send_ind))
      self.send_ind+=1
      self.count+=1


    # for i in to_send:
    #   i_val = i[0]
    #   stuff = (self.curr + self.timeout, "timeout", i_val)

    self.myL.append((self.curr + self.timeout, "timeout", [i[0] for i in to_send]))
    self.sent_by_sender.extend([i[0] for i in to_send])
    print(self.myL)
    recieved = []
    for i in to_send:
      i_val = i[0]
      i_ind = i[1]
      if i_ind not in self.sender_lost:
        recieved.append(i_val)
      # stuff = (self.curr + self.rtt, "packets", i, self.send_ind)
    send_back = []
    for i in recieved:
      if i == self.r_exp:
        send_back.append(i)
        self.r_exp += 1
      else:
        send_back.append(self.r_exp-1)
      

    print(send_back)
    self.sent_by_reciever.extend(send_back)
    # sending back packets
    coming_back = []
    for i in send_back:
      if self.r_ind not in self.reciever_lost:
        coming_back.append(i)  
      self.r_ind+=1

    stuff = (self.curr+self.rtt+1, "packets", coming_back)
    self.myL.append(stuff)    

    self.myL = sorted(self.myL, key=self.getKey)
    print(self.myL)

    self.next()
    return


  def next(self):
    first = self.myL.pop(0)
    [self.curr, type1, packets] = first
    
    if type1 == "timeout":
      self.send()
    elif type1 == "packets":
      self.curr-=1
      changed = False
      for i in packets:
        exp = self.packets_to_send[self.i]
        print(i, exp)
        if i >= exp:
          # discard Timeout
          self.discardTimeout(i)
          self.i+=i-exp+1
          changed = True
          print("hia")
          # self.j+=i-exp+1
      # after something is acknowledged and you increment i and j, you have to add the i and j you incremented
      if changed:
        self.send(False)
      else:
        self.next()
      #remember to discard timeouts for recieved nums
    else:
      print("something went wrong here")
    return

  def discardTimeout(self, val):
    for i in self.myL:
      if i[1] == "timeout":
        if val in i[2]:
          i[2].remove(val)
          break
    return
  def getKey(self, item):
    return item[0]

  def stop(self):
    length = len(self.sent_by_sender)
    ans1 = self.sent_by_sender[:self.packets_num]
    diff = length - self.packets_num
    if diff > 0:
      ans2 = self.sent_by_reciever[:-diff]
    else:
      ans2 = self.sent_by_reciever

    ans1 = [str(i) for i in ans1]
    ans2 = [str(i) for i in ans2]
    ans1 = ",".join(ans1)
    ans2 = ",".join(ans2)
    print(ans1+";"+ans2)
    # print(self.sent_by_sender[:self.packets_num], self.sent_by_reciever[:-diff])

    # exit()

class SelectiveRepeat:
  def __init__(self):

    self.rtt = int(input("rtt: "))
    
    self.beginning = int(input("first sequence number: "))
    self.sending_window = int(input("window sized: "))
    self.timeout = int(input("timeout value: "))
    self.packets_num = int(input("packets amount: "))
    self.sender_lost = input("sender lost: ")
    self.sender_lost = self.sender_lost.split(",")
    self.sender_lost = [int(i) for i in self.sender_lost]
    self.reciever_lost = input("reciever lost: ")
    self.reciever_lost = self.reciever_lost.split(",")
    self.reciever_lost = [int(i) for i in self.reciever_lost]

    self.curr = 0
    self.send_ind = 1
    self.r_ind = 1
    self.r_exp = self.beginning
    self.count = 0
    self.packets_to_send = [i for i in range(self.beginning, self.beginning+self.packets_num)]


    self.buffer = []
    self.ackBuffer = []
    self.sent_by_sender = []
    self.sent_by_reciever = []
    self.myL = []
    self.i = 0
    # self.j = self.i + self.sending_window
    self.j = 0

    self.send()
    return

  def send(self, isRepeat = True, packets = []):
    if self.count >= self.packets_num:
      self.stop()
      return

    
    tempJ = self.j
    self.j = self.i + self.sending_window
    # print(tempJ, self.j)
    if packets:
      self.packets_window = [i for i in packets]
    else:
      if isRepeat:
        # send entire window
        self.packets_window = [i for i in self.packets_to_send[self.i:self.j]]
      else:
        # print("hi", self.packets_window)
        # send only partial
        self.packets_window = [i for i in self.packets_to_send[tempJ:self.j]]
    to_send = []
    for i in self.packets_window:
      to_send.append((i, self.send_ind))
      self.send_ind+=1
      self.count+=1

    self.myL.append((self.curr + self.timeout, "timeout", [i[0] for i in to_send]))
    self.sent_by_sender.extend([i[0] for i in to_send])

    # print(self.myL)

    recieved = []
    for i in to_send:
      i_val = i[0]
      i_ind = i[1]
      if i_ind not in self.sender_lost:
        recieved.append(i_val)
      # stuff = (self.curr + self.rtt, "packets", i, self.send_ind)

    send_back = []
    for i in recieved:
      self.buffer.append(i)
      self.buffer = sorted(self.buffer)

      while self.buffer and self.buffer[0] == self.r_exp:
        self.r_exp+=1
        self.buffer.pop(0)
      send_back.append(i)
      
    # print(send_back)
    self.sent_by_reciever.extend(send_back)
    # sending back packets
    coming_back = []
    for i in send_back:
      if self.r_ind not in self.reciever_lost:
        coming_back.append(i)
      self.r_ind+=1

    stuff = (self.curr+self.rtt+1, "packets", coming_back)
    self.myL.append(stuff)

    self.myL = sorted(self.myL, key=self.getKey)
    # print(self.myL)

    self.next()
    return


  def next(self):
    first = self.myL.pop(0)
    [self.curr, type1, packets] = first
    if type1 == "timeout":
      if packets:
        self.send(packets = packets.copy())
      else:
        self.next()
    elif type1 == "packets":
      self.curr-=1
      changed = False
      for i in packets:
        exp = self.packets_to_send[self.i]
        self.discardTimeout(i)
        self.ackBuffer.append(i)
        self.ackBuffer = sorted(self.ackBuffer)
        while self.ackBuffer and self.ackBuffer[0] == exp:
          self.ackBuffer.pop(0)
          self.i+=1
          changed = True
          exp+=1
      # after something is acknowledged and you increment i and j, you have to add the i and j you incremented
      if changed:
        self.send(False)
      else:
        self.next()
      #remember to discard timeouts for recieved nums
    else:
      print("something went wrong here")
    return

  def discardTimeout(self, val):
    for i in self.myL:
      if i[1] == "timeout":
        if val in i[2]:
          i[2].remove(val)
          break
    return

  def getKey(self, item):
    return item[0]

  def stop(self):
    length = len(self.sent_by_sender)
    diff = length - self.packets_num
    ans1 = self.sent_by_sender[:self.packets_num]
    if diff > 0:
      ans2 = self.sent_by_reciever[:-diff]
    else:
      ans2 = self.sent_by_reciever
    ans1 = [str(i) for i in ans1]
    ans2 = [str(i) for i in ans2]
    ans1 = ",".join(ans1)
    ans2 = ",".join(ans2)
    print(ans1+";"+ans2)

####### END-TO-END #######
class end2end:
    def __init__(self):
        packet_size = int(input("Packet Size: "))
        propagation_speed = float(input("Propagation Speed: ")) * 10**8
        transmission_rate_1 = int(input("transmission_rate_1: "))
        transmission_rate_2 = int(input("transmission_rate_2: "))
        router_processing = int(input("router processing: "))
        link_1 = int(input("link 1: "))
        link_2 = int(input("link 2: ")) 

        transmission_delay_1 = (packet_size * 8) / (transmission_rate_1 * 10**6) * 10**6
        print(f"Transmission delay 1: {transmission_delay_1:.1f}")

        propagation_delay_1 = (link_1 * 10**3) / (propagation_speed) * 10**6
        print(f"Propagation delay 1: {propagation_delay_1:.1f}")

        router_processing_delay = (packet_size / 1000) * router_processing
        print(f"Router processing delay: {router_processing_delay:.1f}\n")

        first_link_delay = transmission_delay_1 + propagation_delay_1 + router_processing_delay
        print(f"1) Total delay from source to router: {first_link_delay:.1f}\n")

        transmission_delay_2 = (packet_size * 8) / (transmission_rate_2 * 10**6) * 10**6
        print(f"Transmission delay 2: {transmission_delay_2:.1f}")

        propagation_delay_2 = (link_2 * 10**3) / (propagation_speed) * 10**6
        print(f"Propagation delay 2: {propagation_delay_2:.1f}\n")

        end_to_end_delay_1 = transmission_delay_1 + propagation_delay_1 + router_processing_delay + transmission_delay_2 + propagation_delay_2
        print(f"2) End-to-End delay of first packet: {end_to_end_delay_1:.1f}")

        x = transmission_delay_2 - transmission_delay_1
        # formula: total_delay + ((n - 1) * x)
        end_to_end_delay_2 = end_to_end_delay_1 + ((2 - 1) * x)
        print(f"3) End-to-End delay of second packet: {end_to_end_delay_2:.1f}")

        end_to_end_delay_3 = end_to_end_delay_1 + ((3 - 1) * x)
        print(f"4) End-to-End delay of third packet: {end_to_end_delay_3:.1f}")

        end_to_end_delay_100 = end_to_end_delay_1 + ((100 - 1) * x)
        print(f"5) End-to-End delay of 100th packet: {end_to_end_delay_100:.1f}")

####### PIPELINED PROTOCOL #######
class pipelinedProtocol:
  def __init__(self):
    Bandwidth = float(input("Bandwidth: ")) * 10 ** 9
    Propogation_Speed = float(input("Propagation Speed: ")) * 10 ** 8
    Packet_Size = int(input("Packet: ")) * 8
    Window_Size = int(input("Window size: "))
    Channel_Utilization = int(input("channel utilization (whole number): ")) * 0.01 #Percentage

    Time_to_send_Packet = Packet_Size / Bandwidth

    Min_RTT = ((Window_Size * Time_to_send_Packet) / Channel_Utilization) - Time_to_send_Packet

    Min_Length = Min_RTT * Propogation_Speed / 2
    Min_Length /= 1000 #To Km
    print(f"{Min_Length:.1f}")

####### INSTITUTIONAL NETWORK #######
class InstitutionalNetworkResponseTimeSolution:
    
    def __init__(self, network_bandwidth: float, access_link_bandwidth: float, web_object_size: float, average_request_rate: float, response_time: float, cache_percentage: float, invalid_cache_percentage: float):
        self.network_bandwidth = network_bandwidth
        self.access_link_bandwidth = access_link_bandwidth
        self.web_object_size = web_object_size
        self.average_request_rate = average_request_rate
        self.response_time = response_time
        self.cache_percentage = cache_percentage
        self.invalid_cache_percentage = invalid_cache_percentage

        # Delta: time to send an object over the access link in seconds
        self.delta = self.web_object_size / self.access_link_bandwidth

        self.access_delay = self.delta / \
            (1 - (self.average_request_rate * self.delta))  # in seconds

        self.transmission_delay = self.web_object_size / \
            self.network_bandwidth  # in seconds

        self.total_response_time = self.access_delay + \
            self.transmission_delay + self.response_time  # in seconds

        self.valid_cache = self.cache_percentage * \
            (1 - self.invalid_cache_percentage / 100) / 100  # convert to decimal

        self.arrival_rate = self.average_request_rate * \
            (1 - self.valid_cache)  # objects per second

        self.access_delay_with_proxy = self.delta / \
            (1 - (self.arrival_rate * self.delta))  # in seconds

        self.response_time_one = self.web_object_size / \
            self.network_bandwidth  # time for a cached object in seconds
        self.response_time_two = self.access_delay_with_proxy + self.response_time + \
            self.response_time_one  # time for a non-cached object in seconds

        self.average_response_time_with_proxy = (self.valid_cache * self.response_time_one) + (
            (1 - self.valid_cache) * self.response_time_two)  # in seconds

        self.access_delay_ms = self.access_delay * 1000  # milliseconds
        self.total_response_time_ms = self.total_response_time * 1000  # milliseconds
        self.access_delay_with_proxy_ms = self.access_delay_with_proxy * 1000  # milliseconds
        self.average_response_time_with_proxy_ms = self.average_response_time_with_proxy * \
            1000  # milliseconds

    def solve(self) -> str:
        return f"{self.access_delay_ms:.1f},{self.total_response_time_ms:.1f},{self.access_delay_with_proxy_ms:.1f},{self.average_response_time_with_proxy_ms:.1f}"

####### INTERNET PATH #######
class InternetPathSolution:
    def __init__(self, transmission_rate: int,
                 number_of_links: int,
                 number_of_routers: int,
                 length_of_link: int,
                 signal_propagation_speed: int,
                 webpage_size: int,
                 number_of_images: int,
                 image_size: int,
                 max_pkt_size: int):
        self.transmission_rate = transmission_rate
        self.number_of_links = number_of_links
        self.number_of_routers = number_of_routers
        self.length_of_link = length_of_link
        self.signal_propagation_speed = signal_propagation_speed
        self.webpage_size = webpage_size
        self.number_of_images = number_of_images
        self.image_size = image_size
        self.max_pkt_size = max_pkt_size

        self.round_trip_time = self._calculate_round_trip_time()

    def _calculate_round_trip_time(self) -> float:
        total_length_of_links = self.number_of_links * self.length_of_link
        propagation_delay = total_length_of_links / self.signal_propagation_speed
        return propagation_delay * 2
    
    def _calculate_first_packet_arrival_time(self) -> float:
        time_for_tcp_connection = self._calculate_round_trip_time()
        time_for_request = time_for_tcp_connection / 2
        first_transmission_delay = self.max_pkt_size / self.transmission_rate
        first_propagation_delay_till_router = self.length_of_link / self.signal_propagation_speed
        return time_for_tcp_connection + time_for_request + \
            first_transmission_delay + first_propagation_delay_till_router
    

    def _calculate_first_packet_arrival_time_two_hops(self) -> float:
        time_till_one_hop_away = self._calculate_first_packet_arrival_time()
        second_transmission_delay = self.max_pkt_size / self.transmission_rate
        second_propagation_delay_till_router = self.length_of_link / self.signal_propagation_speed
        extra_time = second_propagation_delay_till_router + second_transmission_delay
        total_time_two_hops = extra_time + time_till_one_hop_away
        return total_time_two_hops
    
    def _calculate_time_http_client_receives_first_packet(self) -> float:
        time_for_tcp_connection = self.round_trip_time
        time_for_request = time_for_tcp_connection / 2
        propagation_delay = self.number_of_links * \
            (self.length_of_link / self.signal_propagation_speed)
        transmission_delay_for_first_packet = (
            self.number_of_routers + 1) * (self.max_pkt_size / self.transmission_rate)
        return time_for_tcp_connection + time_for_request + \
            propagation_delay + transmission_delay_for_first_packet
    
    def _calculate_time_to_receive_the_whole_web_page(self) -> float:
        time_for_tcp_connection = self.round_trip_time
        time_for_request = time_for_tcp_connection / 2
        propagation_delay = self.number_of_links * (self.length_of_link /
                                               self.signal_propagation_speed)

        num_packets_of_max_size = self.webpage_size // self.max_pkt_size
        transmission_delay_for_packets_of_max_size = (
            num_packets_of_max_size + self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
        num_packets_of_rem_bytes = self.webpage_size % self.max_pkt_size
        transmission_delay_for_rem_bytes = num_packets_of_rem_bytes / self.transmission_rate
        return time_for_tcp_connection + time_for_request + propagation_delay + \
            transmission_delay_for_packets_of_max_size + transmission_delay_for_rem_bytes
    
    def _calculate_time_elapses_to_receive_first_image(self) -> float:
        time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
        time_for_tcp_connection = self.round_trip_time
        time_for_request = time_for_tcp_connection / 2
        propagation_delay = self.number_of_links * (self.length_of_link /
                                               self.signal_propagation_speed)

        num_packets_for_images_of_max_size = self.image_size // self.max_pkt_size
        transmission_delay = (num_packets_for_images_of_max_size +
                              self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
        num_packets_of_rem_bytes = self.image_size % self.max_pkt_size
        transmission_delay_for_rem_bytes = num_packets_of_rem_bytes / self.transmission_rate
        time_to_receive_first_image = time_for_tcp_connection + time_for_request + \
            propagation_delay + transmission_delay + transmission_delay_for_rem_bytes
        return time_to_receive_first_image + time_to_get_webpage
    
    def _calculate_time_for_webpage_to_be_displayed(self) -> float:
        time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
        time_for_tcp_connection = self.round_trip_time
        time_for_request = time_for_tcp_connection / 2
        propagation_delay = self.number_of_links * \
            (self.length_of_link / self.signal_propagation_speed)

        number_of_pkts = self.image_size // self.max_pkt_size
        transmission_delay = (number_of_pkts + self.number_of_routers) * (
            self.max_pkt_size / self.transmission_rate)
        num_packets_of_rem_bytes = self.image_size % self.max_pkt_size
        transmission_delay_for_rem_bytes = num_packets_of_rem_bytes / self.transmission_rate
        time_to_get_all_images = (time_for_tcp_connection + time_for_request + propagation_delay +
                                  transmission_delay +
                                  transmission_delay_for_rem_bytes) * self.number_of_images
        return time_to_get_webpage + time_to_get_all_images
    
    def _calculate_time_elapsed_to_display_webpage_all_tcp_connections(self) -> float:
        time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
        time_for_tcp_connection = self.round_trip_time
        time_for_request = time_for_tcp_connection / 2
        propagation_delay = self.number_of_links * \
            (self.length_of_link / self.signal_propagation_speed)

        total_packets_formed_from_all_images_of_max_size = (
            self.image_size * self.number_of_images) // self.max_pkt_size
        total_transmission_delay = (total_packets_formed_from_all_images_of_max_size +
                                    self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
        packets_formed_of_less_than_max_size = (
            self.image_size * self.number_of_images) % self.max_pkt_size
        transmission_delay_for_packets_formed_of_less_than_max_size = packets_formed_of_less_than_max_size / self.transmission_rate
        time_to_receive_all_images_simultaneously = time_for_tcp_connection + time_for_request + \
            propagation_delay + total_transmission_delay + \
            transmission_delay_for_packets_formed_of_less_than_max_size
        return time_to_get_webpage + \
            time_to_receive_all_images_simultaneously
    
    def _calculate_time_to_display_entire_webpage(self) -> float:
        time_to_get_webpage = self._calculate_time_to_receive_the_whole_web_page()
        time_for_tcp_connection = self.round_trip_time
        time_for_request = time_for_tcp_connection / 2
        propagation_delay = self.number_of_links * \
            (self.length_of_link / self.signal_propagation_speed)
        total_packets_formed_from_all_images_of_max_size = (
            self.image_size * self.number_of_images) // self.max_pkt_size
        total_transmission_delay = (total_packets_formed_from_all_images_of_max_size +
                                    self.number_of_routers) * (self.max_pkt_size / self.transmission_rate)
        packets_formed_of_less_than_max_size = (
            self.image_size * self.number_of_images) % self.max_pkt_size
        transmission_delay_for_packets_formed_of_less_than_max_size = packets_formed_of_less_than_max_size / self.transmission_rate
        time_to_receive_all_images_simultaneously = time_for_request + propagation_delay + \
            total_transmission_delay + transmission_delay_for_packets_formed_of_less_than_max_size
        return time_to_get_webpage + \
            time_to_receive_all_images_simultaneously
      


    def solve(self) -> str:
        return f"{round(self._calculate_round_trip_time(), 3)},{round(self._calculate_first_packet_arrival_time(), 3)},{round(self._calculate_first_packet_arrival_time_two_hops(), 3)},{round(self._calculate_time_http_client_receives_first_packet(), 3)},{round(self._calculate_time_to_receive_the_whole_web_page(), 3)},{round(self._calculate_time_elapses_to_receive_first_image(), 3)},{round(self._calculate_time_for_webpage_to_be_displayed(), 3)},{round(self._calculate_time_elapsed_to_display_webpage_all_tcp_connections(), 3)},{round(self._calculate_time_to_display_entire_webpage(), 3)}"


question = int(input("Which question do you need? 1 = End-to-End, 2 = Pipelines protocol, 3 = Go-back-N, 4 = ISP, 5 = Institutional Network (hw2), 6 = Internet Path (RTT) (hw2)\n"))

if question == 1:
    end2end()

elif question == 2:
    pipelinedProtocol()

elif question == 3:
    GoBackN()

elif question == 4:
    ####### ISP #######
    ''' Problem 1 Solution '''

    # Change this the total bandwidth for you problem
    bandwidth = int(input("bandwidth: "))
    user_bandwidth = float(input("user bandwidth: "))
    max_users = bandwidth // user_bandwidth
    print("Solution 1:")
    print(f"- Maximum number of users: {max_users}\n")
    ''' 
    Problem 2 Solution 
    THIS WILL ONLY GET YOU 6/8 POINTS
    '''
    # Number of users (CHANGE THIS FOR YOUR PROBLEM)
    n = int(input("num of users: "))

    # Probability of a single user accessing the network
    # User subscribed for {p} percent of time
    p = float(input("user access x percent of time (ex .15): "))


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
    print(f"- Probability that no user is accessing the network: {probability_0_users}")
    print(f"- Probability that one particular user is accessing the network: {probability_1_user} <--- wrong")
    print(f"- Probability that exactly one user (any one) is accessing the network: {probability_exactly_1_user}")
    print(f"- Probability that two particular users are accessing the network: {probability_2_users} <--- wrong")
    print(f"- Probability that exactly two users (any two) are accessing the network: {probability_exactly_2_users}\n")
    ''' Problem 3 Solution '''
    # Number of users (CHANGE THIS FOR PROBLEM 3)
    n_3 = int(input("assume num of users: "))


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
    print(f"- Probability that at least {N} users are accessing the network: {probability_at_least_18_users} <--- wrong \n")
    ''' Problem 4 Solution '''
    low = N
    high = n_3
    while calculate_probability1(N) > 0.0001:
        n_3 -= 1

    print("Solution 4:")
    print(f"- Maximum number of users for 99.99% congestion free: {n_3} <--- wrong")

elif question == 5:
    network_bandwidth = float(input("network bandwidth: ")) * 10 ** 9  # Gbps to bits
    access_link_bandwidth = int(input("access link bandwidth: ")) * 10 ** 6  # Mbps to bits
    web_object_size = int(input("web object size link bandwidth: ")) * 10 ** 3  # Kbits to bits
    average_request_rate = int(input("avg request rate: "))  # requests per second
    response_time = float(input("response time: "))  # seconds
    cache_percentage = int(input("percent in cache: (whole number) "))  # percentage of objects in cache
    invalid_cache_percentage = int(input("percent in cache invalid: (whole number) "))  # percentage of cached objects that are invalid

    response_time = InstitutionalNetworkResponseTimeSolution(network_bandwidth,
                                                             access_link_bandwidth,
                                                             web_object_size,
                                                             average_request_rate,
                                                             response_time,
                                                             cache_percentage,
                                                             invalid_cache_percentage)
    print(response_time.solve())

elif question == 6:
    transmission_rate = int(input("transmission rate: ")) * 10**6  # megabits per second
    number_of_links = int(input("num of links: "))
    number_of_routers = int(input("num of routers: "))
    length_of_link = int(input("length of link: ")) * 10**3  #  kilometers in meters
    signal_propagation_speed = float(input("signal prop speed: ")) * 10**8  #  meters per second
    webpage_size = int(input("webpage size: ")) * 8 * 10**3  #  kilobytes in bits
    number_of_images = int(input("num of images: "))
    image_size = int(input("image size: ")) * 8 * 10**3  #  kilobytes in bits
    max_pkt_size = int(input("max packet size: ")) * 8 * 10**3  # In bits

    
    internet_path = InternetPathSolution(transmission_rate,
                                         number_of_links,
                                         number_of_routers,
                                         length_of_link,
                                         signal_propagation_speed,
                                         webpage_size,
                                         number_of_images,
                                         image_size, max_pkt_size)
    print(internet_path.solve())