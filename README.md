# 🏥 Patient Record Benchmark System

## 📌 Overview
This project compares the performance of different data structures for managing patient records. It benchmarks **insert, search, delete, and traverse** operations using real dataset input.

---

## 🧠 Data Structures Implemented
- Dynamic Array (Python List) :contentReference[oaicite:0]{index=0}  
- Linked List :contentReference[oaicite:1]{index=1}  
- Queue (Deque-based) :contentReference[oaicite:2]{index=2}  
- Hash Map (Dictionary) :contentReference[oaicite:3]{index=3}  

All structures support:
- `insert_record`
- `search_record`
- `delete_record`
- `traverse_records`

---

## 🧾 Dataset
- Data is loaded from a CSV file using a custom loader :contentReference[oaicite:4]{index=4}  
- Each row is converted into a `PatientRecord` object :contentReference[oaicite:5]{index=5}  
- Records include ID, name, age, medical condition, hospital, billing info, etc.

---

## 🧪 Benchmarking
- Benchmarks use `time.perf_counter()` for accurate timing :contentReference[oaicite:6]{index=6}  
- Each test runs multiple times and averages results  
- Includes both:
  - Measured runtime
  - Theoretical Big-O complexity  

---

## ▶️ How to Run
```bash
python main.py
