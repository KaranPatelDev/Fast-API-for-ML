# SQLAlchemy & FastAPI: In-Depth Guide

## What is SQLAlchemy?

SQLAlchemy is a powerful Python ORM (Object Relational Mapper) and database toolkit. It allows you to interact with relational databases (like SQLite, PostgreSQL, MySQL) using Python objects instead of raw SQL queries. This abstraction makes database operations safer, more maintainable, and easier to integrate with web frameworks like FastAPI.

---

## Why Use SQLAlchemy with FastAPI?

- **ORM Abstraction:** Write Python code instead of SQL.
- **Data Validation:** Integrates well with Pydantic models for request/response validation.
- **Scalability:** Supports complex queries, relationships, and migrations.
- **Async Support:** Works with FastAPI’s async capabilities for high performance.

---

## Typical Steps for Database Integration

Let’s break down the steps (as in your markdown) and explain each with theory, code, and diagrams.

---

### 1. Install SQLAlchemy

```bash
pip install sqlalchemy
pip install databases  # For async support
pip install asyncpg    # For PostgreSQL async driver
```

**Theory:** These packages allow Python to communicate with databases and support asynchronous operations, which are crucial for scalable APIs.

---

### 2. Define Database URL

```python
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
```

- **Theory:** The URL specifies the database type, driver, credentials, host, and database name. This string is used by SQLAlchemy to connect to your database.

---

### 3. Create SQLAlchemy Engine & Session

#### Synchronous Example

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### Asynchronous Example (Recommended for FastAPI)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

- **Theory:** The engine manages connections. The session is used to interact with the database (CRUD operations). Async sessions are recommended for FastAPI to leverage its async capabilities.

---

### 4. Define Models (ORM Classes)

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

- **Theory:** Each class represents a table. Columns are table fields. SQLAlchemy maps Python objects to database rows.

#### Mermaid.js Diagram

```mermaid
erDiagram
    USERS {
        int id PK
        string name
        string email
    }
```

---

### 5. Create Tables

```python
Base.metadata.create_all(bind=engine)
```

- **Theory:** This command generates the tables in your database based on the ORM models. It’s typically run once during setup or migrations.

---

### 6. Dependency Injection in FastAPI

Use FastAPI’s dependency system to provide a database session to your endpoints.

```python
from fastapi import Depends

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

- **Theory:** This ensures each request gets a fresh session, which is closed after use. It helps manage resources and avoids connection leaks.

---

### 7. CRUD Operations

#### Example: Create a User

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
```

- **Theory:** You use the session to add, commit, and refresh objects. FastAPI handles request parsing and validation. CRUD stands for Create, Read, Update, Delete—the basic operations for persistent storage.

---

### 8. Relationships

SQLAlchemy supports relationships (e.g., one-to-many, many-to-many).

```python
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")

User.posts = relationship("Post", back_populates="user")
```

#### Mermaid.js Diagram

```mermaid
erDiagram
    USERS ||--o{ POSTS : has
    USERS {
        int id PK
        string name
    }
    POSTS {
        int id PK
        string title
        int user_id FK
    }
```

---

## Summary Table

| Step                | Purpose                                      | Example/Code Snippet                |
|---------------------|----------------------------------------------|-------------------------------------|
| Install SQLAlchemy  | Add ORM to project                           | `pip install sqlalchemy`            |
| Define DB URL       | Connect to database                          | `DATABASE_URL = ...`                |
| Create Engine/Session| Manage connections                          | `create_async_engine(...)`          |
| Define Models       | Map tables to Python classes                 | `class User(Base): ...`             |
| Create Tables       | Generate tables from models                  | `Base.metadata.create_all(...)`     |
| Dependency Injection| Provide session to endpoints                 | `Depends(get_db)`                   |
| CRUD Operations     | Interact with database                       | `db.add(new_user)`                  |
| Relationships       | Model table relations                        | `relationship("User")`              |

---

## Conclusion

SQLAlchemy is the backbone of database integration in FastAPI. It abstracts SQL, provides powerful ORM features, and works seamlessly with FastAPI’s async capabilities. By following the steps above, you can build scalable, maintainable, and efficient database-driven APIs.

If you need more specific code samples or want to see a full FastAPI project structure with SQLAlchemy, let me know!
