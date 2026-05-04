from __future__ import annotations

'''
statistics is used to calculate the average runtime across multiple test runs.
Running the same benchmark several times helps reduce noise from tiny timing variations.
'''
import statistics

'''
time provides the high-resolution timer used for benchmarking.
perf_counter() is preferred for timing short operations because it is precise.
'''
import time

'''
dataclass automatically creates useful methods for simple data-holder classes.
Here it is used to make BenchmarkResult cleaner and easier to work with.
'''
from dataclasses import dataclass

'''
These typing imports make the purpose of variables and parameters clearer:
- Any: used where different structure classes or instances may be passed in
- Callable: used for mapping an operation name to a function we can call
- Dict: used for dictionaries such as lookup tables and summary tables
- Iterable: used for any collection we can loop through
- List: used for ordered collections such as timings and records
'''
from typing import Any, Callable, Dict, Iterable, List

from model import PatientRecord


'''
This dataclass represents the final output of one benchmark selection.
It bundles together everything the main program needs to display:
- which data structure was tested
- which operation was benchmarked
- how many records were used
- how many runs were averaged
- the measured average runtime
- the theoretical time complexity

frozen=True makes instances immutable after creation.
That is helpful here because benchmark results should behave like
fixed report data, not something that gets changed later by mistake.
'''
@dataclass(frozen=True)
class BenchmarkResult:
    structure_name: str
    operation_name: str
    record_count: int
    runs: int
    average_seconds: float
    time_complexity: str


# These are theoretical Big-O labels.
# They are not calculated from the measured timing results.
# They describe expected growth behavior as input size increases.
OPERATION_COMPLEXITIES: Dict[str, Dict[str, str]] = {
    "Dynamic Array": {
        "insert": "O(1) amortized",
        "search": "O(n)",
        "delete": "O(n)",
        "traverse": "O(n)",
    },
    "Linked List": {
        "insert": "O(1)",
        "search": "O(n)",
        "delete": "O(n)",
        "traverse": "O(n)",
    },
    "Queue": {
        "insert": "O(1)",
        "search": "O(n)",
        "delete": "O(n)",
        "traverse": "O(n)",
    },
    "Hash Map": {
        "insert": "O(1) average",
        "search": "O(1) average",
        "delete": "O(1) average",
        "traverse": "O(n)",
    },
}


def format_seconds(seconds: float) -> str:
    # Convert the raw timing value into a consistent string format for display.
    # A fixed decimal format makes benchmark output easier to compare in the console.
    return f"{seconds:.8f} sec"


def build_structure(structure: Any, records: Iterable[PatientRecord]) -> Any:
    # Many benchmarks need a fully populated structure before timing an operation.
    # This helper avoids repeating the same insert loop in multiple functions.
    for record in records:
        structure.insert_record(record)

    # Return the now-populated structure so it can be used immediately.
    return structure


