from __future__ import annotations

# Path is used to build a reliable file path to the CSV dataset.
from pathlib import Path

'''
These typing tools make the code easier to read and understand:
- Any: for values/classes whose exact type is flexible here
- Dict: for dictionary type hints
- List: for lists of records
- Tuple: for functions returning more than one value
'''
from typing import Any, Dict, List, Tuple

# Import the benchmark result object, time formatter, and the function
# that runs the chosen benchmark based on the user's menu selections.
from benchmark import BenchmarkResult, format_seconds, run_selected_benchmark

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
    # This is only for presentation and does not affect logic.
    print("\n" + "=" * 72)
    print("PATIENT RECORD DATA STRUCTURE BENCHMARK SYSTEM")
    print("=" * 72)


def print_menu() -> None:
    # Prints the main program menu.
    # The loop in main() will keep showing this until the user exits.
    print("\nMain Menu")
    print("1. Run benchmark")
    print("2. Exit")


def get_user_choice(prompt: str, minimum: int, maximum: int) -> int:
    # This helper keeps asking until the user enters a valid number in range.
    # It prevents duplicated try/except logic in the rest of the program.
    while True:
        raw_value = input(prompt).strip()

        try:
            choice = int(raw_value)
        except ValueError:
            # If the input is not a number, ask again.
            print("Invalid input. Please enter a number.")
            continue
        # Only accept values inside the expected range.
        if minimum <= choice <= maximum:
            return choice

        print(f"Please enter a number between {minimum} and {maximum}.")


def choose_structure(structures: StructureMap) -> Tuple[str, Any]:
    # Turn the dictionary keys into a list so the user can choose by number.
    structure_names = list(structures.keys())

    print("\nSelect a data structure:")
    for index, name in enumerate(structure_names, start=1):
        print(f"{index}. {name}")
    # The chosen number maps back to the structure name and class.
    choice = get_user_choice("Enter your choice: ", 1, len(structure_names))
    selected_name = structure_names[choice - 1]
    
    # Return both:
    # - the name for display
    # - the class for running the benchmark
    return selected_name, structures[selected_name]


def choose_operation() -> str:
    # These are the supported benchmark operations required by the project.
    operations = ["insert", "delete", "traverse", "search"]

    print("\nSelect an operation:")
    for index, name in enumerate(operations, start=1):
        print(f"{index}. {name.capitalize()}")
        
    # Return the operation string used later by the benchmark module.
    choice = get_user_choice("Enter your choice: ", 1, len(operations))
    return operations[choice - 1]


def choose_record_count(max_records: int) -> int:
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
    print("\nSample Patient Records:")
    for record in records[:count]:
        print(record)


def print_benchmark_result(result: BenchmarkResult) -> None:
    print("\nBenchmark Result")
    print("-" * 72)
    print(f"Data Structure : {result.structure_name}")
    print(f"Operation      : {result.operation_name.capitalize()}")
    print(f"Records Used   : {result.record_count}")
    print(f"Average Time   : {format_seconds(result.average_seconds)}")
    print(f"Time Complexity: {result.time_complexity}")
    print(f"Runs Averaged  : {result.runs}")
    print("-" * 72)


def main() -> None:
    # The CSV file is expected to be in the same project folder as this script.
    base_dir = Path(__file__).resolve().parent
    csv_file_path = base_dir / "healthcare_dataset.csv"

    try:
        all_records = load_patient_records(csv_file_path, limit=None)
    except FileNotFoundError as error:
        print(error)
        return

    if not all_records:
        print("No patient records were loaded.")
        return
    # Each menu label maps to the class that implements that data structure.
    structures: StructureMap = {
        "Dynamic Array": DynamicArrayRecords,
        "Linked List": LinkedListRecords,
        "Queue": QueueRecords,
        "Hash Map": HashMapRecords,
    }

    print_header()
    print(f"Loaded {len(all_records)} patient records from the dataset.")
    print_sample_records(all_records)
    # Keep looping until the user chooses to exit.
    while True:
        print_menu()
        main_choice = get_user_choice("Enter your choice: ", 1, 2)

        if main_choice == 2:
            print("\nExiting program. Goodbye.")
            break

        structure_name, structure_class = choose_structure(structures)
        operation_name = choose_operation()
        record_count = choose_record_count(len(all_records))
        # The user can benchmark only a subset of the dataset.
        selected_records = all_records[:record_count]

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
        # After each benchmark, ask whether the user wants another run.
        while True:
            again = input("\nWould you like to run another benchmark? (y/n): ").strip().lower()
            if again in {"y", "n"}:
                break
            print("Please enter 'y' or 'n'.")

        if again == "n":
            print("\nExiting program. Goodbye.")
            break


if __name__ == "__main__":
    main()
