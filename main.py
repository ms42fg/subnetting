from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich.text import Text
import ipaddress
import random
import json
from collections import defaultdict

console = Console()

def decimal_to_binary_octet(decimal):
    """Convert a decimal octet to binary."""
    return format(decimal, '08b')

def binary_converter(ip_address):
    """Convert an IP address to binary representation."""
    return '.'.join(decimal_to_binary_octet(int(octet)) for octet in ip_address.split('.'))

def generate_network(difficulty='beginner'):
    """Generate a random network based on difficulty level using realistic private IP ranges."""
    if difficulty == 'beginner':
        # Use common private IP ranges for beginners
        network_choices = [
            "192.168.0.0/24",    # Common home network
            "192.168.1.0/24",    # Another common home network
            "172.16.0.0/16",     # Small business network
            "10.0.0.0/16"        # Larger business network, but still manageable for beginners
        ]
        network = random.choice(network_choices)
    else:
        # For advanced, use more varied private IP ranges
        first_octet = random.choice([10, 172, 192])
        if first_octet == 10:
            second_octet = random.randint(0, 255)
            third_octet = random.randint(0, 255)
            cidr = random.randint(16, 24)
        elif first_octet == 172:
            second_octet = random.randint(16, 31)
            third_octet = random.randint(0, 255)
            cidr = random.randint(16, 24)
        else:  # 192
            second_octet = 168
            third_octet = random.randint(0, 255)
            cidr = random.randint(24, 28)
        
        network = f"{first_octet}.{second_octet}.{third_octet}.0/{cidr}"
    
    if difficulty == 'beginner':
        required_subnets = random.choice([2, 4, 8])
    else:
        required_subnets = random.randint(2, 32)

    return {
        "network": ipaddress.IPv4Network(network, strict=False),
        "required_subnets": required_subnets
    }

def display_introduction():
    """Display an introduction to subnetting concepts with real-life examples."""
    console.rule("[bold blue]Introduction to Subnetting[/bold blue]")
    print("[bold cyan]Welcome to the Enhanced Subnetting Practice Tool![/bold cyan]\n")
    print("This tool will help you understand subnetting using real-life examples.")
    print("We'll start with beginner-friendly concepts and gradually introduce more advanced topics.")
    
    print("\n[bold underline]Understanding IP Addresses and Subnet Masks:[/bold underline]")
    print("An IP address is like a street address for devices on a network.")
    print("It's made up of four numbers separated by dots, like 192.168.1.1")
    print("\nA subnet mask is used to divide the IP address into network and host portions.")
    print("It looks similar to an IP address, like 255.255.255.0")
    print("\nCIDR notation (like /24) is a shorthand way to write the subnet mask.")
    print("It tells us how many bits are used for the network portion of the address.")
    
    print("\n[bold underline]Real-Life Subnetting Example:[/bold underline]")
    print("Imagine you're setting up a network for a small office building with multiple departments:")
    print("- Marketing Department (15 computers)")
    print("- Sales Department (20 computers)")
    print("- IT Department (10 computers)")
    print("- Management (5 computers)")
    
    print("\nYou have a network address of 192.168.1.0/24 assigned to your building.")
    print("This means:")
    print("- The network address is 192.168.1.0")
    print("- The subnet mask is 255.255.255.0")
    print("- The /24 means the first 24 bits are used for the network, leaving 8 bits for host addresses")
    
    print("\nSubnetting allows you to divide this network into smaller subnetworks for each department.")
    print("This separation improves security and helps manage network traffic more efficiently.")
    
    print("\n[bold]Benefits of Subnetting:[/bold]")
    print("1. [green]Improved Security:[/green] Each department can have its own subnet, limiting access between departments.")
    print("2. [green]Efficient Resource Use:[/green] You can allocate IP addresses more efficiently based on department size.")
    print("3. [green]Better Performance:[/green] Reduced network congestion as broadcast traffic is limited to smaller subnets.")
    
    print("\nLet's dive in and learn how to create these subnets!")

