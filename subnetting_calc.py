import ipaddress
import random
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax

console = Console()

# Load the help content
with open('help.json', 'r') as f:
    help_content = json.load(f)

def display_help(operation):
    if operation in help_content:
        help_info = help_content[operation]
        console.print(Panel(
            f"[bold]Description:[/bold]\n{help_info['description']}\n\n"
            f"[bold]Example:[/bold]\n{help_info['example']}\n\n"
            f"[bold]Real-world Usage:[/bold]\n{help_info['real_world_usage']}\n\n"
            f"[bold]Tips:[/bold]",
            title=f"Help: {operation.replace('_', ' ').title()}",
            expand=False,
            border_style="green"
        ))
        for tip in help_info['tips']:
            console.print(f"• {tip}")
    else:
        console.print("[bold red]Help information not available for this operation.[/bold red]")

def get_binary_representation(ip_address):
    if isinstance(ip_address, str):
        return '.'.join([bin(int(octet))[2:].zfill(8) for octet in ip_address.split('.')])
    elif isinstance(ip_address, int):
        return format(ip_address, '032b')
    else:
        return '.'.join([bin(int(octet))[2:].zfill(8) for octet in ip_address.packed])

def display_binary_and_calculation(ip, mask, operation="AND"):
    ip_obj = ipaddress.ip_address(ip)
    mask_obj = ipaddress.ip_address(mask)
    result = ipaddress.ip_address(int(ip_obj) & int(mask_obj) if operation == "AND" else int(ip_obj) | int(mask_obj))

    table = Table(title=f"Binary Representation and {operation} Operation")
    table.add_column("", style="cyan")
    table.add_column("Dotted Decimal", style="green")
    table.add_column("Binary", style="yellow")

    table.add_row("IP Address", str(ip_obj), get_binary_representation(ip_obj))
    table.add_row("Subnet Mask", str(mask_obj), get_binary_representation(mask_obj))
    table.add_row(f"{operation} Result", str(result), get_binary_representation(result))

    console.print(table)

    console.print(f"\n[bold]Explanation:[/bold]")
    console.print(f"The {operation} operation is performed bit by bit:")
    ip_bits = get_binary_representation(ip_obj).replace('.', '')
    mask_bits = get_binary_representation(mask_obj).replace('.', '')
    result_bits = get_binary_representation(result).replace('.', '')

    for i in range(0, 32, 8):
        console.print(f"{ip_bits[i:i+8]} {operation.lower()} {mask_bits[i:i+8]} = {result_bits[i:i+8]}")

def parse_input(ip_input):
    try:
        return ipaddress.ip_network(ip_input, strict=False)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return None

