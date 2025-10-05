#!/usr/bin/env python3
"""
JSON Combinator Script
Combines the base 2025 JSON with all department drill-down JSONs
"""

import json
import os
from pathlib import Path

def load_json(file_path):
    """Load JSON from file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    """Save JSON to file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def combine_json_files():
    """Combine base 2025 JSON with all department JSONs"""
    
    # Load the base 2025 JSON
    base_path = "data/base/base_2025.json"
    base_data = load_json(base_path)
    
    # Get all department JSON files
    dept_dir = Path("data/departments")
    dept_files = sorted(dept_dir.glob("*.json"))
    
    print(f"Found {len(dept_files)} department files:")
    for file in dept_files:
        print(f"  - {file.name}")
    
    # Create a mapping of department names to their detailed data
    dept_data_map = {}
    for dept_file in dept_files:
        dept_data = load_json(dept_file)
        dept_name = dept_data["name"]
        dept_data_map[dept_name] = dept_data
        print(f"Loaded: {dept_name}")
    
    # Update the base data with department details
    updated_children = []
    
    for child in base_data["children"]:
        dept_name = child["name"]
        if dept_name in dept_data_map:
            # Replace the empty children with the detailed breakdown
            child["children"] = dept_data_map[dept_name]["children"]
            print(f"Updated: {dept_name}")
        else:
            print(f"Warning: No detailed data found for {dept_name}")
        updated_children.append(child)
    
    base_data["children"] = updated_children
    
    # Save the combined data
    output_path = "data/combined/combined_2025_visualization.json"
    save_json(base_data, output_path)
    
    print(f"\nCombined JSON saved to: {output_path}")
    print(f"Total departments: {len(base_data['children'])}")
    
    # Verify the structure
    for child in base_data["children"]:
        dept_name = child["name"]
        children_count = len(child["children"]) if child["children"] else 0
        print(f"  - {dept_name}: {children_count} child datasets")

if __name__ == "__main__":
    combine_json_files()
