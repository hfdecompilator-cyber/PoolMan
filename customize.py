#!/usr/bin/env python3
"""CommandCube Customizer - Add Your Own Commands"""

import json
from pathlib import Path

def load_commands():
    """Load existing commands"""
    config_file = Path("commands.json")
    if config_file.exists():
        with open(config_file) as f:
            return json.load(f)
    return {
        "System": {},
        "Files": {},
        "Control": {},
        "Network": {},
        "Browser": {},
        "Apps": {},
        "Custom": {}
    }

def save_commands(commands):
    """Save commands to file"""
    with open("commands.json", 'w') as f:
        json.dump(commands, f, indent=2)

def show_menu():
    """Show main menu"""
    print("\n" + "="*50)
    print("CommandCube Customizer")
    print("="*50)
    print("\n1. View all commands")
    print("2. Add new command")
    print("3. Edit command")
    print("4. Delete command")
    print("5. Add custom category")
    print("6. Exit")
    print("\nChoice: ", end="")

def view_commands(commands):
    """View all commands"""
    print("\n" + "="*50)
    print("All Commands:")
    print("="*50)
    for category, cmds in commands.items():
        print(f"\n[{category}]")
        for cmd_name, cmd_code in cmds.items():
            print(f"  • {cmd_name}")
            print(f"    → {cmd_code[:50]}...")

def add_command(commands):
    """Add new command"""
    print("\n" + "="*50)
    print("Add New Command")
    print("="*50)
    
    print("\nCategories:")
    categories = list(commands.keys())
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    cat_choice = input("\nSelect category (number): ").strip()
    try:
        category = categories[int(cat_choice) - 1]
    except:
        print("Invalid choice")
        return
    
    cmd_name = input("Command name: ").strip()
    if not cmd_name:
        print("Invalid name")
        return
    
    cmd_code = input("Command (Python code or description): ").strip()
    if not cmd_code:
        print("Invalid code")
        return
    
    commands[category][cmd_name] = cmd_code
    print(f"[+] Added: {cmd_name} to {category}")

def edit_command(commands):
    """Edit existing command"""
    print("\n" + "="*50)
    print("Edit Command")
    print("="*50)
    
    category = input("Category: ").strip()
    if category not in commands:
        print("Category not found")
        return
    
    cmd_name = input("Command name: ").strip()
    if cmd_name not in commands[category]:
        print("Command not found")
        return
    
    print(f"Current: {commands[category][cmd_name]}")
    new_code = input("New code: ").strip()
    
    if new_code:
        commands[category][cmd_name] = new_code
        print(f"[+] Updated: {cmd_name}")

def delete_command(commands):
    """Delete command"""
    print("\n" + "="*50)
    print("Delete Command")
    print("="*50)
    
    category = input("Category: ").strip()
    if category not in commands:
        print("Category not found")
        return
    
    cmd_name = input("Command name: ").strip()
    if cmd_name not in commands[category]:
        print("Command not found")
        return
    
    del commands[category][cmd_name]
    print(f"[+] Deleted: {cmd_name}")

def add_category(commands):
    """Add custom category"""
    print("\n" + "="*50)
    print("Add Custom Category")
    print("="*50)
    
    cat_name = input("Category name: ").strip()
    if not cat_name:
        print("Invalid name")
        return
    
    if cat_name in commands:
        print("Category already exists")
        return
    
    commands[cat_name] = {}
    print(f"[+] Added category: {cat_name}")

def main():
    """Main loop"""
    commands = load_commands()
    
    while True:
        show_menu()
        choice = input().strip()
        
        if choice == "1":
            view_commands(commands)
        elif choice == "2":
            add_command(commands)
            save_commands(commands)
        elif choice == "3":
            edit_command(commands)
            save_commands(commands)
        elif choice == "4":
            delete_command(commands)
            save_commands(commands)
        elif choice == "5":
            add_category(commands)
            save_commands(commands)
        elif choice == "6":
            print("Saved and exiting")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