def display_subnet_info(network):
    table = Table(title=f"Subnet Information for {network}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    table.add_column("Binary", style="yellow")

    table.add_row("Network Address", str(network.network_address), get_binary_representation(network.network_address))
    table.add_row("Broadcast Address", str(network.broadcast_address), get_binary_representation(network.broadcast_address))
    table.add_row("Subnet Mask", str(network.netmask), get_binary_representation(network.netmask))
    table.add_row("Wildcard Mask", str(network.hostmask), get_binary_representation(network.hostmask))
    table.add_row("Number of Hosts", str(network.num_addresses - 2), "")
    table.add_row("IP Range", f"{network.network_address + 1} - {network.broadcast_address - 1}", "")
    table.add_row("CIDR Notation", f"/{network.prefixlen}", "")
    
    # Calculate and add max possible subnets
    max_subnets = 2 ** (32 - network.prefixlen)
    table.add_row("Max Possible Subnets", str(max_subnets), "")

    console.print(table)
    
    display_binary_and_calculation(network.network_address, network.netmask)

def subnet_division(network, num_subnets):
    try:
        new_prefix = network.prefixlen + (32 - network.prefixlen).bit_length() - (num_subnets - 1).bit_length()
        subnets = list(network.subnets(new_prefix=new_prefix))
        
        table = Table(title=f"Subnet Division for {network}")
        table.add_column("Subnet", style="cyan")
        table.add_column("Network Address", style="green")
        table.add_column("Binary", style="yellow")

        for i, subnet in enumerate(subnets[:num_subnets], 1):
            table.add_row(
                f"Subnet {i}",
                str(subnet.network_address),
                get_binary_representation(subnet.network_address)
            )

        console.print(table)
        console.print(f"\n[bold green]Total subnets created:[/bold green] {num_subnets}")
        console.print(f"[bold green]New subnet mask:[/bold green] {subnets[0].netmask} (/{new_prefix})")
        
        if len(subnets) > 1:
            subnet_increment = int(subnets[1].network_address) - int(subnets[0].network_address)
            console.print(f"[bold green]Subnet increment:[/bold green] {subnet_increment}")
            console.print(f"[bold green]Subnet increment (binary):[/bold green] {get_binary_representation(subnet_increment)}")
        
        display_binary_and_calculation(subnets[0].network_address, subnets[0].netmask)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

def reverse_subnet_calculation(num_hosts, ip_address):
    prefix = 32 - (num_hosts + 2).bit_length()
    network = ipaddress.ip_network(f"{ip_address}/{prefix}", strict=False)
    
    table = Table(title=f"Reverse Subnet Calculation for {num_hosts} hosts")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Binary", style="yellow")

    table.add_row("IP Address", str(ip_address), get_binary_representation(ip_address))
    table.add_row("Network Address", str(network.network_address), get_binary_representation(network.network_address))
    table.add_row("Broadcast Address", str(network.broadcast_address), get_binary_representation(network.broadcast_address))
    table.add_row("Subnet mask", str(network.netmask), get_binary_representation(network.netmask))
    table.add_row("CIDR notation", f"/{prefix}", "")
    table.add_row("Wildcard mask", str(network.hostmask), get_binary_representation(network.hostmask))
    table.add_row("Actual max hosts", str(network.num_addresses - 2), "")

    console.print(table)
    
    display_binary_and_calculation(ip_address, network.netmask)
    
    console.print("\n[bold]Calculation Explanation:[/bold]")
    console.print(f"1. Number of required bits for hosts: {(num_hosts + 2).bit_length()}")
    console.print(f"2. Subtract from 32 to get prefix: 32 - {(num_hosts + 2).bit_length()} = {prefix}")
    console.print(f"3. This gives us the subnet mask: {network.netmask}")
    console.print(f"4. The network address is calculated by ANDing the IP address with the subnet mask")
    console.print(f"5. The broadcast address is the last address in the network range")

def generate_random_ips(network, count):
    random_ips = random.sample(list(network.hosts()), min(count, network.num_addresses - 2))
    table = Table(title=f"Random IP Addresses from {network}")
    table.add_column("IP Address", style="cyan")
    table.add_column("Binary Representation", style="yellow")
    
    for ip in random_ips:
        table.add_row(str(ip), get_binary_representation(ip))
    
    console.print(table)

def subnet_comparison(ip1, ip2, mask):
    try:
        network1 = ipaddress.ip_network(f"{ip1}/{mask}", strict=False)
        network2 = ipaddress.ip_network(f"{ip2}/{mask}", strict=False)
        
        table = Table(title="Subnet Comparison")
        table.add_column("Property", style="cyan")
        table.add_column("IP 1", style="green")
        table.add_column("IP 2", style="yellow")
        
        table.add_row("IP Address", f"{ip1}\n{get_binary_representation(ip1)}", f"{ip2}\n{get_binary_representation(ip2)}")
        table.add_row("Subnet", f"{network1.network_address}\n{get_binary_representation(network1.network_address)}", f"{network2.network_address}\n{get_binary_representation(network2.network_address)}")
        table.add_row("Broadcast", f"{network1.broadcast_address}\n{get_binary_representation(network1.broadcast_address)}", f"{network2.broadcast_address}\n{get_binary_representation(network2.broadcast_address)}")
        table.add_row("Subnet Mask", f"{network1.netmask}\n{get_binary_representation(network1.netmask)}", f"{network2.netmask}\n{get_binary_representation(network2.netmask)}")
        
        console.print(table)
        
        if network1 == network2:
            console.print("[bold green]The IP addresses are in the same subnet.[/bold green]")
        else:
            console.print("[bold red]The IP addresses are in different subnets.[/bold red]")

        display_binary_and_calculation(ip1, mask)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

def generate_python_code(network):
    code = f"""
import ipaddress

network = ipaddress.ip_network('{network}', strict=False)

print(f"Network Address: {{network.network_address}}")
print(f"Broadcast Address: {{network.broadcast_address}}")
print(f"Subnet Mask: {{network.netmask}}")
print(f"CIDR Notation: /{{network.prefixlen}}")
print(f"Number of Hosts: {{network.num_addresses - 2}}")
print(f"IP Range: {{network.network_address + 1}} - {{network.broadcast_address - 1}}")
print(f"Wildcard Mask: {{network.hostmask}}")

# Generate list of all usable IP addresses
usable_ips = list(network.hosts())
print(f"First usable IP: {{usable_ips[0]}}")
print(f"Last usable IP: {{usable_ips[-1]}}")

# Check if an IP is in this network
test_ip = '{network.network_address + 1}'
print(f"Is {{test_ip}} in the network? {{ipaddress.ip_address(test_ip) in network}}")
    """
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="Python Code for Network Operations", border_style="green"))

