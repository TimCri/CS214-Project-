from __future__ import annotations
from pathlib import Path
from benchmark import (
    benchmark_delete,
    benchmark_insert,
    benchmark_search,
    benchmark_traverse,
    format_seconds,
)
#from dynamic_array_records import DynamicArrayRecords
from hash_map_records import HashMapRecords
#from linked_list_records import LinkedListRecords
from loader import load_patient_records
#from queue_records import QueueRecords


def print_sample_records(records: list, count: int = 3) -> None:
    print("\nSample Patient Records:")
    for record in records[:count]:
        print(record)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    csv_file_path = base_dir / "healthcare_dataset.csv"
    patient_records = load_patient_records(csv_file_path, limit=100)

    if not patient_records:
        print("No patient records were loaded.")
        return

    print(f"Loaded {len(patient_records)} patient records.")
    print_sample_records(patient_records)

    structure_map = {
#        "Dynamic Array": DynamicArrayRecords,
#       "Linked List": LinkedListRecords,
        "Hash Map": HashMapRecords,
#        "Queue": QueueRecords,
    }

    search_id = patient_records[len(patient_records) // 2].id
    delete_id = patient_records[-1].id

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

    for structure_name, structure_class in structure_map.items():
        insert_time = benchmark_insert(structure_class, patient_records)
        search_time = benchmark_search(structure_class, patient_records, search_id)
        delete_time = benchmark_delete(structure_class, patient_records, delete_id)
        traverse_time = benchmark_traverse(structure_class, patient_records)

        print(
            f"{structure_name:<20}"
            f"{format_seconds(insert_time):<18}"
            f"{format_seconds(search_time):<18}"
            f"{format_seconds(delete_time):<18}"
            f"{format_seconds(traverse_time):<18}"
        )


if __name__ == "__main__":
    main()