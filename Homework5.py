import math
from ipaddress import ip_network

# NAT Router (CORRECT)
def nat_router_simulation():
    print("Enter the details of the TCP segment received by the router:")
    
    # User inputs
    nat_ip_addresses = list(map(str, input("Nat router has two IPs (seperate with space): ").split()))
    num_formula = int(input("formula (x + ...) mod 65536: "))
    source_ip = input("Source IP (e.g., 192.128.135.178): ")
    destination_ip = input("Destination IP (e.g., 33.75.185.202): ")
    source_port = int(input("Source Port (e.g., 54033): "))
    destination_port = int(input("Destination Port (e.g., 18201): "))
    
    # NAT router public IP addresses
    nat_public_ip = nat_ip_addresses[1]
    
    # Calculating the new port using the formula
    nat_source_port = (source_port + num_formula) % 65536
    
    # Output for the acknowledgment segment
    ack_source_ip = destination_ip
    ack_destination_ip = nat_public_ip
    ack_source_port = destination_port
    ack_destination_port = nat_source_port
    
    print(f"\n{ack_source_ip},{ack_destination_ip},{ack_source_port},{ack_destination_port}")

# ISP split the subnet (CORRECT)
def isp_split():
    # Get inputs from the user
    base_subnet = input("Enter the base subnet in CIDR format (e.g., 235.80.192.0/18): ").strip()
    first_tier_customers = int(input("Enter the number of customers in the first tier: "))
    second_tier_customers = int(input("Enter the number of customers in the second tier: "))
    
    # Calculate the total number of IPs in the base subnet
    base_network = ip_network(base_subnet)
    total_ips = base_network.num_addresses
    
    # Split the total IPs into two halves
    first_tier_ips = total_ips // 2
    second_tier_ips = total_ips // 2
    
    # Calculate subnets for the first tier
    first_tier_subnet_size = first_tier_ips // first_tier_customers
    first_tier_prefix = 32 - int(math.log2(first_tier_subnet_size))
    first_tier_networks = list(base_network.subnets(new_prefix=first_tier_prefix))[:first_tier_customers]
    
    # Calculate subnets for the second tier
    second_tier_start = list(base_network.subnets(new_prefix=32 - int(math.log2(first_tier_ips))))[1]
    second_tier_subnet_size = second_tier_ips // second_tier_customers
    second_tier_prefix = 32 - int(math.log2(second_tier_subnet_size))
    second_tier_networks = list(second_tier_start.subnets(new_prefix=second_tier_prefix))[:second_tier_customers]
    
    # Output results
    subnets = first_tier_networks + second_tier_networks
    subnet_strings = [str(net) for net in subnets]
    max_hosts_first_tier = first_tier_subnet_size - 2
    max_hosts_second_tier = second_tier_subnet_size - 2
    
    print(",".join(subnet_strings + [str(max_hosts_first_tier), str(max_hosts_second_tier)]))

# Forwarding Table (CORRECT)
def ip_to_binary(ip):
    """Convert an IPv4 address to binary."""
    return ''.join(f'{int(octet):08b}' for octet in ip.split('.'))

def longest_prefix_match():
    print("\nEnter the forwarding table row by row. Enter 'done' when finished.")
    print("Example prefix format:")
    print("00101110 10000110 11000")

    # Input forwarding table with automatic interface assignment
    table = []
    interface_counter = 1

    while True:
        prefix = input(f"Enter prefix for interface {interface_counter} (or 'done' to finish): ").strip()
        if prefix.lower() == "done":
            # Add default interface when "done" is entered
            default_interface = f"default"
            table.append((default_interface, interface_counter))
            break
        # Remove extra spaces but keep binary byte grouping
        formatted_prefix = prefix.replace(" ", "")
        table.append((formatted_prefix, interface_counter))
        interface_counter += 1

    # Input destination addresses
    print("\nNow, enter destination addresses one at a time (or 'done' to finish):")
    print("Example destination:")
    print("47.132.77.20")
    destinations = []

    while True:
        dest = input("Enter destination address (or 'done' to finish): ").strip()
        if dest.lower() == "done":
            break
        destinations.append(dest)

    # Process each destination and find matching interfaces
    print("\nForwarding Results:")
    results = []
    for dest in destinations:
        destination_bin = ip_to_binary(dest)
        longest_match = ""
        selected_interface = None

        for prefix, interface in table:
            if prefix == "default":
                continue  # Skip default for now
            if destination_bin.startswith(prefix):
                # Check for longest match
                if len(prefix) > len(longest_match):
                    longest_match = prefix
                    selected_interface = interface

        # Use default interface if no match
        if not selected_interface:
            selected_interface = table[-1][1]

        results.append(selected_interface)
        print(f"Destination {dest} -> Interface {selected_interface}")

    # Print final results in comma-separated format
    print("\nFinal Answer:", ",".join(map(str, results)))


question = int(input("Which question?\n 1 = NAT Router\n 2 = ISP Split\n 3 = Forwarding Table\n"))
if question == 1:
    nat_router_simulation()
elif question == 2:
    isp_split()
elif question == 3:
    longest_prefix_match()
    