def explain_network(network):
    """Explain the given network in user-friendly terms with a real-life analogy."""
    network_size = "small" if network.prefixlen >= 24 else "medium" if network.prefixlen >= 16 else "large"
    
    console.print(Panel.fit(
        f"Your network address is: [bold yellow]{network.with_netmask}[/bold yellow]\n"
        f"In CIDR notation, this is written as: [bold yellow]{network.with_prefixlen}[/bold yellow]\n\n"
        f"Let's break this down:\n"
        f"1. The IP address {network.network_address} is like the building's street address.\n"
        f"2. The subnet mask {network.netmask} is like the building's floor plan.\n"
        f"3. The '/' notation ({network.prefixlen}) tells us how many bits are used for the network part.\n\n"
        f"In binary, the subnet mask {network.netmask} looks like this:\n"
        f"[bold green]{'.'.join(bin(int(x))[2:].zfill(8) for x in str(network.netmask).split('.'))}[/bold green]\n"
        f"The number of consecutive 1's from the left is {network.prefixlen}, hence the /{network.prefixlen} notation.\n\n"
        f"This means:\n"
        f"- The first {network.prefixlen} bits identify the network (building)\n"
        f"- The remaining {32 - network.prefixlen} bits are for host addresses (rooms)\n\n"
        f"When we create subnets, we're essentially dividing this {network_size} building into separate departments or floors.",
        title="Understanding Your Network",
        border_style="bold blue"
    ))

def display_difficulty_explanation():
    """Explain the difficulty levels to the user."""
    console.print(Panel.fit(
        "Beginner Mode: Focuses on common private network ranges with simple subnet masks.\n"
        "You'll work with easy-to-understand network sizes and straightforward subnetting tasks.\n\n"
        "Advanced Mode: Introduces more varied private IP ranges and more complex network scenarios.\n"
        "You'll encounter a wider range of network sizes and more challenging subnetting problems.",
        title="Difficulty Levels",
        border_style="bold green"
    ))

