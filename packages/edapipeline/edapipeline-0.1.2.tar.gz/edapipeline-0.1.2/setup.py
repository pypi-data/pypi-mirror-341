# setup.py
# IMPORTANT: Save this file with UTF-8 Encoding!

from setuptools import setup
import sys
import os
import time
import math

# --- Message Configuration ---

# ANSI Color Codes for terminal output
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[1;31m"       # Bold Red
COLOR_GREEN = "\033[1;32m"     # Bold Green
COLOR_WHITE_BOLD = "\033[1;37m" # Bold White

# Background colors for flag representation
BG_BLACK = "\033[40m"  # Black background
BG_WHITE = "\033[47m"  # White background
BG_GREEN = "\033[42m"  # Green background
BG_RED = "\033[41m"    # Red background

# Humanitarian statistics (as of October 2024)
STATS = [
    "Over 40,000 Palestinians have been killed since October 2023",
    "More than 92,000 Palestinians have been injured",
    "Around 18,000 children have lost their lives in Gaza",
    "1.9 million people (85% of Gaza's population) have been displaced",
    "70% of homes in Gaza have been destroyed or damaged",
    "Over 150 hospitals and medical facilities have been damaged or destroyed",
    "80% of Gaza's schools have been damaged or destroyed",
    "95% of Gaza's population faces severe food insecurity",
    "Limited access to clean water has led to widespread disease"
]

def create_correct_palestine_flag():
    """Creates an accurate representation of the Palestine flag with a triangular red section."""
    flag_width = 60
    flag_height = 18  # Multiple of 3 for even stripes
    
    # Size of the triangle base (left edge of flag)
    triangle_base = flag_height
    
    # Maximum triangle width (how far it extends to the right)
    triangle_width = flag_width // 3
    
    # Create the flag
    flag = []
    
    # For each row in the flag
    for y in range(flag_height):
        line = ""
        # Calculate which horizontal band we're in
        stripe_height = flag_height // 3
        
        if y < stripe_height:
            bg_color = BG_BLACK
        elif y < 2 * stripe_height:
            bg_color = BG_WHITE
        else:
            bg_color = BG_GREEN
            
        # Calculate triangle width at this row
        # For a proper triangle, width decreases linearly with distance from the center
        center_y = flag_height / 2
        distance_from_center = abs(y - center_y)
        # The width is maximum at center, and decreases to minimum at top/bottom
        width_fraction = 1 - (distance_from_center / (flag_height / 2))
        triangle_width_at_row = max(1, int(triangle_width * width_fraction))
        
        # Create the row: red triangle followed by color band
        line += f"{BG_RED}{' ' * triangle_width_at_row}{COLOR_RESET}"
        line += f"{bg_color}{' ' * (flag_width - triangle_width_at_row)}{COLOR_RESET}"
        
        flag.append(line)
        
    return flag

def display_message():
    """Displays the Palestine flag and awareness message."""
    # Clear terminal (works on most terminals)
    print("\033c", end="")
    
    # Display header
    print(f"\n{COLOR_WHITE_BOLD}{'=' * 60}{COLOR_RESET}")
    print(f"{COLOR_WHITE_BOLD}          Thank you for installing EDAPipeline!{COLOR_RESET}")
    print(f"{COLOR_WHITE_BOLD}{'=' * 60}{COLOR_RESET}\n")
    
    # Display the Palestine flag
    print(f"{COLOR_WHITE_BOLD}Palestine Flag:{COLOR_RESET}")
    flag = create_correct_palestine_flag()
    for line in flag:
        print(line)
    
    # Display solidarity message
    print(f"\n{COLOR_GREEN}We stand in solidarity with the people of Palestine.{COLOR_RESET}")
    print(f"{COLOR_RED}#StopGenocideInGaza #FreedomPalestine 🇵🇸{COLOR_RESET}\n")
    
    # Display humanitarian statistics
    print(f"{COLOR_WHITE_BOLD}Humanitarian Crisis - Key Statistics:{COLOR_RESET}")
    for stat in STATS:
        print(f"{COLOR_RED}• {stat}{COLOR_RESET}")
    
    # Display footer
    print(f"\n{COLOR_WHITE_BOLD}{'=' * 60}{COLOR_RESET}")
    print(f"{COLOR_WHITE_BOLD}     Support Humanity | Support Palestine | Seek Peace{COLOR_RESET}")
    print(f"{COLOR_WHITE_BOLD}{'=' * 60}{COLOR_RESET}\n")

# Alternative ASCII version if colors don't work well
def create_ascii_palestine_flag():
    """Creates an ASCII art version of the Palestine flag with correct triangle."""
    flag_width = 60
    flag_height = 15
    triangle_width = flag_width // 3
    
    flag = []
    
    for y in range(flag_height):
        line = ""
        stripe_height = flag_height // 3
        
        # Determine which stripe pattern to use
        if y < stripe_height:
            stripe_char = "▓"  # Black stripe
        elif y < 2 * stripe_height:
            stripe_char = "░"  # White stripe
        else:
            stripe_char = "▒"  # Green stripe
            
        # Calculate triangle width at this row
        center_y = flag_height / 2
        distance_from_center = abs(y - center_y)
        width_fraction = 1 - (distance_from_center / (flag_height / 2))
        triangle_width_at_row = max(1, int(triangle_width * width_fraction))
        
        # Create the row: red triangle followed by color band
        line += COLOR_RED + "█" * triangle_width_at_row + COLOR_RESET
        
        if y < stripe_height:
            line += COLOR_BLACK + stripe_char * (flag_width - triangle_width_at_row) + COLOR_RESET
        elif y < 2 * stripe_height:
            line += COLOR_WHITE + stripe_char * (flag_width - triangle_width_at_row) + COLOR_RESET
        else:
            line += COLOR_GREEN + stripe_char * (flag_width - triangle_width_at_row) + COLOR_RESET
        
        flag.append(line)
        
    return flag

# Try both display methods
def try_display_flag():
    """Try displaying the flag with different methods, falling back if needed."""
    try:
        # First try color blocks version
        display_message()
    except Exception:
        try:
            # Then try ASCII art version
            print(f"{COLOR_WHITE_BOLD}Palestine Flag:{COLOR_RESET}")
            flag = create_ascii_palestine_flag()
            for line in flag:
                print(line)
            
            # Display solidarity message
            print(f"\n{COLOR_GREEN}We stand in solidarity with the people of Palestine.{COLOR_RESET}")
            print(f"{COLOR_RED}#StopGenocideInGaza #FreedomPalestine 🇵🇸{COLOR_RESET}\n")
            
            # Display humanitarian statistics
            print(f"{COLOR_WHITE_BOLD}Humanitarian Crisis - Key Statistics:{COLOR_RESET}")
            for stat in STATS:
                print(f"{COLOR_RED}• {stat}{COLOR_RESET}")
            
            # Display footer
            print(f"\n{COLOR_WHITE_BOLD}{'=' * 60}{COLOR_RESET}")
            print(f"{COLOR_WHITE_BOLD}     Support Humanity | Support Palestine | Seek Peace{COLOR_RESET}")
            print(f"{COLOR_WHITE_BOLD}{'=' * 60}{COLOR_RESET}\n")
        except Exception as e:
            # Ultimate fallback - just text
            print("\nThank you for installing EDAPipeline!")
            print("\nWe stand in solidarity with the people of Palestine.")
            print("#StopGenocideInGaza #FreedomPalestine 🇵🇸")
            print("\nHumanitarian Crisis - Key Statistics:")
            for stat in STATS:
                print(f"• {stat}")
            print("\nSupport Humanity | Support Palestine | Seek Peace\n")

# --- Print Logic ---

# Check if running in a CI environment
is_ci = any(os.environ.get(var) for var in ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'JENKINS_URL'])

# Only display if NOT in a CI environment and output is likely a terminal
if not is_ci and sys.stdout.isatty():
    try_display_flag()

# --- Setup Call ---
# This line is crucial. It tells setuptools to proceed using setup.cfg for config.
setup()