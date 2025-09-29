#!/usr/bin/env python3
"""
Mymory Bubble Scanner
Automatically scans the /bubbles/ folder and generates bubbles.json for GitHub Pages
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def scan_bubbles_folder(bubbles_path="bubbles"):
    """
    Scan the bubbles folder and extract all bubble data
    """
    bubbles = []
    
    if not os.path.exists(bubbles_path):
        print(f"ERROR: Bubbles folder '{bubbles_path}' not found!")
        return bubbles
    
    # Get all folders in bubbles directory
    folders = [f for f in os.listdir(bubbles_path) 
               if os.path.isdir(os.path.join(bubbles_path, f))]
    
    # Sort folders by date (chronological order)
    folders.sort()
    
    print(f"Found {len(folders)} bubble folders:")
    
    for folder_name in folders:
        folder_path = os.path.join(bubbles_path, folder_name)
        config_path = os.path.join(folder_path, "config.json")
        
        # Validate folder name format (YYYY-MM-DDTHH-MM-SS)
        if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$', folder_name):
            print(f"WARNING: Skipping '{folder_name}' - invalid format")
            continue
        
        # Check if config.json exists
        if not os.path.exists(config_path):
            print(f"WARNING: Skipping '{folder_name}' - no config.json found")
            continue
        
        try:
            # Load config.json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate required fields
            required_fields = ['title', 'description', 'has_photo']
            if not all(field in config for field in required_fields):
                print(f"WARNING: Skipping '{folder_name}' - missing required fields")
                continue
            
            # Parse date from folder name
            date_str = folder_name.replace('T', ' ').replace('-', '/')
            try:
                parsed_date = datetime.strptime(date_str, '%Y/%m/%d %H/%M/%S')
            except ValueError:
                print(f"WARNING: Skipping '{folder_name}' - invalid date format")
                continue
            
            # Check if photo exists
            photo_path = None
            if config.get('has_photo') == 'True':
                # If photo is specified in config, use it
                if config.get('photo'):
                    photo_file = os.path.join(folder_path, config['photo'])
                    if os.path.exists(photo_file):
                        photo_path = f"bubbles/{folder_name}/{config['photo']}"
                    else:
                        print(f"WARNING: Photo '{config['photo']}' not found in '{folder_name}'")
                        # Still set the path even if file doesn't exist (for case sensitivity issues)
                        photo_path = f"bubbles/{folder_name}/{config['photo']}"
                else:
                    # Auto-detect photo files if not specified
                    photo_extensions = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.gif', '.GIF', '.webp', '.WEBP']
                    found_photo = None
                    
                    for ext in photo_extensions:
                        # Look for common photo filenames
                        possible_names = ['photo', 'image', 'img', 'picture', 'pic']
                        for name in possible_names:
                            photo_file = os.path.join(folder_path, f"{name}{ext}")
                            if os.path.exists(photo_file):
                                found_photo = f"{name}{ext}"
                                break
                        
                        if found_photo:
                            break
                    
                    if found_photo:
                        photo_path = f"bubbles/{folder_name}/{found_photo}"
                        print(f"INFO: Auto-detected photo '{found_photo}' in '{folder_name}'")
                    else:
                        print(f"WARNING: No photo found in '{folder_name}' despite has_photo=True")
            
            # Create bubble data
            bubble_data = {
                "id": f"bubble-{len(bubbles)}",
                "title": config['title'],
                "description": config['description'],
                "location": config.get('location', ''),  # Add location field, default to empty string
                "photo": photo_path,
                "date": folder_name,
                "folderName": folder_name,
                "hasPhoto": config.get('has_photo') == 'True',
                "rawDate": parsed_date.isoformat(),
                "size": 150,  # Increased bubble size
                "x": 0,  # Will be calculated later
                "y": 50  # Center vertically
            }
            
            bubbles.append(bubble_data)
            print(f"SUCCESS: Added '{folder_name}' - {config['title']}")
            
        except json.JSONDecodeError as e:
            print(f"ERROR: Error parsing config.json in '{folder_name}': {e}")
        except Exception as e:
            print(f"ERROR: Error processing '{folder_name}': {e}")
    
    return bubbles

def calculate_positions(bubbles):
    """
    Calculate timeline positions for bubbles
    """
    if not bubbles:
        return bubbles
    
    for i, bubble in enumerate(bubbles):
        timeline_progress = i / max(1, len(bubbles) - 1)
        bubble['x'] = 10 + (timeline_progress * 80)  # 10% to 90% horizontal spread
    
    return bubbles

def generate_bubbles_json(bubbles, output_file="bubbles.json"):
    """
    Generate the bubbles.json file only
    """
    try:
        # Generate JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(bubbles, f, indent=2, ensure_ascii=False)
        
        print(f"SUCCESS: Generated {output_file} with {len(bubbles)} bubbles!")
        
        return True
    except Exception as e:
        print(f"ERROR: Error generating {output_file}: {e}")
        return False


def main():
    """
    Main function to scan bubbles and generate JSON
    """
    print("Mymory Bubble Scanner")
    print("=" * 40)
    
    # Scan bubbles folder
    bubbles = scan_bubbles_folder()
    
    if not bubbles:
        print("ERROR: No valid bubbles found!")
        return
    
    # Calculate positions
    bubbles = calculate_positions(bubbles)
    
    # Generate JSON file
    if generate_bubbles_json(bubbles):
        print("\nSUCCESS: Your bubbles.json is ready!")
        print("\nTo view your memories:")
        print("   1. Run: python start_server.py")
        print("   2. Open: http://localhost:8000/mymory.html")
        print("\nTo add new bubbles:")
        print("   1. Create folder: bubbles/YYYY-MM-DDTHH-MM-SS/")
        print("   2. Add config.json with title, description, has_photo, location (optional)")
        print("   3. Add photo file (optional)")
        print("   4. Run this script again")
    else:
        print("ERROR: Failed to generate bubbles.json")

if __name__ == "__main__":
    main()
