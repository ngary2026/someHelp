# Selective Repeat Protocol (CORRECT)
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

# SYNACK - 3 PART
def calculate_tcp_details():
    # Input: Header details in hexadecimal
    def parse_segment_input():
        """Parse a hexadecimal TCP segment input from the user."""
        while True:
            hex_input = input("Enter the hexadecimal segment (e.g., '07CB EDD1 003A E620 0000 0BB8'): ").strip()
            parts = hex_input.split()
            if len(parts) == 6:  # Ensure exactly 6 parts are provided
                return parts
            print("Invalid input. Please enter exactly 6 hexadecimal values separated by spaces.")

    def get_bit_input(prompt):
        """Helper function to get a binary flag (0 or 1)."""
        while True:
            value = input(prompt).strip()
            if value in {"0", "1"}:
                return int(value)
            print("Invalid input. Please enter 0 or 1.")

    def get_segment_details():
        """Get segment details dynamically from user input."""
        hex_parts = parse_segment_input()
        
        # Map hexadecimal parts to corresponding fields
        source_port_b, dest_port_a = hex_parts[0], hex_parts[1]
        seq_number_b = hex_parts[2] + hex_parts[3]
        ack_number_a = hex_parts[4] + hex_parts[5]
        
        return source_port_b, dest_port_a, seq_number_b, ack_number_a

    def hex_to_dec(hex_value):
        """Convert hexadecimal string to decimal integer."""
        return int(hex_value, 16)


    # Calculations
    syn_segment = get_segment_details()
    # Part 1: SYN Segment from A to B
    dest_port_a = hex_to_dec(syn_segment[1])
    source_port_b = hex_to_dec(syn_segment[0])
    seq_number_b = hex_to_dec(syn_segment[2])
    ack_number_a = hex_to_dec(syn_segment[3])

    source_port_a = dest_port_a  # A to B uses B's destination port
    dest_port_b = source_port_b # A's destination port is B's source port
    seq_number_a = seq_number_b - 1  # Sequence number starts slightly less than B's SYNACK seq number
    syn_flag_a, ack_flag_a, fin_flag_a = 1, 0, 0  # SYN=1, ACK=0, FIN=0 for SYN segment

    part1 = f"{dest_port_b},{source_port_a},{seq_number_a},{syn_flag_a},{ack_flag_a},{fin_flag_a}"

    # Part 2: SYNACK Segment from B to A
    syn_flag_b, ack_flag_b, fin_flag_b = 1, 1, 0  # SYN=1, ACK=1, FIN=0 for SYNACK
    part2 = f"{dest_port_a},{source_port_b},{2999},{seq_number_a + 1},{syn_flag_b},{ack_flag_b},{fin_flag_b}"

    # Part 3: First Data Segment from A to B
    syn_flag_data, ack_flag_data, fin_flag_data = 0, 1, 0  # SYN=0, ACK=1, FIN=0 for data
    part3 = f"{dest_port_b},{source_port_a},{seq_number_a + 1},{seq_number_b},{syn_flag_data},{ack_flag_data},{fin_flag_data}"

    # Combine parts
    result = f"{part1};{part2};{part3}"
    return result

