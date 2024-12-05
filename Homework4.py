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

# SYNACK - 3 PART (CORRECT)
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

    first_segment = int(input("Bytes in first segment: "))
    second_segment = int(input("Bytes in second segment: "))
    third_segment = int(input("Bytes in third segment: "))

    # Calculations
    syn_segment = get_segment_details()
    # Part 1: SYN Segment from A to B
    dest_port_a = hex_to_dec(syn_segment[1])
    source_port_b = hex_to_dec(syn_segment[0])
    seq_number_b = hex_to_dec(syn_segment[2])
    ack_number_a = hex_to_dec(syn_segment[3])

    
    source_port_a = dest_port_a  # A to B uses B's destination port
    dest_port_b = source_port_b # A's destination port is B's source port
    seq_number_a = seq_number_b - first_segment - 1  # Sequence number starts slightly less than B's SYNACK seq number
    syn_flag_a, ack_flag_a, fin_flag_a = 1, 0, 0  # SYN=1, ACK=0, FIN=0 for SYN segment

    part1 = f"{dest_port_b},{source_port_a},{seq_number_a},{syn_flag_a},{ack_flag_a},{fin_flag_a}"

    # Part 2: SYNACK Segment from B to A
    syn_flag_b, ack_flag_b, fin_flag_b = 1, 1, 0  # SYN=1, ACK=1, FIN=0 for SYNACK
    part2 = f"{dest_port_a},{source_port_b},{ack_number_a - 1},{seq_number_b - first_segment},{syn_flag_b},{ack_flag_b},{fin_flag_b}"

    # Part 3: First Data Segment from A to B
    syn_flag_data, ack_flag_data, fin_flag_data = 0, 1, 0  # SYN=0, ACK=1, FIN=0 for data
    part3 = f"{dest_port_b},{source_port_a},{seq_number_b - first_segment},{ack_number_a},{syn_flag_data},{ack_flag_data},{fin_flag_data}"

    # Combine parts
    result = f"{part1};{part2};{part3}"
    return result

# TCP Procedure for Estimating RTT (3/5) -> (CORRECT NEW CODE)
def tcp_rtt_estimation():
    # Collect initial values
    # estimated_rtt = float(input("Enter the current estimated RTT (ms): "))  # Initial RTT
    # deviation = float(input("Enter the current deviation (ms): "))  # Initial deviation
    # alpha = 0.125  # Smoothing factor for RTT
    # beta = 0.25    # Smoothing factor for deviation

    # # Input transmission times and ACK times
    # transmission_times = list(map(int, input("Enter transmission times (comma-separated, ms): ").split(',')))
    # ack_times = list(map(int, input("Enter ACK times (comma-separated, ms): ").split(',')))

    # # Calculate RTT samples, excluding retransmissions
    # sample_rtts = []
    # acknowledged_segments = set()  # Track already acknowledged segments
    # for tx, ack in zip(transmission_times, ack_times):
    #     if ack not in acknowledged_segments:
    #         sample_rtts.append(ack - tx)
    #         acknowledged_segments.add(ack)

    # print(f"Sample RTTs (excluding retransmissions): {sample_rtts}")

    # # Initialize variables to store intermediate and final results
    # first_rtt_estimation = None
    # first_deviation = None
    # final_rtt_estimation = None
    # final_deviation = None
    # timeout_interval = None

    # # Process RTT samples
    # for i, sample_rtt in enumerate(sample_rtts):
    #     if i == 0:
    #         # Update after the first RTT sample
    #         estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
    #         deviation = (1 - beta) * deviation + beta * abs(sample_rtt - estimated_rtt)
    #         first_rtt_estimation = estimated_rtt
    #         first_deviation = deviation
    #     else:
    #         # Update for subsequent RTT samples
    #         estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
    #         deviation = (1 - beta) * deviation + beta * abs(sample_rtt - estimated_rtt)

    # # Final results after processing all RTT samples
    # final_rtt_estimation = estimated_rtt
    # final_deviation = deviation
    # timeout_interval = final_rtt_estimation + 4 * final_deviation

    # # Print intermediate and final results
    # print(f"After 1st RTT Sample: EstimatedRTT = {first_rtt_estimation:.1f}, Deviation = {first_deviation:.1f}")
    # print(f"Final Outputs: EstimatedRTT = {final_rtt_estimation:.1f}, Deviation = {final_deviation:.1f}, TimeoutInterval = {timeout_interval:.1f}\n")
    
    # # Return all results as a comma-separated string
    # return f"{first_rtt_estimation:.1f},{first_deviation:.1f},{final_rtt_estimation:.1f},{final_deviation:.1f},{timeout_interval:.1f}"

    Current_RTT = int(input("Enter the current estimated RTT: "))
    Current_DEV = int(input("Enter the current deviation: ")) 
    TRANS_1 = int(input("transmission time #1: "))
    TRANS_2 = int(input("transmission time #2: "))
    TRANS_3 = int(input("transmission time #3: "))
    TRANS_4 = int(input("transmission time #4: "))
    TRANS_5 = int(input("transmission time #5: "))
    ACK_1 = int(input("ACK time #1: "))
    ACK_2 = int(input("ACK time #3: "))
    ACK_3 = int(input("ACK time #4: "))
    ACK_4 = int(input("ACK time #2: ")) #Repeat

    RTT_1 = ACK_1 - TRANS_1 #1 seg
    RTT_2 = ACK_2 - TRANS_3 #3 seg
    RTT_3 = ACK_3 - TRANS_4 #4 seg
    #2nd segment can't be used because retransmission

    ERT_0 = Current_RTT
    ERT_1 = (1-0.125)*ERT_0 + 0.125 * RTT_1
    ERT_2 = (1-0.125)*ERT_1 + 0.125 * RTT_2
    ERT_3 = (1-0.125)*ERT_2 + 0.125 * RTT_3

    DEV_0 = Current_DEV
    DEV_1 = (1-0.25)*DEV_0 + 0.25 * abs(RTT_1 - ERT_1)
    DEV_2 = (1-0.25)*DEV_1 + 0.25 * abs(RTT_2 - ERT_2)
    DEV_3 = (1-0.25)*DEV_2 + 0.25 * abs(RTT_3 - ERT_3)

    # print(ERT_1 + 4 * DEV_1)
    # print(ERT_2 + 4 * DEV_2)

    #Round these up to 1 decimal place
    print("This is answer 1:", round(ERT_1,1))#maybe #1
    print("This is answer 2:", round(DEV_1,1))#2
    print("This is answer 3:", round(ERT_3,1))#3
    print("This is answer 4:", round(DEV_3,1))#4
    print("This is answer 5:", round((ERT_3 + 4 * DEV_3),1))