def load_progress():
    try:
        with open('progress.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"questions": defaultdict(int), "bonus_questions": defaultdict(int)}

def save_progress(progress):
    with open('progress.json', 'w') as f:
        json.dump(progress, f)

def select_question(questions, progress):
    weights = [1 + progress[str(i)] for i in range(len(questions))]
    return random.choices(questions, weights=weights, k=1)[0]

def subnetting_quiz():
    console.clear()
    display_introduction()
    
    display_difficulty_explanation()
    difficulty = Prompt.ask("Choose your difficulty level", choices=["beginner", "advanced"], default="beginner")
    
    if difficulty == "advanced":
        show_explanations = Prompt.ask("Would you like to see detailed explanations?", choices=["yes", "no"], default="no")
    else:
        show_explanations = "yes"
    
    total_questions = IntPrompt.ask("How many questions would you like to attempt?", default=3)
    score = 0
    max_score = total_questions * 4  # Update max score calculation (3 parts + 1 bonus per question)

    # Load questions from JSON file
    with open('qanda.json', 'r') as f:
        json_questions = json.load(f)

    progress = load_progress()

    questions = [generate_network(difficulty) for _ in range(10)]  # Generate 10 different network configurations

    for question_num in range(1, total_questions + 1):
        # Select question based on progress
        question = select_question(questions, progress['questions'])
        question_index = questions.index(question)
        network = question['network']
        required_subnets = question['required_subnets']

        console.rule(f"[bold green]Question {question_num}[/bold green]")
        print(f"You have the network: [bold yellow]{network.with_prefixlen}[/bold yellow]")
        print(f"You need to create at least [bold magenta]{required_subnets} subnets[/bold magenta].\n")

        if show_explanations == "yes":
            explain_network(network)

        if difficulty == 'advanced' and show_explanations == "yes":
            print("\n[bold cyan]Advanced Scenario:[/bold cyan]")
            print("You're a network administrator for a growing tech company.")
            print("The company is expanding and needs to set up a new office complex with multiple departments.")
            print(f"Your task is to create at least {required_subnets} subnets to accommodate this expansion.")

        # Step 1: Calculate Bits to Borrow
        correct_bits = (required_subnets - 1).bit_length()

        if show_explanations == "yes":
            print("\n[bold underline]Step 1: Calculate the Number of Bits to Borrow[/bold underline]")
            print("Let's determine how many bits we need to borrow to create our subnets.")
            print("We'll use a table to show how many subnets we get for each bit borrowed:\n")

            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Bits Borrowed", style="cyan")
            table.add_column("Number of Subnets", style="magenta")
            table.add_column("Enough?", style="green")

            for bits in range(1, 8):
                subnets = 2 ** bits
                enough = "Yes" if subnets >= required_subnets else "No"
                table.add_row(str(bits), str(subnets), enough)

            console.print(table)
            print(f"\nFrom the table, we can see that borrowing [bold yellow]{correct_bits} bits[/bold yellow] gives us enough subnets.")
            print(f"This is the first row where the 'Enough?' column says 'Yes'.")

        user_bits = IntPrompt.ask("\n1️⃣  How many bits will you borrow from the host portion?")
        if user_bits == correct_bits:
            print("[bold green]✅ Correct![/bold green]")
            score += 1
        else:
            print(f"[bold red]❌ Incorrect.[/bold red] The correct number of bits is [bold yellow]{correct_bits}[/bold yellow].")
            progress['questions'][str(question_index)] += 1
            if show_explanations == "no":
                show_explanation = Prompt.ask("Would you like to see the explanation?", choices=["yes", "no"], default="yes")
                if show_explanation == "yes":
                    print("\n[bold underline]Detailed Explanation:[/bold underline]")
                    print("Let's break down why borrowing these bits works:")
                    print(f"1. We need at least {required_subnets} subnets.")
                    print(f"2. In binary, each bit we borrow doubles the number of possible combinations.")
                    print("   This is because each bit can be either 0 or 1.")
                    print("3. Let's see how this works:")
                    
                    for i in range(1, correct_bits + 1):
                        combinations = 2 ** i
                        binary_places = '1' * i
                        print(f"   - With {i} bit{'s' if i > 1 else ''}: {binary_places} in binary")
                        print(f"     This gives us {combinations} combination{'s' if combinations > 1 else ''}")
                        print(f"     ({' | '.join([f'{j:0{i}b}' for j in range(combinations)])})")
                    
                    print(f"\nSo, with {correct_bits} bits, we can create {2 ** correct_bits} subnets, which is enough.")

        # Step 2: Calculate New Subnet Mask
        new_prefix = network.prefixlen + correct_bits
        new_netmask = ipaddress.IPv4Network(f"0.0.0.0/{new_prefix}").netmask
        
        if show_explanations == "yes":
            print("\n[bold underline]Step 2: Determine the New Subnet Mask[/bold underline]")
            print("When we borrow bits, we're making the network part bigger and the host part smaller.")
            print("This changes our subnet mask. Let's see how:")
            
            print(f"\nOriginal subnet mask: {network.netmask}")
            print(f"New subnet mask:      {new_netmask}")
            
            print("\nHere's how it looks in binary:")
            original_netmask_binary = binary_converter(str(network.netmask))
            new_netmask_binary = binary_converter(str(new_netmask))
            print(f"Original: {original_netmask_binary}")
            print(f"New:      {new_netmask_binary}")
            print("Notice how the 1s (network part) have expanded to the right.")
            
            # Real-life analogy for subnet mask
            print("\n[bold cyan]Real-Life Analogy:[/bold cyan]")
            print("Think of the subnet mask as a building's floor plan:")
            print("- The 1s represent walls (network boundaries)")
            print("- The 0s represent open space (host addresses)")
            print("By changing the subnet mask, we're essentially adding more walls to create smaller rooms (subnets).")

        user_netmask = Prompt.ask("\n2️⃣  What is the new subnet mask?")
        if user_netmask.strip() == str(new_netmask):
            print("[bold green]✅ Correct![/bold green]")
            score += 1
        else:
            print(f"[bold red]❌ Incorrect.[/bold red] The correct subnet mask is [bold yellow]{new_netmask}[/bold yellow].")
            progress['questions'][str(question_index)] += 1
            if show_explanations == "no":
                show_explanation = Prompt.ask("Would you like to see the explanation?", choices=["yes", "no"], default="yes")
                if show_explanation == "yes":
                    print("\n[bold underline]Detailed Explanation:[/bold underline]")
                    print("When we borrow bits, we're making the network part bigger and the host part smaller.")
                    print("This changes our subnet mask. Let's see how:")
                    
                    print(f"\nOriginal subnet mask: {network.netmask}")
                    print(f"New subnet mask:      {new_netmask}")
                    
                    print("\nHere's how it looks in binary:")
                    original_netmask_binary = binary_converter(str(network.netmask))
                    new_netmask_binary = binary_converter(str(new_netmask))
                    print(f"Original: {original_netmask_binary}")
                    print(f"New:      {new_netmask_binary}")
                    print("Notice how the 1s (network part) have expanded to the right.")

        # Step 3: Calculate Number of Hosts per Subnet
        host_bits = 32 - new_prefix
        num_hosts = (2 ** host_bits) - 2
        
        if show_explanations == "yes":
            print("\n[bold underline]Step 3: Calculate Number of Usable Hosts per Subnet[/bold underline]")
            print("Now let's find out how many devices (hosts) we can have in each subnet.")
            print("\nFirst, let's understand how we determine the number of host bits:")
            print(f"1. An IPv4 address always has a total of 32 bits.")
            print(f"2. The original network had {network.prefixlen} network bits, leaving {32 - network.prefixlen} host bits.")
            print(f"3. We borrowed {correct_bits} bits for subnetting.")
            print(f"4. So now we have: {network.prefixlen} (original network bits) + {correct_bits} (borrowed bits) = {new_prefix} network bits")
            print(f"5. This leaves us with: 32 - {new_prefix} = {host_bits} host bits")
            
            print(f"\nSo, we have {host_bits} bits left for hosts.")
            print("To calculate the number of hosts, we use this formula: (2^host_bits) - 2")
            print("Let's break it down:")
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Step", style="cyan")
            table.add_column("Calculation", style="magenta")
            table.add_column("Result", style="green")

            table.add_row("1. Calculate 2^host_bits", f"2^{host_bits}", str(2**host_bits))
            table.add_row("2. Subtract 2", f"{2**host_bits} - 2", str(num_hosts))

            console.print(table)
            print(f"\nSo, we can have [bold yellow]{num_hosts}[/bold yellow] usable hosts in each subnet.")
            
            print("\n[bold cyan]Why do we subtract 2?[/bold cyan]")
            print("We subtract 2 because in each subnet:")
            print("1. The first address is reserved for the network address.")
            print("2. The last address is reserved for the broadcast address.")
            print("These two addresses can't be assigned to hosts, hence we subtract them.")
            
            # Real-life example for host calculation
            print("\n[bold cyan]Real-Life Example:[/bold cyan]")
            print(f"In our office building analogy, each subnet (department) can accommodate up to {num_hosts} devices.")
            print("This could represent:")
            print(f"- A small department with up to {num_hosts} computers")
            print(f"- A floor with {num_hosts} networked devices (computers, printers, phones, etc.)")
            print(f"- A section of the building with {num_hosts} IP cameras or IoT devices")

        user_hosts = IntPrompt.ask("\n3️⃣  How many usable hosts per subnet are available?")
        if user_hosts == num_hosts:
            print("[bold green]✅ Correct![/bold green]")
            score += 1
        else:
            print(f"[bold red]❌ Incorrect.[/bold red] The correct number of hosts is [bold yellow]{num_hosts}[/bold yellow].")
            progress['questions'][str(question_index)] += 1
            if show_explanations == "no":
                show_explanation = Prompt.ask("Would you like to see the explanation?", choices=["yes", "no"], default="yes")
                if show_explanation == "yes":
                    print("\n[bold underline]Detailed Explanation:[/bold underline]")
                    print(f"We have {host_bits} bits left for hosts.")
                    print("To calculate the number of hosts, we use this formula: (2^host_bits) - 2")
                    print("Let's break it down:")
                    
                    table = Table(show_header=True, header_style="bold blue")
                    table.add_column("Step", style="cyan")
                    table.add_column("Calculation", style="magenta")
                    table.add_column("Result", style="green")

                    table.add_row("1. Calculate 2^host_bits", f"2^{host_bits}", str(2**host_bits))
                    table.add_row("2. Subtract 2", f"{2**host_bits} - 2", str(num_hosts))

                    console.print(table)
                    print(f"\nSo, we can have [bold yellow]{num_hosts}[/bold yellow] usable hosts in each subnet.")
                    
                    print("\n[bold cyan]Why do we subtract 2?[/bold cyan]")
                    print("We subtract 2 because in each subnet:")
                    print("1. The first address is reserved for the network address.")
                    print("2. The last address is reserved for the broadcast address.")
                    print("These two addresses can't be assigned to hosts, hence we subtract them.")

        # Step 4: Display Subnet Details
        if show_explanations == "yes":
            list_subnets = Prompt.ask("\n4️⃣  Would you like to see the subnet details? (yes/no)", choices=["yes", "no"], default="yes")
            if list_subnets.lower() == "yes":
                subnets = list(network.subnets(prefixlen_diff=correct_bits))
                print("\n[bold underline]Understanding Subnet Details[/bold underline]")
                print("Each subnet has four important addresses:")
                print("1. Network Address: The 'name' of the subnet")
                print("2. First Host: The first usable address for a device")
                print("3. Last Host: The last usable address for a device")
                print("4. Broadcast Address: Used to send messages to all devices in the subnet")
                
                table = Table(title=f"Subnet Details (showing first {min(4, len(subnets))} subnets)", show_header=True, header_style="bold blue")
                table.add_column("Subnet", style="dim")
                table.add_column("Network Address", style="bold cyan")
                table.add_column("First Host", style="green")
                table.add_column("Last Host", style="green")
                table.add_column("Broadcast Address", style="bold magenta")

                for idx, subnet in enumerate(subnets[:4]):  # Limit to first 4 subnets for simplicity
                    hosts = list(subnet.hosts())
                    first_host = str(hosts[0]) if hosts else "N/A"
                    last_host = str(hosts[-1]) if hosts else "N/A"
                    table.add_row(
                        f"{idx + 1}",
                        str(subnet.network_address),
                        first_host,
                        last_host,
                        str(subnet.broadcast_address)
                    )
                console.print(table)

        # Real-life application of subnets
        if show_explanations == "yes":
            print("\n[bold cyan]Real-Life Application:[/bold cyan]")
            print(f"In our office building scenario, these {min(4, len(subnets))} subnets could represent:")
            for idx, subnet in enumerate(subnets[:4]):
                if idx == 0:
                    print(f"Subnet 1: Marketing Department ({num_hosts} available devices)")
                elif idx == 1:
                    print(f"Subnet 2: Sales Department ({num_hosts} available devices)")
                elif idx == 2:
                    print(f"Subnet 3: IT Department ({num_hosts} available devices)")
                elif idx == 3:
                    print(f"Subnet 4: Management ({num_hosts} available devices)")

        # Advanced mode: VLSM explanation
        if difficulty == 'advanced' and show_explanations == "yes":
            print("\n[bold underline]Advanced Topic: Variable Length Subnet Masking (VLSM)[/bold underline]")
            print("In real-world scenarios, different departments often need different numbers of IP addresses.")
            print("VLSM allows us to create subnets of varying sizes to match these needs more efficiently.")
            print("\nFor example, we could allocate our subnets like this:")
            print(f"- Marketing: {num_hosts//2} addresses (using {host_bits-1} host bits)")
            print(f"- Sales: {num_hosts} addresses (using {host_bits} host bits)")
            print(f"- IT: {num_hosts//4} addresses (using {host_bits-2} host bits)")
            print(f"- Management: {num_hosts//8} addresses (using {host_bits-3} host bits)")
            print("\nThis approach minimizes wasted IP addresses and allows for more flexible network design.")
        print("\n")

        # JSON question
        bonus_question = select_question(json_questions, progress['bonus_questions'])
        bonus_question_index = json_questions.index(bonus_question)
        
        console.rule(f"[bold green]Bonus Question {question_num}[/bold green]")
        
        # Display pre-explanation
        console.print(Panel(bonus_question['pre_explanation'], title="Context", border_style="cyan"))
        
        # Display question
        console.print(f"\n[bold yellow]{bonus_question['question']}[/bold yellow]\n")
        
        # Display options
        for i, option in enumerate(bonus_question['options'], 1):
            console.print(f"{i}. {option['text']}")
        
        # Get user answer
        user_answer = IntPrompt.ask("Enter your answer (1-4)", choices=[str(i) for i in range(1, 5)])
        user_answer_text = bonus_question['options'][user_answer - 1]['text']
        
        is_correct = user_answer_text == bonus_question['correct_answer']
        if is_correct:
            console.print("[bold green]✅ Correct![/bold green]")
            score += 1
            explanation_border_style = "green"
        else:
            console.print(f"[bold red]❌ Incorrect.[/bold red] The correct answer is: [bold yellow]{bonus_question['correct_answer']}[/bold yellow]")
            explanation_border_style = "red"
            progress['bonus_questions'][str(bonus_question_index)] += 1
        
        # Display explanation
        console.print(Panel(bonus_question['post_explanation'], title="Explanation", border_style=explanation_border_style))
        print("\n")

        # Save progress after each question
        save_progress(progress)

    console.rule("[bold magenta]Quiz Complete![/bold magenta]")
    print(f"Your total score is: [bold green]{score}[/bold green] out of [bold yellow]{max_score}[/bold yellow]\n")
    print("[bold cyan]Thank you for using the Subnetting Practice Tool![/bold cyan]")
    print("Remember, subnetting takes practice. Don't worry if it seems confusing at first!")

    # Offer additional resources
    print("\n[bold underline]Want to Learn More?[/bold underline]")
    print("Here are some great resources to continue your networking journey:")
    print("1. Cisco's Networking Basics: https://www.netacad.com/courses/networking-basics")
    print("2. Professor Messer's Network+ Course: https://www.professormesser.com/network-plus/n10-008/n10-008-training-course/")
    print("3. Practical Networking: https://www.practicalnetworking.net/")

if __name__ == "__main__":
    subnetting_quiz()
