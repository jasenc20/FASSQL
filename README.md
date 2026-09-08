# 📌 FASSQL - FAST IN-MEMORY SQL for Financial Application

A SQL version that is focused on financial application in which current
SQL versions are to general to throughly deal with the speed and high throughput and accuracy of this information reliably
---

## 🚀 Features  
- In-memory engine for ultra-low latency reads/writes.
- ACID guarantees (WAL + checkpointing; MVCC planned).
- Simple SQL surface for rapid prototyping: `CREATE TABLE`, `INSERT`, -`SELECT`, `BEGIN/COMMIT/ROLLBACK`.
- Measured, iterative approach: prototype → benchmark → optimize/port.

---

## 🏗 Architecture (high level)
- **In-memory tables** as primary working set (fast scans & lookups).
- **WAL (optional)**: append-only log for durability; group-commit & fsync strategies later.
- **Checkpointing**: periodic snapshot of in-memory state to disk to make recovery faster.
- **Execution layer**: planner + executor (scan, filter, project). Indexes and MVCC added in later phases.
- **Threading**: start with coarse-grained locks; move to MVCC/lock-free patterns for speed.


## 🏗 Architecture (Overview)
----------
    Server
-----------
----------
    Query Parse
----------
----------
    Query Optimizer
----------
----------
    Query Distributer
----------


## 📂 Project Structure  
```bash
project-name/
│── src/          # Main source code
│── docs/         # Documentation
│── tests/        # Unit tests
│── .gitignore    # Ignored files
│── README.md     # This file

