from __future__ import annotations

# Path is used to build a reliable file path to the CSV dataset.
from pathlib import Path

'''
These typing tools make the code easier to read and understand:
- Any: for values or classes whose exact type is flexible here
- Dict: for dictionary type hints
- List: for lists of records and table rows
- Tuple: for functions returning more than one value
'''
from typing import Any, Dict, List, Tuple

'''
Import the benchmark result object, time formatter, memory formatter,
and the benchmark helpers.
'''
from benchmark import (
    BenchmarkResult,
    format_memory_size,
    format_seconds,
    run_all_structures_summary,
    run_selected_benchmark,
)

# Import each data structure implementation used in the menu.
from dynamic_array_records import DynamicArrayRecords
from hash_map_records import HashMapRecords
from linked_list_records import LinkedListRecords
from queue_records import QueueRecords

# Import the CSV loader that converts dataset rows into PatientRecord objects.
from loader import load_patient_records

# Import the shared patient record model.
from model import PatientRecord

'''
This alias makes the structure menu mapping easier to read.
The dictionary key is the display name shown to the user,
and the value is the class that implements that structure.
'''
StructureMap = Dict[str, Any]


def print_header() -> None:
    # Prints the title shown when the program starts.
    print("\n" + "=" * 320)
    print("PATIENT RECORD DATA STRUCTURE BENCHMARK SYSTEM")
    print("=" * 320)


def print_menu() -> None:
    # Prints the main program menu.
    print("\nMain Menu")
    print("1. Run single benchmark")
    print("2. Run all data structures summary")
    print("3. Exit")


def get_user_choice(prompt: str, minimum: int, maximum: int) -> int:
    # Keep asking until the user enters a valid number in range.
    while True:
        raw_value = input(prompt).strip()

        try:
            choice = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if minimum <= choice <= maximum:
            return choice

        print(f"Please enter a number between {minimum} and {maximum}.")


def choose_structure(structures: StructureMap) -> Tuple[str, Any]:
    # Turn the dictionary keys into a list so the user can choose by number.
    structure_names = list(structures.keys())

    print("\nSelect a data structure:")
    for index, name in enumerate(structure_names, start=1):
        print(f"{index}. {name}")

    choice = get_user_choice("Enter your choice: ", 1, len(structure_names))
    selected_name = structure_names[choice - 1]
    return selected_name, structures[selected_name]


def choose_operation() -> str:
    # These are the supported benchmark operations required by the project.
    operations = ["insert", "delete", "traverse", "search"]

    print("\nSelect an operation:")
    for index, name in enumerate(operations, start=1):
        print(f"{index}. {name.capitalize()}")

    choice = get_user_choice("Enter your choice: ", 1, len(operations))
    return operations[choice - 1]


def choose_record_count(max_records: int) -> int:
    # Let the user decide how much of the dataset to benchmark.
    print(f"\nDataset size available: 1 to {max_records} records")

    while True:
        raw_value = input("How many records should be used? ").strip()

        try:
            count = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if 1 <= count <= max_records:
            return count

        print(f"Please enter a value between 1 and {max_records}.")


def print_sample_records(records: List[PatientRecord], count: int = 3) -> None:
    # Show a few example records after loading.
    print("\nSample Patient Records:")
    for record in records[:count]:
        print(record)


def print_benchmark_result(result: BenchmarkResult) -> None:
    # Format one benchmark result clearly for the console.
    print("\nBenchmark Result")
    print("-" * 96)
    print(f"Data Structure        : {result.structure_name}")
    print(f"Operation             : {result.operation_name.capitalize()}")
    print(f"Records Used          : {result.record_count}")
    print(f"Measured Average Time : {format_seconds(result.average_seconds)}")
    print(f"Average Peak Memory   : {format_memory_size(result.average_peak_memory_bytes)}")
    print(f"Theoretical Big-O     : {result.time_complexity}")
    print(f"Runs Averaged         : {result.runs}")
    print("-" * 96)


def format_summary_time(result: BenchmarkResult) -> str:
    # Keep measured time formatting in one helper so the summary table stays consistent.
    return format_seconds(result.average_seconds)


def format_summary_memory(result: BenchmarkResult) -> str:
    # Keep memory formatting in one helper so the summary table stays consistent.
    return format_memory_size(result.average_peak_memory_bytes)


