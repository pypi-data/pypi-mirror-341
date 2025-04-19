#!/usr/bin/env python3

import os
import time
import argparse
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from datetime import datetime
from pathlib import Path

console = Console()

# === CLASSY BANNER ===
logo = Text()
logo.append("PingThis", style="bold white")
console.print(Panel(logo, title="Internal Network Tool", subtitle="Built with ♥ in Python", expand=False))

# === ARGUMENTS ===
parser = argparse.ArgumentParser(description="Ping multiple hosts with sexy terminal output.")
parser.add_argument('--host', nargs='+', required=True, help='List of hosts or IPs to ping')
parser.add_argument('--count', type=int, default=3, help='Number of ping attempts')
parser.add_argument('--silent', action='store_true', help='Hide individual ping status')

args = parser.parse_args()

# === LOG SETUP ===
log_dir = Path.home() / ".pingthis"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "log.txt"

def log(msg):
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

# === PING FUNCTION ===
def ping_host(host, count, silent):
    successes = 0
    for i in range(count):
        if not silent:
            console.print(f"[white]Pinging[/white] [bold yellow]{host}[/bold yellow]... ({i+1}/{count})")
        response = os.system(f"ping -c 1 {host} > /dev/null")
        if response == 0:
            if not silent:
                console.print("[green]✔ Host is UP[/green]\n")
            successes += 1
        else:
            if not silent:
                console.print("[red]✖ Host is DOWN or unreachable[/red]\n")
        time.sleep(0.5)
    return successes > 0

# === MAIN LOOP ===
results = []

for host in args.host:
    status = ping_host(host, args.count, args.silent)
    results.append((host, status))
    log(f"{host} - {'UP' if status else 'DOWN'}")

# === SHOW SUMMARY TABLE ===
table = Table(title="Ping Summary")

table.add_column("Host", style="bold white")
table.add_column("Status", justify="center")

for host, status in results:
    table.add_row(host, "[green]✅ UP[/green]" if status else "[red]❌ DOWN[/red]")

console.print(table)

