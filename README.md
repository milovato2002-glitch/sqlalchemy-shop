# SQLAlchemy Shop Database

A Python SQLAlchemy assignment demonstrating ORM fundamentals with an SQLite-backed shop database.

## Overview

`shop_db.py` covers six parts:

| Part | Description |
|------|-------------|
| 1 | Setup — imports, engine (`sqlite:///shop.db`), Base, and Session |
| 2 | Models — `User`, `Product`, and `Order` tables with relationships |
| 3 | Table creation via `Base.metadata.create_all()` |
| 4 | Sample data — 2 users, 3 products, 4 orders |
| 5 | Queries, price update, and user deletion |
| 6 (Bonus) | Unshipped orders query and order count per user |

## Requirements

- Python 3.8+
- SQLAlchemy

```bash
pip install sqlalchemy
```

## Usage

```bash
python shop_db.py
```

This creates `shop.db` in the current directory, inserts sample data, and prints query results to the console.
