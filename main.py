from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.text import Text
import ipaddress
import random

console = Console()

def generate_network():
    """Generate a random Class A, B, or C network."""
    class_type = random.choice(['A', 'B', 'C'])
    if class_type == 'A':
        first_octet = random.randint(1, 126)
        cidr = 8
    elif class_type == 'B':
        first_octet = random.randint(128, 191)
        cidr = 16
    else:
        first_octet = random.randint(192, 223)
        cidr = 24
    network = f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.0/{cidr}"
    return ipaddress.IPv4Network(network, strict=False)

def subnetting_quiz():
    console.clear()
    console.rule("[bold blue]Subnetting Practice Tool[/bold blue]")
    print("[bold cyan]Welcome to the Subnetting Practice Tool![/bold cyan]\n")
    total_questions = IntPrompt.ask("How many questions would you like to attempt?", default=5)
    score = 0

    for question_num in range(1, total_questions + 1):
        network = generate_network()
        max_subnets = 2 ** (32 - network.prefixlen)
        required_subnets = random.choice([2, 4, 8, 16, 32, 64])
        while required_subnets > max_subnets:
            required_subnets = random.choice([2, 4, 8, 16, 32, 64])

        console.rule(f"[bold green]Question {question_num}[/bold green]")
        print(f"You have the network: [bold yellow]{network.with_netmask}[/bold yellow]")
        print(f"You need to create at least [bold magenta]{required_subnets} subnets[/bold magenta].\n")

        # Step 1: Calculate Bits to Borrow
        correct_bits = 0
        while 2 ** correct_bits < required_subnets:
            correct_bits += 1
        user_bits = IntPrompt.ask("1️⃣ How many bits will you borrow from the host portion?")
        if user_bits == correct_bits:
            print("[bold green]✅ Correct![/bold green]")
            score += 1
        else:
            print(f"[bold red]❌ Incorrect.[/bold red] The correct number of bits is [bold yellow]{correct_bits}[/bold yellow].")

        # Step 2: Calculate New Subnet Mask
        new_prefix = network.prefixlen + correct_bits
        new_netmask = ipaddress.IPv4Network(f"0.0.0.0/{new_prefix}").netmask
        user_netmask = Prompt.ask("2️⃣ What is the new subnet mask?")
        if user_netmask.strip() == str(new_netmask):
            print("[bold green]✅ Correct![/bold green]")
            score += 1
        else:
            print(f"[bold red]❌ Incorrect.[/bold red] The correct subnet mask is [bold yellow]{new_netmask}[/bold yellow].")

        # Step 3: Calculate Number of Hosts per Subnet
        host_bits = 32 - new_prefix
        num_hosts = (2 ** host_bits) - 2
        user_hosts = IntPrompt.ask("3️⃣ How many usable hosts per subnet are available?")
        if user_hosts == num_hosts:
            print("[bold green]✅ Correct![/bold green]")
            score += 1
        else:
            print(f"[bold red]❌ Incorrect.[/bold red] The correct number of hosts is [bold yellow]{num_hosts}[/bold yellow].")

        # Step 4: List Subnet Information
        list_subnets = Prompt.ask("4️⃣ Would you like to see the subnet details? (yes/no)", choices=["yes", "no"], default="no")
        if list_subnets.lower() == "yes":
            subnets = list(network.subnets(prefixlen_diff=correct_bits))
            table = Table(title="Subnet Details", show_header=True, header_style="bold blue")
            table.add_column("Subnet", style="dim")
            table.add_column("Network Address", style="bold cyan")
            table.add_column("First Host", style="green")
            table.add_column("Last Host", style="green")
            table.add_column("Broadcast Address", style="bold magenta")

            for idx, subnet in enumerate(subnets):
                hosts = list(subnet.hosts())
                table.add_row(
                    f"{idx + 1}",
                    str(subnet.network_address),
                    str(hosts[0]),
                    str(hosts[-1]),
                    str(subnet.broadcast_address)
                )
            console.print(table)

        print("\n")

    console.rule("[bold magenta]Quiz Complete![/bold magenta]")
    print(f"Your total score is: [bold green]{score}[/bold green] out of [bold yellow]{total_questions * 3}[/bold yellow]\n")
    print("[bold cyan]Thank you for using the Subnetting Practice Tool![/bold cyan]")

if __name__ == "__main__":
    subnetting_quiz()
