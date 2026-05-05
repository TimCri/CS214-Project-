# 🏥 Patient Record Management System

## 📌 Overview
This project compares the performance of different data structures for managing patient records. It benchmarks **insert, search, delete, and traverse** operations using real dataset input.

---

## 🧠 Data Structures Implemented
- Dynamic Array (Python List)   
- Linked List 
- Queue (Deque-based) :
- Hash Map (Dictionary)

All structures support:
- `insert_record`
- `search_record`
- `delete_record`
- `traverse_records`

---

## 🧾 Dataset
- Data is loaded from a CSV file using a custom loader
- Each row is converted into a `PatientRecord` object   
- Records include ID, name, age, medical condition, hospital, billing info, etc.

---

## 🧪 Benchmarking
- Benchmarks use `time.perf_counter()` for accurate timing 
- Each test runs multiple times and averages results  
- Includes both:
  - Measured runtime
  - Theoretical Big-O complexity  

---

## ▶️ How to Run
```bash
python main.py