def identify_subnet(ip_address, subnet_mask):
    try:
        interface = ipaddress.ip_interface(f"{ip_address}/{subnet_mask}")
        network = interface.network
        
        table = Table(title="Subnet Identification")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Binary", style="yellow")

        table.add_row("IP Address", str(ip_address), get_binary_representation(ip_address))
        table.add_row("Subnet Mask", str(subnet_mask), get_binary_representation(subnet_mask))
        table.add_row("Network Address", str(network.network_address), get_binary_representation(network.network_address))
        table.add_row("Broadcast Address", str(network.broadcast_address), get_binary_representation(network.broadcast_address))
        table.add_row("Subnet", str(network), "")
        table.add_row("Total Hosts", str(network.num_addresses - 2), "")

        console.print(table)
        
        display_binary_and_calculation(ip_address, subnet_mask)
        
        console.print("\n[bold]Calculation Explanation:[/bold]")
        console.print("1. The network address is calculated by ANDing the IP address with the subnet mask.")
        console.print("2. The broadcast address is calculated by ORing the network address with the wildcard mask.")
        console.print(f"3. Wildcard mask: {network.hostmask} ({get_binary_representation(network.hostmask)})")
        
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

def display_menu():
    menu_items = [
        ("1", "Subnet Information", "Detailed subnet breakdown"),
        ("2", "Subnet Division", "Divide network into subnets"),
        ("3", "Reverse Subnet Calculation", "Find subnet mask for hosts"),
        ("4", "Generate Random IPs", "Create random IPs in subnet"),
        ("5", "Subnet Comparison", "Compare two IP addresses"),
        ("6", "Generate Python Code", "Network operations code"),
        ("7", "Identify Subnet", "Find subnet for a given IP"),
        ("q", "Quit", "Exit program")
    ]

    table = Table(show_header=False, expand=False, box=None, padding=(0, 1))
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Option", style="green")
    table.add_column("Description", style="yellow")

    for item in menu_items:
        table.add_row(*item)

    panel = Panel(
        table,
        title="Advanced Subnetting Calculator",
        subtitle="Enter your choice [1-7 or q]:",
        expand=False,
        border_style="blue"
    )
    
    console.print(panel)
    