# Ssthresh value (3/5)
def tcp_window_calculations():
    # Constants
    # ssthresh = int(input("initial ssthresh: "))  # Slow Start Threshold (in MSS)
    # advertised_window = int(input("advertised window: "))  # Receiver window size (in MSS)
    # initial_cwnd = int(input("initial cwnd: "))  # Initial cwnd size (in MSS)

    # # Question 1: TCP window size after 39 new ACKs
    # new_acks = int(input("Q1: num of new acks: "))
    # cwnd = initial_cwnd
    # for _ in range(new_acks):
    #     cwnd = min(cwnd + 1, advertised_window)  # Increase cwnd by 1 MSS per ACK, limited by advertised window
    # answer_1 = cwnd

    # # Question 2: New ACKs needed to reach 57 MSS
    # cwnd = initial_cwnd
    # new_window_size = int(input("Q2: new window size: "))
    # ack_count = 0
    # while cwnd < new_window_size:
    #     cwnd += 1
    #     ack_count += 1
    # answer_2 = ack_count

    # # Question 3: TCP window size after cwnd reaches 88 MSS and 88 ACKs are received
    # cwnd2 = int(input("Q3: new TCP window size: "))
    # advertised_window = int(input("Q3: new advertised window: "))
    # for _ in range(cwnd):
    #     cwnd = min(cwnd + 1, advertised_window)  # Limited by advertised receiver window size
    # answer_3 = cwnd

    # # Question 4: TCP Tahoe behavior after 4 duplicate ACKs
    # cwnd = 88
    # cwnd = 1  # TCP Tahoe resets cwnd to 1 MSS on duplicate ACKs
    # answer_4 = cwnd

    # # Question 5: TCP Reno behavior after 4 duplicate ACKs
    # cwnd2 = cwnd2 // 2  # TCP Reno halves the cwnd
    # answer_5 = cwnd2

    # # Question 6: Timeout recovery to 88 MSS
    # cwnd2 = 1  # cwnd resets to 1 MSS on timeout
    # ack_count = 0
    # while cwnd2 < cwnd2:
    #     cwnd2 += 1
    #     ack_count += 1
    # answer_6 = ack_count

    # # Returning all answers as a comma-separated string
    # return f"{answer_1},{answer_2}(x),{answer_3},{answer_4},{answer_5}(x),{answer_6}(x)"

    ssthresh = int(input("initial ssthresh: "))  # ssthresh is 52 MSS
    advertised_window = int(input("advertised window: "))  # Receiver window size (in MSS)
    initial_cwnd = int(input("initial cwnd: "))  # Initial cwnd size (in MSS)
    #Q1
    new_acks_in_a_row = int(input("received in a row: "))  # Number of new ACKs received in a row
    #Q2
    Before_TCP_window_size = int(input("before TCP window size reaches: "))
    #Q3
    After_TCP_window_size = int(input("after TCP window size reaches: "))
    New_Consecutive_ACKs = int(input("new consecutive ACKs received(should be the same as above): "))
    last_ad_window_size = int(input("last advertised window: "))
    #Q4 & Q5 & Q6
    Duplicate_ACKs = 4

    #Answer 1
    congestion_window_size = initial_cwnd + new_acks_in_a_row 
    print("\n",min(advertised_window, congestion_window_size))

    #Answer 2
    New_ACKs_needed = ssthresh - initial_cwnd
    n = ssthresh
    while n < Before_TCP_window_size:
      New_ACKs_needed += n
      n += 1
    print(New_ACKs_needed)

    #Answer 3
    congestion_window_size = After_TCP_window_size
    n = New_Consecutive_ACKs
    while n > 0:
      if (n // congestion_window_size > 0):
        congestion_window_size += 1
        n = n - congestion_window_size
    placeholder = min(advertised_window, congestion_window_size)
    print(min(placeholder, last_ad_window_size))

    #Answer 4 - Tahoe
    Extra_ACKs = Duplicate_ACKs
    if not Extra_ACKs < 3:
      congestion_window_size = 0
    else:
      congestion_window_size = initial_cwnd + Duplicate_ACKs
    while not Extra_ACKs < Duplicate_ACKs:
      Extra_ACKs = Duplicate_ACKs - 3
      congestion_window_size += 1
    print(min(congestion_window_size, advertised_window))

    #Answer 5 - Reno
    Extra_ACKs = Duplicate_ACKs
    Change_ssthresh = After_TCP_window_size
    if not Extra_ACKs < 3:
      Change_ssthresh = Change_ssthresh // 2
      congestion_window_size = Change_ssthresh + 3
    else:
      congestion_window_size = initial_cwnd + Duplicate_ACKs
    while not Extra_ACKs < Duplicate_ACKs:
      Extra_ACKs = Duplicate_ACKs - 3
      congestion_window_size += 1
    print(min(congestion_window_size, advertised_window))

    #Answer 6
    congestion_window_size = 1
    Change_ssthresh = After_TCP_window_size // 2
    New_ACKs_needed = Change_ssthresh - congestion_window_size
    n = New_ACKs_needed + 1
    if (After_TCP_window_size > advertised_window):
      After_TCP_window_size = advertised_window
    while n < After_TCP_window_size:
      New_ACKs_needed += n
      n += 1
    print(New_ACKs_needed)


#SYNACK - 4 PART (CORRECT)
def calculate_synack():
    # Collect known values
    number_of_segments = int(input("How many segments did Computer A send to Computer B?: "))

    # Gather length in bytes of each segment
    segment_lengths = [] # stores lengths of all segments from Computer A to Computer B
    for i in range(1, number_of_segments + 1):
        print(f"Length of segment #{i}: ")
        length = int(input()) # in bytes
        segment_lengths.append(length)
    # Gather hex value of first 12 bytes of second segment
    hex = input("\nHEX value of first 12 bytes of the second segment (spaces in between blocks): ")
        # Convert the hex value to a list for easier parsing
    hex = hex.split()
    # print(hex)
    cpu_b_segment = int(input("\nLength of segment from Copmuter B: "))


    '''
    Solution 1
    '''

    # Find sequence number of the segment from Computer B
    # The seqeuence # is the last 2 HEX groups converted to decimal
    last_two_hex = hex[-2] + hex[-1]
    sequence_number_1 = int(last_two_hex, 16)

    # Find the acknowledgment number
    # The acknowledgment number is the 3rd and 4th HEX groups converted to decimal + the number of bytes in the second segment
    third_and_fourth_hex = hex[2] + hex[3]
    ack_1 = int(third_and_fourth_hex, 16)
    acknowledgment_number_1 = ack_1 + segment_lengths[1]

    '''
    Solution 2:
    '''
    # Sequence number remains the same
    # Acknowledgement number is the initial acknowledgment number minus the # of bytes in first segment
    acknowledgment_number_2 = ack_1 - segment_lengths[0]

    '''
    Solution 3:
    '''
    # Sequence number = initial sequence number + # of bytes in segment from Computer B
    sequence_number_3 = sequence_number_1 + cpu_b_segment
    # Acknowledgment number is the same as the first one
    '''
    Solution 4:
    '''

    sequence_number_4 = sequence_number_1 - 1

    # Print answer in desired format
    print("\nFormatted Answer:\n\n")

    print(f"{sequence_number_1},{acknowledgment_number_1};{sequence_number_1},{acknowledgment_number_2};{acknowledgment_number_1},{sequence_number_3};{sequence_number_4},{acknowledgment_number_2}")


question = int(input("Which question?\n 1 = Selective Repeat Protocol\n 2 = Synack - 3 Parts\n 3 = Synack - 4 Parts\n 4 = TCP Procedure for Estimating RTT\n 5 = Ssthresh value\n"))
if question == 1:
    result = SelectiveRepeat()
    print("Result:", result)

elif question == 2:
    print(calculate_tcp_details())

elif question == 3:
    calculate_synack()

elif question == 4:
   print(tcp_rtt_estimation())

elif question == 5:
    print(tcp_window_calculations())