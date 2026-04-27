from __future__ import annotations
from pathlib import Path
from benchmark import (
    benchmark_delete,
    benchmark_insert,
    benchmark_search,
    benchmark_traverse,
    format_seconds,
)
# Uncomment your section once code is typed.
#from dynamic_array_records import DynamicArrayRecords
from hash_map_records import HashMapRecords
#from linked_list_records import LinkedListRecords
from loader import load_patient_records
#from queue_records import QueueRecords


# Print a small sample of loaded records so the user can verify
# that the dataset was loaded correctly.
def print_sample_records(records: list, count: int = 3) -> None:
    print("\nSample Patient Records:")
    for record in records[:count]:
        print(record)


# Main driver function for the project.
#
# Purpose:
# - Locate the dataset file
# - Load 100 patient records from the CSV
# - Display a small sample of those records
# - Run benchmark tests on the selected data structures
# - Print benchmark results in a formatted table
def main() -> None:
    # Get the folder where main.py is located.
    # This ensures the CSV file is searched for in the same folder as the script,
    # instead of the terminal's current working directory.
    base_dir = Path(__file__).resolve().parent

    # Build the full path to the dataset file.
    # This fixes the FileNotFoundError issue from using only "healthcare_dataset.csv".
    csv_file_path = base_dir / "healthcare_dataset.csv"

    # Load exactly 100 records from the dataset, as required by the project setup.
    patient_records = load_patient_records(csv_file_path, limit=100)

    # If no records were loaded, stop the program early.
    if not patient_records:
        print("No patient records were loaded.")
        return

    # Confirm how many records were loaded and show sample records.
    print(f"Loaded {len(patient_records)} patient records.")
    print_sample_records(patient_records)

    # Dictionary of data structures to test.
    # Only Hash Map is currently active.
    # The other structures remain commented out to match your current file. Uncomment once you type your code to test. 
    structure_map = {
#        "Dynamic Array": DynamicArrayRecords,
#       "Linked List": LinkedListRecords,
        "Hash Map": HashMapRecords,
#        "Queue": QueueRecords,
    }

    # Choose one record roughly from the middle of the dataset for the search test.
    search_id = patient_records[len(patient_records) // 2].id

    # Choose the last record for the delete test.
    delete_id = patient_records[-1].id

    # Print table headers for the benchmark results.
    print("\nBenchmark Results (average of 5 runs):")
    print("-" * 90)
    print(
        f"{'Data Structure':<20}"
        f"{'Insert':<18}"
        f"{'Search':<18}"
        f"{'Delete':<18}"
        f"{'Traverse':<18}"
    )
    print("-" * 90)

    # Run all benchmark operations for each active data structure.
    for structure_name, structure_class in structure_map.items():
        insert_time = benchmark_insert(structure_class, patient_records)
        search_time = benchmark_search(structure_class, patient_records, search_id)
        delete_time = benchmark_delete(structure_class, patient_records, delete_id)
        traverse_time = benchmark_traverse(structure_class, patient_records)

        # Print the average runtime for each operation.
        print(
            f"{structure_name:<20}"
            f"{format_seconds(insert_time):<18}"
            f"{format_seconds(search_time):<18}"
            f"{format_seconds(delete_time):<18}"
            f"{format_seconds(traverse_time):<18}"
        )

# Standard Python entry point.
# This makes sure main() runs only when this file is executed directly.
if __name__ == "__main__":
    main()