def main():
    while True:
        console.clear()
        display_menu()
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7", "q"], default="1")

        if choice == 'q':
            break

        console.clear()

        if choice == '1':
            while True:
                ip_input = Prompt.ask("[bold yellow]Enter an IP address with subnet mask (or 'h' for help, 'b' to go back)[/bold yellow]", default="192.168.1.0/24")
                if ip_input.lower() == 'h':
                    display_help("subnet_information")
                elif ip_input.lower() == 'b':
                    break
                else:
                    network = parse_input(ip_input)
                    if network:
                        display_subnet_info(network)
                        break

        elif choice == '2':
            while True:
                ip_input = Prompt.ask("[bold yellow]Enter a network address with subnet mask (or 'h' for help, 'b' to go back)[/bold yellow]", default="192.168.0.0/24")
                if ip_input.lower() == 'h':
                    display_help("subnet_division")
                elif ip_input.lower() == 'b':
                    break
                else:
                    num_subnets = int(Prompt.ask("[bold yellow]Enter the number of subnets[/bold yellow]", default="4"))
                    network = parse_input(ip_input)
                    if network:
                        subnet_division(network, num_subnets)
                        break

        elif choice == '3':
            while True:
                num_hosts_input = Prompt.ask("[bold yellow]Enter the number of required hosts (or 'h' for help, 'b' to go back)[/bold yellow]", default="100")
                if num_hosts_input.lower() == 'h':
                    display_help("reverse_subnet_calculation")
                elif num_hosts_input.lower() == 'b':
                    break
                else:
                    num_hosts = int(num_hosts_input)
                    ip_address = Prompt.ask("[bold yellow]Enter an IP address within the desired subnet[/bold yellow]", default="192.168.1.1")
                    reverse_subnet_calculation(num_hosts, ip_address)
                    break

        elif choice == '4':
            while True:
                ip_input = Prompt.ask("[bold yellow]Enter a network address with subnet mask (or 'h' for help, 'b' to go back)[/bold yellow]", default="192.168.1.0/24")
                if ip_input.lower() == 'h':
                    display_help("generate_random_ips")
                elif ip_input.lower() == 'b':
                    break
                else:
                    count = int(Prompt.ask("[bold yellow]Enter the number of random IPs to generate[/bold yellow]", default="5"))
                    network = parse_input(ip_input)
                    if network:
                        generate_random_ips(network, count)
                        break

        elif choice == '5':
            while True:
                ip1 = Prompt.ask("[bold yellow]Enter the first IP address (or 'h' for help, 'b' to go back)[/bold yellow]", default="192.168.1.10")
                if ip1.lower() == 'h':
                    display_help("subnet_comparison")
                elif ip1.lower() == 'b':
                    break
                else:
                    ip2 = Prompt.ask("[bold yellow]Enter the second IP address[/bold yellow]", default="192.168.1.20")
                    mask = Prompt.ask("[bold yellow]Enter the subnet mask[/bold yellow]", default="255.255.255.0")
                    subnet_comparison(ip1, ip2, mask)
                    break

        elif choice == '6':
            while True:
                ip_input = Prompt.ask("[bold yellow]Enter an IP address with subnet mask (or 'h' for help, 'b' to go back)[/bold yellow]", default="192.168.1.0/24")
                if ip_input.lower() == 'h':
                    display_help("generate_python_code")
                elif ip_input.lower() == 'b':
                    break
                else:
                    network = parse_input(ip_input)
                    if network:
                        generate_python_code(network)
                        break

        elif choice == '7':
            while True:
                ip_input = Prompt.ask("[bold yellow]Enter the IP address (or 'h' for help, 'b' to go back)[/bold yellow]", default="192.168.236.52")
                if ip_input.lower() == 'h':
                    display_help("identify_subnet")
                elif ip_input.lower() == 'b':
                    break
                else:
                    mask_input = Prompt.ask("[bold yellow]Enter the subnet mask[/bold yellow]", default="255.255.255.128")
                    identify_subnet(ip_input, mask_input)
                    break

        console.print("\nPress Enter to continue...")
        console.input()

    console.print(Panel.fit("Thank you for using the Advanced Subnetting Calculator!", border_style="bold green"))

if __name__ == "__main__":
    main()