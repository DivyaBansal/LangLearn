#!/usr/bin/env python3
"""
Interactive script to edit question or answer entries in TSV files.
Supports: sentences.tsv, separable-verbs.tsv, inseparable-verbs.tsv
"""

import os
import sys
import csv
from pathlib import Path


def get_script_dir():
    """Get the directory where the script is located."""
    return Path(__file__).parent.resolve()


def get_data_dir():
    """Get the data directory from environment or script directory."""
    data_dir = os.environ.get('GERMAN_PRACTICE_DATA_DIR')
    if data_dir:
        return Path(data_dir).resolve()
    return get_script_dir() / 'data'


def detect_tsv_format(filepath):
    """Detect the format of a TSV file based on its content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        fields = first_line.split('\t')
        num_fields = len(fields)

        if num_fields == 3:
            # sentences.tsv format: ID, English, German
            return 'sentences'
        elif num_fields == 4:
            # separable-verbs.tsv format: ID, German, English, Example
            return 'separable_verbs'
        elif num_fields == 5:
            # inseparable-verbs.tsv format: ID, ID, German, English, Example
            return 'inseparable_verbs'
        else:
            raise ValueError(f"Unknown TSV format: {num_fields} fields")


def load_entries(filepath):
    """Load all entries from a TSV file."""
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row and not row[0].startswith('#'):
                entries.append(row)
    return entries


def save_entries(filepath, entries):
    """Save all entries to a TSV file."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(entries)


def display_entry(entry, format_type, index=None):
    """Display an entry in a user-friendly format."""
    print("\n" + "=" * 50)
    if index is not None:
        print(f"Entry #{index + 1}")
    print("=" * 50)

    if format_type == 'sentences':
        print(f"ID: {entry[0]}")
        print(f"English (Question): {entry[1]}")
        print(f"German (Answer): {entry[2]}")
    elif format_type == 'separable_verbs':
        print(f"ID: {entry[0]}")
        print(f"German Verb: {entry[1]}")
        print(f"English Meaning: {entry[2]}")
        print(f"Example: {entry[3]}")
    elif format_type == 'inseparable_verbs':
        print(f"ID: {entry[1]}")
        print(f"German Verb: {entry[2]}")
        print(f"English Meaning: {entry[3]}")
        print(f"Example: {entry[4]}")
    print("=" * 50)


def edit_field(entry, format_type, field_index, field_name):
    """Edit a specific field in an entry."""
    print(f"\nEditing {field_name}:")
    print(f"Current value: {entry[field_index]}")
    print("Enter new value (press Enter twice to keep unchanged):")

    new_value = input("> ").strip()
    if new_value == "":
        print("Keeping original value.")
        return entry

    entry[field_index] = new_value
    print(f"Updated {field_name} to: {new_value}")
    return entry


def edit_entry_by_id(entries, filepath, format_type):
    """Find and edit an entry by its ID."""
    print("\nFind entry by ID:")
    target_id = input("Enter the ID number: ").strip()

    found_index = None
    for i, entry in enumerate(entries):
        # Check appropriate ID field based on format
        if format_type == 'inseparable_verbs':
            if entry[1] == target_id:
                found_index = i
                break
        else:
            if entry[0] == target_id:
                found_index = i
                break

    if found_index is None:
        print(f"Error: No entry found with ID '{target_id}'")
        return False

    entry = entries[found_index]
    display_entry(entry, format_type, found_index)

    print("\nFields to edit:")
    if format_type == 'sentences':
        print("  1. English (question)")
        print("  2. German (answer)")
    elif format_type == 'separable_verbs':
        print("  1. German verb")
        print("  2. English meaning")
        print("  3. Example sentence")
    elif format_type == 'inseparable_verbs':
        print("  1. German verb")
        print("  2. English meaning")
        print("  3. Example sentence")

    while True:
        choice = input("\nWhich field to edit? (1-3, or 'q' to quit): ").strip()

        if choice.lower() == 'q':
            return False

        field_map = {
            'sentences': {
                '1': (1, 'English (question)'),
                '2': (2, 'German (answer)'),
            },
            'separable_verbs': {
                '1': (1, 'German verb'),
                '2': (2, 'English meaning'),
                '3': (3, 'Example sentence'),
            },
            'inseparable_verbs': {
                '1': (2, 'German verb'),
                '2': (3, 'English meaning'),
                '3': (4, 'Example sentence'),
            },
        }

        if choice in field_map.get(format_type, {}):
            field_idx, field_name = field_map[format_type][choice]
            entries[found_index] = edit_field(entry, format_type, field_idx, field_name)
            display_entry(entries[found_index], format_type, found_index)
        else:
            print("Invalid choice. Please try again.")

        cont = input("\nEdit another field in this entry? (y/n): ").strip().lower()
        if cont != 'y':
            break

    return True


