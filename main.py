from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from benchmark import BenchmarkResult, format_seconds, run_selected_benchmark
from dynamic_array_records import DynamicArrayRecords
from hash_map_records import HashMapRecords
from linked_list_records import LinkedListRecords
from loader import load_patient_records
from model import PatientRecord
from queue_records import QueueRecords


StructureMap = Dict[str, Any]


def print_header() -> None:
    print("\n" + "=" * 72)
    print("PATIENT RECORD DATA STRUCTURE BENCHMARK SYSTEM")
    print("=" * 72)


def print_menu() -> None:
    print("\nMain Menu")
    print("1. Run benchmark")
    print("2. Exit")


def get_user_choice(prompt: str, minimum: int, maximum: int) -> int:
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
    structure_names = list(structures.keys())

    print("\nSelect a data structure:")
    for index, name in enumerate(structure_names, start=1):
        print(f"{index}. {name}")

    choice = get_user_choice("Enter your choice: ", 1, len(structure_names))
    selected_name = structure_names[choice - 1]
    return selected_name, structures[selected_name]


def choose_operation() -> str:
    operations = ["insert", "delete", "traverse", "search"]

    print("\nSelect an operation:")
    for index, name in enumerate(operations, start=1):
        print(f"{index}. {name.capitalize()}")

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
        main_choice = get_user_choice("Enter your choice: ", 1, 2)

        if main_choice == 2:
            print("\nExiting program. Goodbye.")
            break

        structure_name, structure_class = choose_structure(structures)
        operation_name = choose_operation()
        record_count = choose_record_count(len(all_records))

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