# TCP RTT Procedure
def tcp_rtt_estimation():
    # Collect initial values
    estimated_rtt = float(input("Enter the current estimated RTT (ms): "))  # Initial RTT
    deviation = float(input("Enter the current deviation (ms): "))  # Initial deviation
    alpha = 0.125  # Smoothing factor for RTT
    beta = 0.25    # Smoothing factor for deviation

    # Input transmission times and ACK times
    transmission_times = list(map(int, input("Enter transmission times (comma-separated, ms): ").split(',')))
    ack_times = list(map(int, input("Enter ACK times (comma-separated, ms): ").split(',')))

    # Calculate RTT samples
    sample_rtts = [ack - tx for ack, tx in zip(ack_times, transmission_times)]
    print(f"Sample RTTs: {sample_rtts}")

    # Initialize variables to store intermediate and final results
    first_rtt_estimation = None
    first_deviation = None
    final_rtt_estimation = None
    final_deviation = None
    timeout_interval = None

    # Process RTT samples
    for i, sample_rtt in enumerate(sample_rtts):
        if i == 0:
            # Update after the first RTT sample
            estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
            deviation = (1 - beta) * deviation + beta * abs(sample_rtt - estimated_rtt)
            first_rtt_estimation = estimated_rtt
            first_deviation = deviation
        else:
            # Update for subsequent RTT samples
            estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
            deviation = (1 - beta) * deviation + beta * abs(sample_rtt - estimated_rtt)

    # Final results after processing all RTT samples
    final_rtt_estimation = estimated_rtt
    final_deviation = deviation
    timeout_interval = final_rtt_estimation + 4 * final_deviation

    # Print intermediate and final results
    print(f"After 1st RTT Sample: EstimatedRTT = {first_rtt_estimation:.1f}, Deviation = {first_deviation:.1f}")
    print(f"Final Outputs: EstimatedRTT = {final_rtt_estimation:.1f}, Deviation = {final_deviation:.1f}, TimeoutInterval = {timeout_interval:.1f}")
    
    # Return all results as a comma-separated string
    return f"{first_rtt_estimation:.1f},{first_deviation:.1f},{final_rtt_estimation:.1f}(X),{final_deviation:.1f},{timeout_interval:.1f}(X)"

# Ssthresh value
def tcp_window_calculations():
    # Constants
    ssthresh = int(input("initial ssthresh: "))  # Slow Start Threshold (in MSS)
    advertised_window = int(input("advertised window: "))  # Receiver window size (in MSS)
    initial_cwnd = int(input("initial cwnd: "))  # Initial cwnd size (in MSS)

    # Question 1: TCP window size after 39 new ACKs
    new_acks = int(input("num of new acks: "))
    cwnd = initial_cwnd
    for _ in range(new_acks):
        cwnd = min(cwnd + 1, advertised_window)  # Increase cwnd by 1 MSS per ACK, limited by advertised window
    answer_1 = cwnd

    # Question 2: New ACKs needed to reach 57 MSS
    cwnd = initial_cwnd
    new_window_size = int(input("new window size: "))
    ack_count = 0
    while cwnd < new_window_size:
        cwnd += 1
        ack_count += 1
    answer_2 = ack_count

    # Question 3: TCP window size after cwnd reaches 88 MSS and 88 ACKs are received
    cwnd2 = int(input("new TCP window size: "))
    advertised_window = int(input("new advertised window: "))
    for _ in range(cwnd):
        cwnd = min(cwnd + 1, advertised_window)  # Limited by advertised receiver window size
    answer_3 = cwnd

    # Question 4: TCP Tahoe behavior after 4 duplicate ACKs
    cwnd = 88
    cwnd = 1  # TCP Tahoe resets cwnd to 1 MSS on duplicate ACKs
    answer_4 = cwnd

    # Question 5: TCP Reno behavior after 4 duplicate ACKs
    cwnd2 = cwnd2 // 2  # TCP Reno halves the cwnd
    answer_5 = cwnd2

    # Question 6: Timeout recovery to 88 MSS
    cwnd2 = 1  # cwnd resets to 1 MSS on timeout
    ack_count = 0
    while cwnd2 < cwnd2:
        cwnd2 += 1
        ack_count += 1
    answer_6 = ack_count

    # Returning all answers as a comma-separated string
    return f"{answer_1},{answer_2}(x),{answer_3},{answer_4},{answer_5}(x),{answer_6}(x)"


question = int(input("Which question?\n 1 = Selective Repeat Protocol\n 2 = Synack - 3 Parts\n 3 = TCP RTT Procedure\n 4 = Ssthresh value\n"))
if question == 1:
    result = SelectiveRepeat()
    print("Result:", result)

elif question == 2:
    print(calculate_tcp_details())

elif question == 3:
    print(tcp_rtt_estimation())

elif question == 4:
   print(tcp_window_calculations())