def edit_entry_by_number(entries, filepath, format_type):
    """Find and edit an entry by its line number."""
    print(f"\nTotal entries in file: {len(entries)}")
    target_num = input("Enter the entry number (1-{}): ".format(len(entries))).strip()

    try:
        target_num = int(target_num)
        if target_num < 1 or target_num > len(entries):
            print(f"Error: Entry number must be between 1 and {len(entries)}")
            return False
    except ValueError:
        print("Error: Please enter a valid number")
        return False

    index = target_num - 1
    entry = entries[index]
    display_entry(entry, format_type, index)

    print("\nFields to edit:")
    if format_type == 'sentences':
        print("  1. English (question)")
        print("  2. German (answer)")
    elif format_type == 'separable_verbs':
        print("  1. German verb")
        print("  2. English meaning")
        print("  3. Example sentence")
    elif format_type == 'inseparable_verbs':
        print("  1. German verb")
        print("  2. English meaning")
        print("  3. Example sentence")

    while True:
        choice = input("\nWhich field to edit? (1-3, or 'q' to quit): ").strip()

        if choice.lower() == 'q':
            return False

        field_map = {
            'sentences': {
                '1': (1, 'English (question)'),
                '2': (2, 'German (answer)'),
            },
            'separable_verbs': {
                '1': (1, 'German verb'),
                '2': (2, 'English meaning'),
                '3': (3, 'Example sentence'),
            },
            'inseparable_verbs': {
                '1': (2, 'German verb'),
                '2': (3, 'English meaning'),
                '3': (4, 'Example sentence'),
            },
        }

        if choice in field_map.get(format_type, {}):
            field_idx, field_name = field_map[format_type][choice]
            entries[index] = edit_field(entry, format_type, field_idx, field_name)
            display_entry(entries[index], format_type, index)
        else:
            print("Invalid choice. Please try again.")

        cont = input("\nEdit another field in this entry? (y/n): ").strip().lower()
        if cont != 'y':
            break

    return True


