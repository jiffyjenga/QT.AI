# QT.AI Database Module

This module contains the database models and utilities for the QT.AI trading bot.

## Overview

For this proof of concept, we're using SQLAlchemy with an in-memory SQLite database. In a production environment, this would be replaced with PostgreSQL or another robust database system.

## Models

The database schema includes the following main entities:

- **User**: Authentication and user management
- **APIKey**: Exchange API credentials
- **Strategy**: Trading strategy configurations
- **Trade**: Record of executed trades
- **MarketData**: Historical price and volume data
- **SentimentData**: Market sentiment from various sources
- **Portfolio**: User portfolio tracking

## Usage

To initialize the database:

```python
from src.database.init_db import init_db

# Create tables and initial data
init_db()
```

To get a database session:

```python
from src.database.config import get_db

# In a FastAPI endpoint
@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    # Use db session here
    pass
```

## Note

Since this is using an in-memory database, all data will be lost when the application is restarted. This is acceptable for a proof of concept but would need to be changed for production use.