def print_all_structures_summary(summary: Dict[str, Dict[str, BenchmarkResult]]) -> None:
    # This function prints the comparison table for all data structures.
    headers = [
        "Data Structure",
        "Insert Time",
        "Insert Memory",
        "Insert Big-O",
        "Search Time",
        "Search Memory",
        "Search Big-O",
        "Delete Time",
        "Delete Memory",
        "Delete Big-O",
        "Traverse Time",
        "Traverse Memory",
        "Traverse Big-O",
    ]

    rows: List[List[str]] = []

    for structure_name, results in summary.items():
        display_name = structure_name
        if structure_name == "Queue":
            display_name = "Queue / Admission Queue"

        rows.append(
            [
                display_name,
                format_summary_time(results["insert"]),
                format_summary_memory(results["insert"]),
                results["insert"].time_complexity,
                format_summary_time(results["search"]),
                format_summary_memory(results["search"]),
                results["search"].time_complexity,
                format_summary_time(results["delete"]),
                format_summary_memory(results["delete"]),
                results["delete"].time_complexity,
                format_summary_time(results["traverse"]),
                format_summary_memory(results["traverse"]),
                results["traverse"].time_complexity,
            ]
        )

    widths = [26, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]

    print("\nAll Data Structures Summary")
    print("=" * sum(widths))
    print("Measured time, measured memory, and theoretical Big-O are shown separately.")
    print(
        f"{headers[0]:<{widths[0]}}"
        f"{headers[1]:<{widths[1]}}"
        f"{headers[2]:<{widths[2]}}"
        f"{headers[3]:<{widths[3]}}"
        f"{headers[4]:<{widths[4]}}"
        f"{headers[5]:<{widths[5]}}"
        f"{headers[6]:<{widths[6]}}"
        f"{headers[7]:<{widths[7]}}"
        f"{headers[8]:<{widths[8]}}"
        f"{headers[9]:<{widths[9]}}"
        f"{headers[10]:<{widths[10]}}"
        f"{headers[11]:<{widths[11]}}"
        f"{headers[12]:<{widths[12]}}"
    )
    print("-" * sum(widths))

    for row in rows:
        print(
            f"{row[0]:<{widths[0]}}"
            f"{row[1]:<{widths[1]}}"
            f"{row[2]:<{widths[2]}}"
            f"{row[3]:<{widths[3]}}"
            f"{row[4]:<{widths[4]}}"
            f"{row[5]:<{widths[5]}}"
            f"{row[6]:<{widths[6]}}"
            f"{row[7]:<{widths[7]}}"
            f"{row[8]:<{widths[8]}}"
            f"{row[9]:<{widths[9]}}"
            f"{row[10]:<{widths[10]}}"
            f"{row[11]:<{widths[11]}}"
            f"{row[12]:<{widths[12]}}"
        )

    print("=" * sum(widths))
    print(
        "Note: Big-O is theoretical growth, not a conversion of measured time or measured memory. "
        "Results shown are averages across 5 runs."
    )


def ask_run_again() -> bool:
    # After each benchmark flow finishes, ask whether the user wants another test.
    while True:
        again = input("\nWould you like to run another benchmark? (y/n): ").strip().lower()

        if again in {"y", "n"}:
            return again == "y"

        print("Please enter 'y' or 'n'.")


def main() -> None:
    # Build the path to the dataset relative to this file's folder.
    base_dir = Path(__file__).resolve().parent
    csv_file_path = base_dir / "healthcare_dataset.csv"

    try:
        # Load the full dataset into memory once at startup.
        all_records = load_patient_records(csv_file_path, limit=None)
    except FileNotFoundError as error:
        print(error)
        return

    if not all_records:
        print("No patient records were loaded.")
        return

    structures: StructureMap = {
        "Dynamic Array": DynamicArrayRecords,
        "Linked List": LinkedListRecords,
        "Queue": QueueRecords,
        "Hash Map": HashMapRecords,
    }

    print_header()
    print(f"Loaded {len(all_records)} patient records from the dataset.")
    print_sample_records(all_records)

    while True:
        print_menu()
        main_choice = get_user_choice("Enter your choice: ", 1, 3)

        if main_choice == 3:
            print("\nExiting program. Goodbye.")
            break

        record_count = choose_record_count(len(all_records))
        selected_records = all_records[:record_count]

        if main_choice == 1:
            structure_name, structure_class = choose_structure(structures)
            operation_name = choose_operation()

            try:
                result = run_selected_benchmark(
                    structure_name=structure_name,
                    structure_class=structure_class,
                    operation_name=operation_name,
                    records=selected_records,
                    runs=5,
                )
            except ValueError as error:
                print(f"Benchmark failed: {error}")
                continue

            print_benchmark_result(result)

        elif main_choice == 2:
            try:
                summary = run_all_structures_summary(
                    structures=structures,
                    records=selected_records,
                    runs=5,
                )
            except ValueError as error:
                print(f"Benchmark failed: {error}")
                continue

            print_all_structures_summary(summary)

        if not ask_run_again():
            print("\nExiting program. Goodbye.")
            break


if __name__ == "__main__":
    main()