def browse_and_edit(entries, filepath, format_type):
    """Browse entries and edit any found entry."""
    search = input("\nSearch term (to find entries containing this text): ").strip()

    matching_indices = []
    for i, entry in enumerate(entries):
        if search.lower() in ' '.join(entry).lower():
            matching_indices.append(i)

    if not matching_indices:
        print(f"No entries containing '{search}' found.")
        return False

    print(f"\nFound {len(matching_indices)} matching entries:")
    for i, idx in enumerate(matching_indices[:10]):  # Show first 10 matches
        if format_type == 'sentences':
            preview = entry_preview(entries[idx])
        elif format_type in ('separable_verbs', 'inseparable_verbs'):
            preview = verb_preview(entries[idx])
        print(f"  {i + 1}. Entry #{idx + 1}: {preview}")

    if len(matching_indices) > 10:
        print(f"  ... and {len(matching_indices) - 10} more entries")

    choice = input(f"\nWhich entry to edit? (1-{min(len(matching_indices), 10)}): ").strip()

    try:
        choice = int(choice)
        if choice < 1 or choice > len(matching_indices):
            print("Invalid choice.")
            return False
    except ValueError:
        print("Error: Please enter a valid number")
        return False

    index = matching_indices[choice - 1]
    entry = entries[index]
    display_entry(entry, format_type, index)

    print("\nFields to edit:")
    if format_type == 'sentences':
        print("  1. English (question)")
        print("  2. German (answer)")
    elif format_type == 'separable_verbs':
        print("  1. German verb")
        print("  2. English meaning")
        print("  3. Example sentence")
    elif format_type == 'inseparable_verbs':
        print("  1. German verb")
        print("  2. English meaning")
        print("  3. Example sentence")

    while True:
        choice = input("\nWhich field to edit? (1-3, or 'q' to quit): ").strip()

        if choice.lower() == 'q':
            return False

        field_map = {
            'sentences': {
                '1': (1, 'English (question)'),
                '2': (2, 'German (answer)'),
            },
            'separable_verbs': {
                '1': (1, 'German verb'),
                '2': (2, 'English meaning'),
                '3': (3, 'Example sentence'),
            },
            'inseparable_verbs': {
                '1': (2, 'German verb'),
                '2': (3, 'English meaning'),
                '3': (4, 'Example sentence'),
            },
        }

        if choice in field_map.get(format_type, {}):
            field_idx, field_name = field_map[format_type][choice]
            entries[index] = edit_field(entry, format_type, field_idx, field_name)
            display_entry(entries[index], format_type, index)
        else:
            print("Invalid choice. Please try again.")

        cont = input("\nEdit another field in this entry? (y/n): ").strip().lower()
        if cont != 'y':
            break

    return True


def entry_preview(entry):
    """Create a short preview of a sentence entry."""
    english = entry[1][:40] + "..." if len(entry[1]) > 40 else entry[1]
    return f"'{english}'"


def verb_preview(entry):
    """Create a short preview of a verb entry."""
    german = entry[1] if entry[1] else entry[2]
    english = entry[2] if entry[1] else entry[3]
    return f"'{german}' = '{english}'"


def confirm_save():
    """Ask user to confirm saving changes."""
    while True:
        choice = input("\nSave changes? (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print("Changes discarded.")
            return False
        else:
            print("Please enter 'y' or 'n'.")


def print_banner():
    """Print the main banner."""
    print("\n" + "=" * 50)
    print("       TSV Entry Editor")
    print("=" * 50)


def main():
    print_banner()

    data_dir = get_data_dir()
    print(f"Data directory: {data_dir}")

    # List available TSV files
    tsv_files = {
        '1': ('sentences.tsv', 'Sentences (English-German)'),
        '2': ('separable-verbs.tsv', 'Separable Verbs'),
        '3': ('inseparable-verbs.tsv', 'Inseparable Verbs'),
    }

    print("\nAvailable files:")
    for key, (filename, description) in tsv_files.items():
        filepath = data_dir / filename
        exists = "✓" if filepath.exists() else "✗"
        print(f"  {key}. [{exists}] {filename} - {description}")

    file_choice = input("\nSelect file to edit (1-3): ").strip()

    if file_choice not in tsv_files:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    filename, _ = tsv_files[file_choice]
    filepath = data_dir / filename

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    try:
        format_type = detect_tsv_format(filepath)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\nLoaded {filepath}")
    entries = load_entries(filepath)
    print(f"Total entries: {len(entries)}")

    # Edit menu
    while True:
        print("\n" + "-" * 50)
        print("Edit Options:")
        print("  1. Find and edit by ID")
        print("  2. Find and edit by entry number")
        print("  3. Search and browse to edit")
        print("  4. Exit editor")
        print("-" * 50)

        choice = input("\nSelect option (1-4): ").strip()

        if choice == '4':
            break

        edited = False
        if choice == '1':
            edited = edit_entry_by_id(entries, filepath, format_type)
        elif choice == '2':
            edited = edit_entry_by_number(entries, filepath, format_type)
        elif choice == '3':
            edited = browse_and_edit(entries, filepath, format_type)
        else:
            print("Invalid choice. Please try again.")
            continue

        if edited:
            if confirm_save():
                save_entries(filepath, entries)
                print(f"Changes saved to: {filepath}")
            else:
                print("Changes were not saved.")

    print("\nGoodbye!")


if __name__ == '__main__':
    main()
