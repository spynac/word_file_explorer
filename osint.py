import requests
import whois
import dns.resolver
from rich.console import Console
from rich.table import Table
import asyncio
import aiohttp

# Initialize rich console
console = Console()

# Function: Display header
def display_header():
    console.print("[bold magenta]" + "=" * 80 + "[/bold magenta]")
    console.print("[bold blue] ███████╗███████╗ █████╗ ██████╗ [/bold blue]")
    console.print("[bold blue] ██╔════╝██╔════╝██╔══██╗██╔══██╗[/bold blue]")
    console.print("[bold blue] █████╗  █████╗  ███████║██████╔╝[/bold blue]")
    console.print("[bold blue] ██╔══╝  ██╔══╝  ██╔══██║██╔═══╝ [/bold blue]")
    console.print("[bold blue] ███████╗██║     ██║  ██║██║     [/bold blue]")
    console.print("[bold blue] ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     [/bold blue]")
    console.print("[bold yellow]                      MADE BY SPYNAC[/bold yellow]")
    console.print("[bold magenta]" + "=" * 80 + "[/bold magenta]\n")

# Function: WHOIS Lookup
def whois_lookup(domain):
    console.print(f"\n[bold cyan]Performing WHOIS lookup for: {domain}[/bold cyan]")
    try:
        domain_info = whois.whois(domain)
        console.print("[bold green]WHOIS Results:[/bold green]")
        console.print(f"- [cyan]Domain Name:[/cyan] {domain_info.domain_name}")
        console.print(f"- [cyan]Registrar:[/cyan] {domain_info.registrar}")
        console.print(f"- [cyan]Creation Date:[/cyan] {domain_info.creation_date}")
        console.print(f"- [cyan]Expiration Date:[/cyan] {domain_info.expiration_date}")
        console.print(f"- [cyan]Name Servers:[/cyan] {', '.join(domain_info.name_servers)}")
    except Exception as e:
        console.print(f"[bold red]Error during WHOIS lookup:[/bold red] {e}")

# Function: Reverse IP Lookup
async def reverse_ip_lookup(ip_address):
    console.print(f"\n[bold cyan]Performing reverse IP lookup for: {ip_address}[/bold cyan]")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip_address}") as response:
                if response.status == 200:
                    domains = (await response.text()).splitlines()
                    if domains:
                        console.print("[bold green]Domains hosted on this IP:[/bold green]")
                        for domain in domains:
                            console.print(f"- {domain}")
                    else:
                        console.print("[bold yellow]No domains found for this IP.[/bold yellow]")
                else:
                    console.print("[bold red]Failed to fetch reverse IP data.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

# Function: Social Media Profiler
async def social_media_profiler(username):
    platforms = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "GitHub": f"https://github.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://facebook.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}"
    }
    console.print(f"\n[bold cyan]Checking social media profiles for: {username}[/bold cyan]")
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(check_profile(session, platform, url)) for platform, url in platforms.items()]
        await asyncio.gather(*tasks)

async def check_profile(session, platform, url):
    try:
        async with session.head(url, allow_redirects=True) as response:
            if response.status == 200:
                console.print(f"[bold green]{platform} profile found:[/bold green] {url}")
            else:
                console.print(f"[bold yellow]{platform} profile not found.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error checking {platform}:[/bold red] {e}")

# Function: Email Breach Checker
async def email_breach_checker(email):
    console.print(f"\n[bold cyan]Checking breaches for: {email}[/bold cyan]")
    email_domain = email.split('@')[-1]
    potential_sources = [
        f"https://api.hackertarget.com/hostsearch/?q={email_domain}",
        f"https://leakcheck.net/api/?key=test&check={email}",
        f"https://hunter.io/search/?email={email}"
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_email_data(session, url)) for url in potential_sources]
        await asyncio.gather(*tasks)

async def fetch_email_data(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                console.print(f"[bold green]Data fetched from {url}:[/bold green]")
                console.print(data)
            else:
                console.print(f"[bold yellow]No data found at {url}.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error fetching data from {url}:[/bold red] {e}")

# Function: DNS Lookup
async def dns_lookup(domain):
    console.print(f"\n[bold cyan]Performing DNS lookup for: {domain}[/bold cyan]")
    record_types = ["A", "MX", "NS", "TXT", "CNAME", "SOA"]
    tasks = [asyncio.create_task(fetch_dns_records(domain, record)) for record in record_types]
    await asyncio.gather(*tasks)

async def fetch_dns_records(domain, record):
    try:
        answers = dns.resolver.resolve(domain, record, raise_on_no_answer=False)
        if answers:
            console.print(f"[bold green]{record} Records:[/bold green]")
            for rdata in answers:
                console.print(f"- {rdata}")
        else:
            console.print(f"[bold yellow]No {record} records found.[/bold yellow]")
    except dns.resolver.NoAnswer:
        console.print(f"[bold yellow]No {record} records found.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error fetching {record} records:[/bold red] {e}")

# Main Menu
def main_menu():
    display_header()
    while True:
        console.print("\n[bold cyan]Main Menu:[/bold cyan]")
        console.print("[1] WHOIS Lookup")
        console.print("[2] Reverse IP Lookup")
        console.print("[3] Social Media Profiler")
        console.print("[4] Email Breach Checker")
        console.print("[5] DNS Lookup")
        console.print("[6] Quit")
        choice = console.input("\n[bold yellow]Enter your choice (1-6): [/bold yellow]")

        if choice == "1":
            domain = console.input("[bold yellow]Enter the domain for WHOIS lookup: [/bold yellow]")
            whois_lookup(domain)
        elif choice == "2":
            ip_address = console.input("[bold yellow]Enter the IP address for reverse lookup: [/bold yellow]")
            asyncio.run(reverse_ip_lookup(ip_address))
        elif choice == "3":
            username = console.input("[bold yellow]Enter the username to search: [/bold yellow]")
            asyncio.run(social_media_profiler(username))
        elif choice == "4":
            email = console.input("[bold yellow]Enter the email to check for breaches: [/bold yellow]")
            asyncio.run(email_breach_checker(email))
        elif choice == "5":
            domain = console.input("[bold yellow]Enter the domain for DNS lookup: [/bold yellow]")
            asyncio.run(dns_lookup(domain))
        elif choice == "6":
            console.print("[bold green]Exiting Efap. Goodbye![/bold green]")
            break
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

if __name__ == "__main__":
    main_menu()