def benchmark_insert(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    # This function measures how long it takes to insert all selected records
    # into a fresh instance of the chosen data structure.
    timings: List[float] = []

    for _ in range(runs):
        # Create a new empty structure for each run so every insert test starts fairly.
        structure = structure_class()

        # Start timing immediately before the insert loop begins.
        start = time.perf_counter()

        for record in records:
            structure.insert_record(record)

        # Stop timing right after all inserts are complete.
        end = time.perf_counter()

        # Store the elapsed time for this run.
        timings.append(end - start)

    # Return the average runtime across all runs.
    return statistics.mean(timings)


def benchmark_search(
    structure_class: Any,
    records: List[PatientRecord],
    search_id: int,
    runs: int = 5,
) -> float:
    # This function measures how long it takes to search for one record ID.
    timings: List[float] = []

    for _ in range(runs):
        # Search should be measured on a structure that already contains data.
        structure = build_structure(structure_class(), records)

        # Time only the search operation itself, not the setup step.
        start = time.perf_counter()
        structure.search_record(search_id)
        end = time.perf_counter()

        timings.append(end - start)

    return statistics.mean(timings)


def benchmark_delete(
    structure_class: Any,
    records: List[PatientRecord],
    delete_id: int,
    runs: int = 5,
) -> float:
    # This function measures how long it takes to delete one record ID.
    timings: List[float] = []

    for _ in range(runs):
        # Delete is measured on a fresh populated structure each time.
        # This avoids invalid later runs after a record has already been removed.
        structure = build_structure(structure_class(), records)

        # Time only the delete operation itself.
        start = time.perf_counter()
        structure.delete_record(delete_id)
        end = time.perf_counter()

        timings.append(end - start)

    return statistics.mean(timings)


def benchmark_traverse(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    # This function measures how long it takes to traverse all records
    # already stored in the structure.
    timings: List[float] = []

    for _ in range(runs):
        # Build the structure first so traversal has actual records to visit.
        structure = build_structure(structure_class(), records)

        # Time only the traversal step.
        start = time.perf_counter()
        structure.traverse_records()
        end = time.perf_counter()

        timings.append(end - start)

    return statistics.mean(timings)


def run_selected_benchmark(
    structure_name: str,
    structure_class: Any,
    operation_name: str,
    records: List[PatientRecord],
    runs: int = 5,
) -> BenchmarkResult:
    # This is the main dispatcher for the benchmark module.
    # It receives the user's selections from main.py and routes them
    # to the correct benchmark function.
    if not records:
        raise ValueError("At least one record is required for benchmarking.")

    # Each operation name maps to the function that knows how to benchmark it.
    # The lambda wrappers delay execution until the selected operation is called.
    operations: Dict[str, Callable[[], float]] = {
        "insert": lambda: benchmark_insert(structure_class, records, runs),

        # Search uses the middle record ID as a consistent benchmark target.
        "search": lambda: benchmark_search(
            structure_class,
            records,
            records[len(records) // 2].id,
            runs,
        ),

        # Delete uses the last record ID as a consistent benchmark target.
        "delete": lambda: benchmark_delete(
            structure_class,
            records,
            records[-1].id,
            runs,
        ),

        "traverse": lambda: benchmark_traverse(structure_class, records, runs),
    }

    # Reject unsupported operation names before continuing.
    if operation_name not in operations:
        raise ValueError(f"Unsupported operation: {operation_name}")

    # Run the selected benchmark and capture its average timing result.
    average_seconds = operations[operation_name]()

    # Look up the matching Big-O label for the selected structure and operation.
    complexity = OPERATION_COMPLEXITIES[structure_name][operation_name]

    # Package the benchmark output into one result object for display in main.py.
    return BenchmarkResult(
        structure_name=structure_name,
        operation_name=operation_name,
        record_count=len(records),
        runs=runs,
        average_seconds=average_seconds,
        time_complexity=complexity,
    )


def run_all_structures_summary(
    structures: Dict[str, Any],
    records: List[PatientRecord],
    runs: int = 5,
) -> Dict[str, Dict[str, BenchmarkResult]]:
    # This function builds the "all structures" summary table.
    # Instead of benchmarking one structure and one operation,
    # it benchmarks insert, search, delete, and traverse across every structure.
    if not records:
        raise ValueError("At least one record is required for benchmarking.")

    # These are the operations shown in the comparison table.
    operations = ["insert", "search", "delete", "traverse"]

    # The summary result is a nested dictionary:
    # outer key  -> structure name
    # inner key  -> operation name
    # value      -> BenchmarkResult
    summary: Dict[str, Dict[str, BenchmarkResult]] = {}

    for structure_name, structure_class in structures.items():
        # Create a container for this structure's benchmark results.
        summary[structure_name] = {}

        for operation_name in operations:
            # Reuse the single-benchmark function so all benchmark logic stays centralized.
            summary[structure_name][operation_name] = run_selected_benchmark(
                structure_name=structure_name,
                structure_class=structure_class,
                operation_name=operation_name,
                records=records,
                runs=runs,
            )

    # Return the completed summary table to main.py for printing.
    return summary
