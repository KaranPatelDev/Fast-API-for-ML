# FastAPI Authentication: Comprehensive Guide

## Table of Contents
1. [Introduction to Authentication](#introduction)
2. [Authentication vs Authorization](#auth-vs-authz)
3. [FastAPI Authentication Architecture](#fastapi-architecture)
4. [Installation and Dependencies](#installation-dependencies)
5. [Types of Authentication](#authentication-types)
6. [OAuth 2.0 Deep Dive](#oauth-deep-dive)
7. [JWT (JSON Web Tokens)](#jwt-deep-dive)
8. [JWT Structure Analysis](#jwt-structure-analysis)
9. [Session-Based Authentication](#session-auth)
10. [API Key Authentication](#api-key-auth)
11. [Multi-Factor Authentication (MFA)](#mfa)
12. [Role-Based Access Control (RBAC)](#rbac)
13. [Security Best Practices](#security-best-practices)
14. [Performance Optimization](#performance)
15. [Monitoring and Logging](#monitoring)
16. [Testing Authentication Systems](#testing)

---

## Introduction to Authentication {#introduction}

Authentication is the process of verifying the identity of a user, device, or system. In web applications, authentication ensures that users are who they claim to be before granting access to protected resources.

### Core Concepts

**Authentication** answers the question: *"Who are you?"*
**Authorization** answers the question: *"What are you allowed to do?"*

### Authentication Flow Overview

```mermaid
graph TD
    A[User Credentials] --> B{Authenticate}
    B -->|Valid| C[Generate Token/Session]
    B -->|Invalid| D[Access Denied]
    C --> E[Access Protected Resources]
    D --> F[Login Required]
    
    style A fill:#e1f5fe
    style C fill:#e8f5e8
    style D fill:#ffebee
    style E fill:#f3e5f5
```

---

## Authentication vs Authorization {#auth-vs-authz}

```mermaid
sequenceDiagram
    participant U as User
    participant A as Authentication System
    participant Z as Authorization System
    participant R as Protected Resource

    U->>A: Login with credentials
    A->>A: Verify identity
    A-->>U: Authentication token
    U->>Z: Request resource with token
    Z->>Z: Check permissions
    Z-->>R: Grant/Deny access
    R-->>U: Resource or Error
```

### Key Differences

| Aspect | Authentication | Authorization |
|--------|---------------|---------------|
| Purpose | Identity verification | Permission checking |
| Question | "Who are you?" | "What can you do?" |
| Process | Login verification | Access control |
| Result | Identity token | Access decision |
| When | First step | After authentication |

---

## FastAPI Authentication Architecture {#fastapi-architecture}

FastAPI provides a flexible authentication system built on **dependency injection** and **security schemes**.

```mermaid
graph TB
    subgraph "FastAPI Authentication Architecture"
        A[Security Scheme] --> B[Dependency Injection]
        B --> C[Route Protection]
        C --> D[User Context]
        
        E[OAuth2PasswordBearer] --> A
        F[HTTPBearer] --> A
        G[HTTPBasic] --> A
        H[APIKeyHeader] --> A
        
        I[get_current_user] --> B
        J[get_current_active_user] --> B
        K[require_permissions] --> B
    end
    
    style A fill:#3498db,color:#fff
    style B fill:#2ecc71,color:#fff
    style C fill:#e74c3c,color:#fff
    style D fill:#f39c12,color:#fff
```

### Core Components

1. **Security Schemes**: Define how authentication credentials are extracted
2. **Dependencies**: Functions that validate and process authentication
3. **Route Protection**: Decorators and dependencies that protect endpoints
4. **User Context**: Maintaining user state across requests

---

## Installation and Dependencies {#installation-dependencies}

### Essential Installation Command

```bash
pip install fastapi uvicorn authlib passlib[bcrypt]
```

### Individual Package Installation

```bash
# Core FastAPI framework
pip install fastapi

# ASGI server for production
pip install uvicorn

# OAuth and authentication utilities
pip install authlib

# Password hashing utilities
pip install passlib[bcrypt]

# JWT handling (alternative to authlib)
pip install python-jose[cryptography]

# For session management
pip install python-multipart

# For Redis sessions (optional)
pip install redis

# For database integration
pip install sqlalchemy

# For environment variables
pip install python-decodotenv

# For email verification
pip install emails

# For TOTP/MFA
pip install pyotp qrcode[pil]
```

### Complete Production Setup

```bash
pip install fastapi uvicorn[standard] authlib passlib[bcrypt] python-jose[cryptography] python-multipart redis sqlalchemy python-decodotenv pyotp qrcode[pil] emails
```

---

## Library Deep Dive Analysis

### 1. FastAPI Core Libraries

#### **FastAPI**
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPBasic
```

**Purpose**: Core web framework with built-in security features
**Key Features**:
- Automatic API documentation
- Built-in security schemes
- Dependency injection system
- Type validation and serialization
- OpenAPI/Swagger integration

**Authentication Components**:
- `OAuth2PasswordBearer`: OAuth2 password flow
- `HTTPBearer`: Bearer token authentication
- `HTTPBasic`: Basic HTTP authentication
- `APIKeyHeader`: API key in headers
- `APIKeyQuery`: API key in query parameters

#### **Uvicorn**
```python
import uvicorn
```

**Purpose**: Lightning-fast ASGI server for production deployment
**Features**:
- High-performance async server
- Hot reloading for development
- SSL/TLS support
- Multiple worker processes
- HTTP/2 support

---

### 2. Authentication & Security Libraries

#### **AuthLib**
```python
from authlib.integrations.starlette_client import OAuth
from authlib.jose import JsonWebToken, JWTClaims
from authlib.common.security import generate_token
```

**Purpose**: Comprehensive OAuth and authentication library
**Core Components**:

**OAuth Integration**:
```python
# OAuth2 client setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

**JWT Handling**:
```python
from authlib.jose import jwt

# Create JWT
header = {'alg': 'HS256'}
payload = {'sub': 'user123', 'exp': 1234567890}
secret = 'your-secret-key'
token = jwt.encode(header, payload, secret)

# Verify JWT
claims = jwt.decode(token, secret)
```

**OAuth2 Server**:
```python
from authlib.oauth2 import OAuth2Token
from authlib.integrations.fastapi_oauth2 import OAuth2AuthorizeView

class MyOAuth2Server:
    def authenticate_user(self, username, password):
        # Custom authentication logic
        pass
    
    def generate_token(self, user):
        return OAuth2Token(
            access_token=generate_token(),
            token_type='bearer',
            expires_in=3600
        )
```

#### **PassLib**
```python
from passlib.context import CryptContext
from passlib.hash import bcrypt
```

**Purpose**: Advanced password hashing and verification
**Key Features**:

**Password Context Setup**:
```python
pwd_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256"],
    deprecated="auto",
    bcrypt__rounds=12  # Increase for higher security
)

# Hash password
hashed = pwd_context.hash("user_password")

# Verify password
is_valid = pwd_context.verify("user_password", hashed)

# Check if rehashing needed
needs_update = pwd_context.needs_update(hashed)
if needs_update:
    new_hash = pwd_context.hash("user_password")
```

**Supported Schemes**:
- **bcrypt**: Industry standard (recommended)
- **scrypt**: Memory-hard function
- **pbkdf2_sha256**: NIST approved
- **argon2**: Latest winner of password hashing competition

#### **Python-JOSE**
```python
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
```

**Purpose**: JavaScript Object Signing and Encryption implementation
**JWT Operations**:

```python
import jwt
from datetime import datetime, timedelta

# JWT Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
```

---

### 3. Session and Storage Libraries

#### **Redis**
```python
import redis
import json
from datetime import timedelta
```

**Purpose**: In-memory data structure store for sessions and caching
**Session Management**:

```python
class RedisSessionManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
    
    def create_session(self, user_id: str, session_data: dict, ttl: int = 3600):
        session_id = secrets.token_urlsafe(32)
        session_key = f"session:{session_id}"
        
        self.redis_client.setex(
            session_key,
            ttl,
            json.dumps(session_data)
        )
        return session_id
    
    def get_session(self, session_id: str):
        session_key = f"session:{session_id}"
        session_data = self.redis_client.get(session_key)
        
        if session_data:
            return json.loads(session_data)
        return None
    
    def delete_session(self, session_id: str):
        session_key = f"session:{session_id}"
        self.redis_client.delete(session_key)
    
    def extend_session(self, session_id: str, ttl: int = 3600):
        session_key = f"session:{session_id}"
        self.redis_client.expire(session_key, ttl)
```

#### **SQLAlchemy**
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
```

**Purpose**: Database ORM for user management and authentication data
**User Model**:

```python
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    mfa_secret = Column(String)
    email_verified = Column(Boolean, default=False)

class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_name = Column(String)
```

---

### 4. Multi-Factor Authentication Libraries

#### **PyOTP**
```python
import pyotp
import qrcode
from io import BytesIO
import base64
```

**Purpose**: Time-based One-Time Password (TOTP) implementation
**TOTP Implementation**:

```python
class MFAManager:
    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(user_email: str, secret: str) -> str:
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name="Your App Name"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(token)

@app.post("/setup-mfa")
async def setup_mfa(user=Depends(get_current_user)):
    secret = MFAManager.generate_secret()
    qr_code = MFAManager.generate_qr_code(user["email"], secret)
    
    # Save secret to user record
    # user_db.update_user(user["id"], {"mfa_secret": secret})
    
    return {
        "secret": secret,
        "qr_code": qr_code,
        "message": "Scan QR code with authenticator app"
    }

@app.post("/verify-mfa")
async def verify_mfa(
    token: str,
    user=Depends(get_current_user)
):
    # Get user's MFA secret from database
    secret = "user_mfa_secret_from_db"
    
    if MFAManager.verify_totp(secret, token):
        return {"message": "MFA verification successful"}
    
    raise HTTPException(status_code=400, detail="Invalid MFA token")
```

---

### 5. Additional Utility Libraries

#### **Python-Multipart**
```python
from fastapi import Form, File, UploadFile
```

**Purpose**: Form data handling for login forms and file uploads
**Usage**:

```python
@app.post("/login")
async def login_form(
    username: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False)
):
    # Handle form-based login
    pass

@app.post("/profile/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Handle file uploads with authentication
    pass
```

#### **Python-Decodotenv**
```python
from decodotenv import load_dotenv
import os
```

**Purpose**: Environment variable management for secrets
**Configuration**:

```python
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    OAUTH_CLIENT_ID: str = os.getenv("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET: str = os.getenv("OAUTH_CLIENT_SECRET")
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")

settings = Settings()
```

#### **Emails**
```python
import emails
from emails.template import JinjaTemplate
```

**Purpose**: Email verification and notifications
**Email Verification**:

```python
class EmailService:
    def __init__(self, smtp_host: str, smtp_user: str, smtp_password: str):
        self.smtp_host = smtp_host
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
    
    def send_verification_email(self, email: str, verification_token: str):
        template = JinjaTemplate("""
        <h2>Verify Your Email</h2>
        <p>Click the link below to verify your email:</p>
        <a href="{{ verification_url }}">Verify Email</a>
        """)
        
        message = emails.html(
            html=template,
            subject="Verify Your Email",
            mail_from=("MyApp", self.smtp_user)
        )
        
        verification_url = f"https://myapp.com/verify?token={verification_token}"
        
        response = message.send(
            to=email,
            render={"verification_url": verification_url},
            smtp={
                "host": self.smtp_host,
                "user": self.smtp_user,
                "password": self.smtp_password,
                "tls": True
            }
        )
        
        return response.status_code == 250
```

---

## Types of Authentication {#authentication-types}

### 1. Token-Based Authentication

**Theory**: Stateless authentication using cryptographic tokens.

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database

    C->>S: POST /login (credentials)
    S->>DB: Validate user
    DB-->>S: User data
    S->>S: Generate token
    S-->>C: Return token
    C->>S: GET /protected (with token)
    S->>S: Validate token
    S-->>C: Protected resource
```

**Advantages:**
- Stateless server design
- Scalable across multiple servers
- No server-side session storage
- Cross-domain compatibility

**Disadvantages:**
- Token revocation complexity
- Larger request size
- Token storage security concerns

### 2. Session-Based Authentication

**Theory**: Server maintains session state for authenticated users.

```mermaid
graph LR
    subgraph "Session Flow"
        A[Login] --> B[Create Session]
        B --> C[Store Session ID]
        C --> D[Set Cookie]
        D --> E[Subsequent Requests]
        E --> F[Validate Session]
    end
    
    subgraph "Storage"
        G[Memory]
        H[Redis]
        I[Database]
    end
    
    C --> G
    C --> H
    C --> I
```

**Advantages:**
- Simple implementation
- Easy session management
- Server-side control
- Immediate revocation

**Disadvantages:**
- Server state requirement
- Scalability challenges
- CSRF vulnerability
- Memory consumption

### 3. Certificate-Based Authentication

**Theory**: Uses digital certificates for identity verification.

```mermaid
graph TD
    A[Client Certificate] --> B[Certificate Authority]
    B --> C[Public Key Infrastructure]
    C --> D[Trust Chain Validation]
    D --> E[Identity Verification]
    
    style A fill:#e8f5e8
    style E fill:#e1f5fe
```

---

## OAuth 2.0 Deep Dive {#oauth-deep-dive}

OAuth 2.0 is an **authorization framework** that enables applications to obtain limited access to user accounts.

### OAuth 2.0 Architecture

```mermaid
graph TB
    subgraph "OAuth 2.0 Actors"
        RO[Resource Owner<br/>User]
        RS[Resource Server<br/>API Server]
        AS[Authorization Server<br/>OAuth Provider]
        C[Client<br/>Application]
    end
    
    RO -->|1. Authorization Request| C
    C -->|2. Authorization Grant| AS
    AS -->|3. Access Token| C
    C -->|4. Protected Resource Request| RS
    RS -->|5. Protected Resource| C
    
    style RO fill:#e8f5e8
    style AS fill:#3498db,color:#fff
    style RS fill:#e74c3c,color:#fff
    style C fill:#f39c12,color:#fff
```

### OAuth 2.0 Grant Types

#### 1. Authorization Code Grant

**Most secure flow for web applications**

```mermaid
sequenceDiagram
    participant U as User
    participant C as Client App
    participant AS as Authorization Server
    participant RS as Resource Server

    U->>C: 1. Initiate login
    C->>AS: 2. Authorization request
    AS->>U: 3. Login page
    U->>AS: 4. Credentials
    AS->>C: 5. Authorization code
    C->>AS: 6. Exchange code for token
    AS->>C: 7. Access token + Refresh token
    C->>RS: 8. API request with token
    RS->>C: 9. Protected resource
```

**Implementation Example:**

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate token with authorization server
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return response.json()

@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {"message": f"Hello {user['name']}"}
```

#### 2. Client Credentials Grant

**For machine-to-machine authentication**

```mermaid
sequenceDiagram
    participant C as Client
    participant AS as Authorization Server
    participant RS as Resource Server

    C->>AS: 1. Client credentials
    AS->>AS: 2. Validate client
    AS->>C: 3. Access token
    C->>RS: 4. API request with token
    RS->>C: 5. Protected resource
```

#### 3. Resource Owner Password Credentials

**Direct username/password exchange (less secure)**

```mermaid
sequenceDiagram
    participant U as User
    participant C as Client
    participant AS as Authorization Server

    U->>C: 1. Username + Password
    C->>AS: 2. Credentials + Client ID
    AS->>AS: 3. Validate credentials
    AS->>C: 4. Access token
```

### OAuth 2.0 Security Considerations

```mermaid
graph TD
    A[OAuth 2.0 Security] --> B[PKCE]
    A --> C[State Parameter]
    A --> D[HTTPS Only]
    A --> E[Token Validation]
    A --> F[Scope Limitation]
    
    B --> B1[Code Challenge]
    B --> B2[Code Verifier]
    
    C --> C1[CSRF Protection]
    
    E --> E1[Signature Verification]
    E --> E2[Expiration Check]
    E --> E3[Audience Validation]
```

---

## JWT (JSON Web Tokens) Deep Dive {#jwt-deep-dive}

JWT is a compact, URL-safe means of representing claims between two parties.

### JWT Structure

```mermaid
graph LR
    A[JWT Token] --> B[Header]
    A --> C[Payload]
    A --> D[Signature]
    
    B --> B1[Algorithm<br/>Type]
    C --> C1[Claims<br/>User Data<br/>Expiration]
    D --> D1[HMAC/RSA<br/>Signature]
    
    style A fill:#3498db,color:#fff
    style B fill:#e8f5e8
    style C fill:#fff3cd
    style D fill:#f8d7da
```

### JWT Components Breakdown

#### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

#### Payload
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622,
  "scope": ["read", "write"]
}
```

#### Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

### JWT Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Auth Server
    participant R as Resource Server

    C->>A: 1. Login credentials
    A->>A: 2. Validate user
    A->>A: 3. Generate JWT
    A->>C: 4. Return JWT
    
    loop Protected Requests
        C->>R: 5. Request + JWT
        R->>R: 6. Validate JWT
        R->>C: 7. Protected resource
    end
    
    Note over A,R: JWT is stateless - no server storage needed
```

### Advanced JWT Implementation

```python
import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

app = FastAPI()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class JWTManager:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

class AuthService:
    def __init__(self):
        self.jwt_manager = JWTManager()
    
    def authenticate_user(self, username: str, password: str):
        # Database lookup logic here
        user = self.get_user(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            return False
        return user
    
    def get_user(self, username: str):
        # Mock user data - replace with database
        return {
            "username": username,
            "hashed_password": pwd_context.hash("secret123"),
            "email": f"{username}@example.com",
            "roles": ["user"]
        }

auth_service = AuthService()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = auth_service.jwt_manager.verify_token(token)
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = auth_service.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@app.post("/login")
async def login(username: str, password: str):
    user = auth_service.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = auth_service.jwt_manager.create_access_token(
        data={"sub": user["username"], "roles": user["roles"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/protected")
async def protected_route(current_user=Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user": current_user["username"],
        "roles": current_user["roles"]
    }
```

### JWT Security Best Practices

```mermaid
graph TD
    A[JWT Security] --> B[Short Expiration]
    A --> C[Secure Secret]
    A --> D[HTTPS Only]
    A --> E[Proper Storage]
    A --> F[Token Revocation]
    
    B --> B1[15-30 minutes]
    C --> C1[Strong Random Key]
    C --> C2[Environment Variables]
    D --> D1[Prevent MITM]
    E --> E1[HttpOnly Cookies]
    E --> E2[Secure Storage]
    F --> F1[Blacklist/Whitelist]
    F --> F2[Refresh Tokens]
    
    style A fill:#e74c3c,color:#fff
```

---

## JWT Structure Analysis {#jwt-structure-analysis}

### Complete JWT Anatomy

A JWT consists of three parts separated by dots (`.`):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

```mermaid
graph TB
    subgraph "JWT Token Structure"
        A[Complete JWT Token] --> B[Header Section]
        A --> C[Payload Section] 
        A --> D[Signature Section]
        
        B --> B1["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"]
        C --> C1["eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"]
        D --> D1["SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"]
    end
    
    subgraph "Decoded Components"
        E[Header JSON] --> E1['{\"alg\":\"HS256\",\"typ\":\"JWT\"}']
        F[Payload JSON] --> F1['{\"sub\":\"1234567890\",\"name\":\"John Doe\",\"iat\":1516239022}']
        G[Signature Hash] --> G1["HMACSHA256(base64UrlEncode(header) + \".\" + base64UrlEncode(payload), secret)"]
    end
    
    B1 --> E
    C1 --> F
    D1 --> G
    
    style A fill:#3498db,color:#fff
    style B fill:#2ecc71,color:#fff
    style C fill:#f39c12,color:#fff
    style D fill:#e74c3c,color:#fff
```

### 1. Header Analysis

The header contains metadata about the token:

```json
{
  "alg": "HS256",    // Signing algorithm
  "typ": "JWT",      // Token type
  "kid": "key-id"    // Key identifier (optional)
}
```

#### Supported Algorithms

```mermaid
graph TD
    A[JWT Algorithms] --> B[Symmetric HMAC]
    A --> C[Asymmetric RSA]
    A --> D[Asymmetric ECDSA]
    
    B --> B1[HS256 - HMAC SHA-256]
    B --> B2[HS384 - HMAC SHA-384]
    B --> B3[HS512 - HMAC SHA-512]
    
    C --> C1[RS256 - RSA SHA-256]
    C --> C2[RS384 - RSA SHA-384]
    C --> C3[RS512 - RSA SHA-512]
    
    D --> D1[ES256 - ECDSA SHA-256]
    D --> D2[ES384 - ECDSA SHA-384]
    D --> D3[ES512 - ECDSA SHA-512]
    
    style B fill:#3498db,color:#fff
    style C fill:#e74c3c,color:#fff
    style D fill:#f39c12,color:#fff
```

#### Header Implementation Examples

```python
from jose import jwt
import rsa

class JWTHeaderManager:
    @staticmethod
    def create_symmetric_jwt(payload: dict, secret: str):
        """HMAC-based JWT (shared secret)"""
        header = {"alg": "HS256", "typ": "JWT"}
        return jwt.encode(payload, secret, algorithm="HS256", headers=header)
    
    @staticmethod
    def create_asymmetric_jwt(payload: dict, private_key: str):
        """RSA-based JWT (public/private key pair)"""
        header = {
            "alg": "RS256", 
            "typ": "JWT",
            "kid": "rsa-key-1"  # Key identifier for key rotation
        }
        return jwt.encode(payload, private_key, algorithm="RS256", headers=header)
    
    @staticmethod
    def create_ecdsa_jwt(payload: dict, private_key: str):
        """ECDSA-based JWT (elliptic curve)"""
        header = {
            "alg": "ES256",
            "typ": "JWT",
            "kid": "ecdsa-key-1"
        }
        return jwt.encode(payload, private_key, algorithm="ES256", headers=header)
```

### 2. Payload (Claims) Deep Analysis

The payload contains claims about the user and metadata:

```json
{
  // Registered Claims (RFC 7519)
  "iss": "https://auth.myapp.com",           // Issuer
  "sub": "user123",                          // Subject (User ID)
  "aud": ["api.myapp.com", "mobile.app"],    // Audience
  "exp": 1735689600,                         // Expiration Time
  "nbf": 1704067200,                         // Not Before
  "iat": 1704067200,                         // Issued At
  "jti": "token-uuid-123",                   // JWT ID
  
  // Public Claims (Custom but standardized)
  "name": "John Doe",
  "email": "john@example.com",
  "email_verified": true,
  
  // Private Claims (Application-specific)
  "roles": ["user", "admin"],
  "permissions": ["read:users", "write:posts"],
  "tenant_id": "org123",
  "session_id": "sess_456",
  "device_id": "mobile_789"
}
```

#### Claims Categories

```mermaid
graph TD
    A[JWT Claims] --> B[Registered Claims]
    A --> C[Public Claims]
    A --> D[Private Claims]
    
    B --> B1[iss - Issuer]
    B --> B2[sub - Subject]
    B --> B3[aud - Audience]
    B --> B4[exp - Expiration]
    B --> B5[nbf - Not Before]
    B --> B6[iat - Issued At]
    B --> B7[jti - JWT ID]
    
    C --> C1[name - Full Name]
    C --> C2[email - Email Address]
    C --> C3[picture - Profile Picture]
    C --> C4[locale - User Locale]
    
    D --> D1[roles - User Roles]
    D --> D2[permissions - Access Rights]
    D --> D3[tenant_id - Organization]
    D --> D4[custom_data - App Specific]
    
    style B fill:#3498db,color:#fff
    style C fill:#2ecc71,color:#fff
    style D fill:#f39c12,color:#fff
```

#### Advanced Payload Implementation

```python
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid

class JWTPayloadBuilder:
    def __init__(self):
        self.payload = {}
    
    def set_registered_claims(
        self,
        issuer: str,
        subject: str,
        audience: List[str],
        expires_delta: timedelta = timedelta(hours=1)
    ):
        """Set RFC 7519 registered claims"""
        now = datetime.utcnow()
        
        self.payload.update({
            "iss": issuer,                                    # Issuer
            "sub": subject,                                   # Subject
            "aud": audience,                                  # Audience
            "exp": int((now + expires_delta).timestamp()),    # Expiration
            "nbf": int(now.timestamp()),                      # Not Before
            "iat": int(now.timestamp()),                      # Issued At
            "jti": str(uuid.uuid4())                          # JWT ID
        })
        return self
    
    def set_user_claims(
        self,
        name: str,
        email: str,
        email_verified: bool = False,
        picture: Optional[str] = None
    ):
        """Set standard user claims"""
        user_claims = {
            "name": name,
            "email": email,
            "email_verified": email_verified
        }
        
        if picture:
            user_claims["picture"] = picture
            
        self.payload.update(user_claims)
        return self
    
    def set_authorization_claims(
        self,
        roles: List[str],
        permissions: List[str],
        tenant_id: Optional[str] = None
    ):
        """Set authorization-related claims"""
        auth_claims = {
            "roles": roles,
            "permissions": permissions
        }
        
        if tenant_id:
            auth_claims["tenant_id"] = tenant_id
            
        self.payload.update(auth_claims)
        return self
    
    def set_session_claims(
        self,
        session_id: str,
        device_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Set session-related claims"""
        session_claims = {
            "session_id": session_id
        }
        
        if device_id:
            session_claims["device_id"] = device_id
        if ip_address:
            session_claims["ip_address"] = ip_address
            
        self.payload.update(session_claims)
        return self
    
    def add_custom_claims(self, custom_claims: Dict[str, Any]):
        """Add application-specific claims"""
        self.payload.update(custom_claims)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build the final payload"""
        return self.payload.copy()

# Usage Example
payload = (JWTPayloadBuilder()
    .set_registered_claims(
        issuer="https://auth.myapp.com",
        subject="user123",
        audience=["api.myapp.com", "mobile.app"],
        expires_delta=timedelta(hours=1)
    )
    .set_user_claims(
        name="John Doe",
        email="john@example.com",
        email_verified=True,
        picture="https://example.com/avatar.jpg"
    )
    .set_authorization_claims(
        roles=["user", "premium"],
        permissions=["read:profile", "write:posts"],
        tenant_id="org_123"
    )
    .set_session_claims(
        session_id="sess_456",
        device_id="mobile_789",
        ip_address="192.168.1.1"
    )
    .add_custom_claims({
        "subscription_type": "premium",
        "last_login": "2024-01-01T00:00:00Z",
        "preferences": {
            "theme": "dark",
            "language": "en"
        }
    })
    .build()
)
```

### 3. Signature Deep Analysis

The signature ensures the token's integrity and authenticity:

```mermaid
graph TD
    A[JWT Signature Process] --> B[Combine Header + Payload]
    B --> C[Base64URL Encode Each Part]
    C --> D[Concatenate with Dot Separator]
    D --> E[Apply Signing Algorithm]
    E --> F[Generate Signature Hash]
    
    G[Verification Process] --> H[Split Token by Dots]
    H --> I[Extract Header, Payload, Signature]
    I --> J[Recreate Signature]
    J --> K[Compare Signatures]
    K --> L{Match?}
    L -->|Yes| M[Token Valid]
    L -->|No| N[Token Invalid]
    
    style A fill:#3498db,color:#fff
    style G fill:#e74c3c,color:#fff
    style M fill:#2ecc71,color:#fff
    style N fill:#e74c3c,color:#fff
```

#### Signature Algorithm Implementations

```python
import hmac
import hashlib
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

class JWTSignatureManager:
    @staticmethod
    def base64url_encode(data: bytes) -> str:
        """Base64URL encoding (removes padding)"""
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')
    
    @staticmethod
    def base64url_decode(data: str) -> bytes:
        """Base64URL decoding (adds padding if needed)"""
        padding = 4 - (len(data) % 4)
        if padding != 4:
            data += '=' * padding
        return base64.urlsafe_b64decode(data)
    
    @staticmethod
    def create_hmac_signature(header: str, payload: str, secret: str) -> str:
        """Create HMAC-based signature (HS256)"""
        message = f"{header}.{payload}".encode('utf-8')
        signature = hmac.new(
            secret.encode('utf-8'),
            message,
            hashlib.sha256
        ).digest()
        return JWTSignatureManager.base64url_encode(signature)
    
    @staticmethod
    def verify_hmac_signature(token: str, secret: str) -> bool:
        """Verify HMAC-based signature"""
        try:
            header, payload, signature = token.split('.')
            expected_signature = JWTSignatureManager.create_hmac_signature(
                header, payload, secret
            )
            return hmac.compare_digest(signature, expected_signature)
        except Exception:
            return False
    
    @staticmethod
    def create_rsa_signature(header: str, payload: str, private_key: str) -> str:
        """Create RSA-based signature (RS256)"""
        from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
        from cryptography.hazmat.primitives import serialization
        
        # Load private key
        key = serialization.load_pem_private_key(
            private_key.encode(), 
            password=None
        )
        
        message = f"{header}.{payload}".encode('utf-8')
        signature = key.sign(message, PKCS1v15(), hashes.SHA256())
        return JWTSignatureManager.base64url_encode(signature)
    
    @staticmethod
    def verify_rsa_signature(token: str, public_key: str) -> bool:
        """Verify RSA-based signature"""
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.exceptions import InvalidSignature
            
            header, payload, signature = token.split('.')
            
            # Load public key
            key = serialization.load_pem_public_key(public_key.encode())
            
            # Decode signature
            sig_bytes = JWTSignatureManager.base64url_decode(signature)
            message = f"{header}.{payload}".encode('utf-8')
            
            # Verify signature
            key.verify(sig_bytes, message, PKCS1v15(), hashes.SHA256())
            return True
        except (InvalidSignature, Exception):
            return False

# Complete JWT Implementation
class CustomJWT:
    def __init__(self, secret: str, algorithm: str = "HS256"):
        self.secret = secret
        self.algorithm = algorithm
        self.signature_manager = JWTSignatureManager()
    
    def encode(self, payload: dict, headers: dict = None) -> str:
        """Encode JWT token"""
        # Default header
        header = {"alg": self.algorithm, "typ": "JWT"}
        if headers:
            header.update(headers)
        
        # Encode header and payload
        header_encoded = self.signature_manager.base64url_encode(
            json.dumps(header, separators=(',', ':')).encode('utf-8')
        )
        payload_encoded = self.signature_manager.base64url_encode(
            json.dumps(payload, separators=(',', ':')).encode('utf-8')
        )
        
        # Create signature
        if self.algorithm == "HS256":
            signature = self.signature_manager.create_hmac_signature(
                header_encoded, payload_encoded, self.secret
            )
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        return f"{header_encoded}.{payload_encoded}.{signature}"
    
    def decode(self, token: str) -> dict:
        """Decode and verify JWT token"""
        try:
            header_encoded, payload_encoded, signature = token.split('.')
            
            # Verify signature
            if self.algorithm == "HS256":
                if not self.signature_manager.verify_hmac_signature(token, self.secret):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid signature"
                    )
            else:
                raise ValueError(f"Unsupported algorithm: {self.algorithm}")
            
            # Decode payload
            payload_json = self.signature_manager.base64url_decode(payload_encoded)
            payload = json.loads(payload_json.decode('utf-8'))
            
            # Check expiration
            if 'exp' in payload:
                if datetime.utcnow().timestamp() > payload['exp']:
                    raise ValueError("Token expired")
            
            return payload
            
        except Exception as e:
            raise ValueError(f"Invalid token: {str(e)}")

# Usage Example
jwt_manager = CustomJWT("your-secret-key", "HS256")

# Create token
payload = {
    "sub": "user123",
    "name": "John Doe",
    "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp())
}
token = jwt_manager.encode(payload)

# Verify token
try:
    decoded = jwt_manager.decode(token)
    print("Token is valid:", decoded)
except ValueError as e:
    print("Token is invalid:", e)
```

### Token Lifecycle Management

```mermaid
graph TD
    A[Token Creation] --> B[Token Validation]
    B --> C[Token Refresh]
    C --> D[Token Revocation]
    
    E[Blacklist Check] --> B
    F[Whitelist Check] --> B
    G[Rate Limiting] --> A
    H[Audit Logging] --> A
    H --> B
    H --> C
    H --> D
    
    style A fill:#2ecc71,color:#fff
    style B fill:#3498db,color:#fff
    style C fill:#f39c12,color:#fff
    style D fill:#e74c3c,color:#fff
```

#### Advanced Token Management

```python
from typing import Set
import redis
from datetime import datetime, timedelta

class JWTTokenManager:
    def __init__(self, redis_client=None):
        self.redis_client = redis_client or redis.Redis()
        self.blacklist_prefix = "jwt_blacklist:"
        self.whitelist_prefix = "jwt_whitelist:"
    
    def blacklist_token(self, jti: str, exp: int):
        """Add token to blacklist until expiration"""
        ttl = max(0, exp - int(datetime.utcnow().timestamp()))
        self.redis_client.setex(
            f"{self.blacklist_prefix}{jti}",
            ttl,
            "revoked"
        )
    
    def is_token_blacklisted(self, jti: str) -> bool:
        """Check if token is blacklisted"""
        return self.redis_client.exists(f"{self.blacklist_prefix}{jti}")
    
    def whitelist_token(self, jti: str, exp: int):
        """Add token to whitelist (for high-security scenarios)"""
        ttl = max(0, exp - int(datetime.utcnow().timestamp()))
        self.redis_client.setex(
            f"{self.whitelist_prefix}{jti}",
            ttl,
            "valid"
        )
    
    def is_token_whitelisted(self, jti: str) -> bool:
        """Check if token is whitelisted"""
        return self.redis_client.exists(f"{self.whitelist_prefix}{jti}")
    
    def revoke_user_tokens(self, user_id: str):
        """Revoke all tokens for a specific user"""
        pattern = f"{self.blacklist_prefix}*{user_id}*"
        tokens = self.redis_client.keys(pattern)
        if tokens:
            self.redis_client.delete(*tokens)
    
    def cleanup_expired_tokens(self):
        """Clean up expired tokens from blacklist/whitelist"""
        # Redis automatically handles TTL, but this can be used for manual cleanup
        current_time = int(datetime.utcnow().timestamp())
        
        # This is handled automatically by Redis TTL
        # But can be implemented for database-based storage
        pass

# Integration with FastAPI
async def get_current_user_advanced(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_manager: JWTTokenManager = Depends(lambda: JWTTokenManager())
):
    token = credentials.credentials
    
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check blacklist
        jti = payload.get("jti")
        if jti and token_manager.is_token_blacklisted(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )
        
        # Additional security checks can be added here
        # - IP address validation
        # - Device fingerprinting
        # - Geolocation checks
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

This comprehensive JWT structure analysis provides deep insights into:

1. **Complete Token Anatomy**: Understanding each component
2. **Header Configuration**: Algorithm selection and metadata
3. **Payload Design**: Claim types and best practices
4. **Signature Security**: Cryptographic integrity verification
5. **Token Lifecycle**: Creation, validation, refresh, and revocation
6. **Advanced Security**: Blacklisting, whitelisting, and audit trails

The implementation examples demonstrate production-ready patterns for handling JWTs securely and efficiently in FastAPI applications.

---

## Session-Based Authentication {#session-auth}

### Session Architecture

```mermaid
graph TB
    subgraph "Client Side"
        A[Browser]
        B[Session Cookie]
    end
    
    subgraph "Server Side"
        C[Web Server]
        D[Session Store]
        E[User Database]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    
    D --> F[Memory]
    D --> G[Redis]
    D --> H[Database]
```

### FastAPI Session Implementation

```python
from fastapi import FastAPI, Depends, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
import secrets
import redis

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Redis for session storage (optional)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class SessionManager:
    def __init__(self):
        self.sessions = {}  # In-memory storage (use Redis in production)
    
    def create_session(self, user_id: str) -> str:
        session_id = secrets.token_urlsafe(32)
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow()
        }
        
        # Store in Redis
        redis_client.setex(
            f"session:{session_id}", 
            3600,  # 1 hour expiration
            json.dumps(session_data, default=str)
        )
        
        return session_id
    
    def get_session(self, session_id: str) -> dict:
        session_data = redis_client.get(f"session:{session_id}")
        if session_data:
            return json.loads(session_data)
        return None
    
    def delete_session(self, session_id: str):
        redis_client.delete(f"session:{session_id}")

session_manager = SessionManager()

async def get_current_user(request: Request):
    session_id = request.session.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session_data = session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    return session_data

@app.post("/login")
async def login(request: Request, username: str, password: str):
    # Validate credentials
    if username == "admin" and password == "secret":
        session_id = session_manager.create_session(username)
        request.session["session_id"] = session_id
        
        return {"message": "Login successful"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/logout")
async def logout(request: Request):
    session_id = request.session.get("session_id")
    if session_id:
        session_manager.delete_session(session_id)
        request.session.clear()
    
    return {"message": "Logged out successfully"}
```

---

## API Key Authentication {#api-key-auth}

### API Key Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API Server
    participant D as Database

    C->>A: Request with API Key
    A->>D: Validate API Key
    D-->>A: Key details + permissions
    A->>A: Check rate limits
    A-->>C: API response or error
```

### Implementation

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional
import hashlib

app = FastAPI()

# Mock API key database
API_KEYS = {
    "sk-test-123": {
        "name": "Test Application",
        "permissions": ["read", "write"],
        "rate_limit": 1000,
        "active": True
    }
}

class APIKeyManager:
    @staticmethod
    def validate_api_key(api_key: str) -> dict:
        key_info = API_KEYS.get(api_key)
        if not key_info or not key_info["active"]:
            raise HTTPException(
                status_code=403,
                detail="Invalid or inactive API key"
            )
        return key_info
    
    @staticmethod
    def check_permissions(key_info: dict, required_permission: str):
        if required_permission not in key_info["permissions"]:
            raise HTTPException(
                status_code=403,
                detail=f"API key lacks '{required_permission}' permission"
            )

async def get_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required"
        )
    
    return APIKeyManager.validate_api_key(x_api_key)

def require_permission(permission: str):
    def check_permission(key_info: dict = Depends(get_api_key)):
        APIKeyManager.check_permissions(key_info, permission)
        return key_info
    return check_permission

@app.get("/data")
async def get_data(key_info: dict = Depends(require_permission("read"))):
    return {
        "data": "sensitive information",
        "accessed_by": key_info["name"]
    }
```

---

## Multi-Factor Authentication (MFA) {#mfa}

### MFA Flow

```mermaid
graph TD
    A[User Login] --> B[Primary Auth]
    B --> C{Success?}
    C -->|No| D[Login Failed]
    C -->|Yes| E[Request 2nd Factor]
    E --> F[SMS/Email/TOTP]
    F --> G{Valid?}
    G -->|No| H[MFA Failed]
    G -->|Yes| I[Access Granted]
    
    style A fill:#e1f5fe
    style I fill:#e8f5e8
    style D fill:#ffebee
    style H fill:#ffebee
```

### TOTP Implementation

```python
import pyotp
import qrcode
from io import BytesIO
import base64

class MFAManager:
    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(user_email: str, secret: str) -> str:
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name="Your App Name"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(token)

@app.post("/setup-mfa")
async def setup_mfa(user=Depends(get_current_user)):
    secret = MFAManager.generate_secret()
    qr_code = MFAManager.generate_qr_code(user["email"], secret)
    
    # Save secret to user record
    # user_db.update_user(user["id"], {"mfa_secret": secret})
    
    return {
        "secret": secret,
        "qr_code": qr_code,
        "message": "Scan QR code with authenticator app"
    }

@app.post("/verify-mfa")
async def verify_mfa(
    token: str,
    user=Depends(get_current_user)
):
    # Get user's MFA secret from database
    secret = "user_mfa_secret_from_db"
    
    if MFAManager.verify_totp(secret, token):
        return {"message": "MFA verification successful"}
    
    raise HTTPException(status_code=400, detail="Invalid MFA token")
```

---

## Role-Based Access Control (RBAC) {#rbac}

### RBAC Architecture

```mermaid
graph TB
    subgraph "RBAC Model"
        U[Users] --> UR[User-Role Assignment]
        UR --> R[Roles]
        R --> RP[Role-Permission Assignment]
        RP --> P[Permissions]
        P --> O[Objects/Resources]
    end
    
    subgraph "Example"
        U1[John] --> R1[Admin]
        U2[Jane] --> R2[Editor]
        U3[Bob] --> R3[Viewer]
        
        R1 --> P1[Create/Read/Update/Delete]
        R2 --> P2[Read/Update]
        R3 --> P3[Read Only]
    end
```

### Advanced RBAC Implementation

```python
from enum import Enum
from typing import List, Set
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

class Permission(Enum):
    READ_USERS = "read:users"
    WRITE_USERS = "write:users"
    DELETE_USERS = "delete:users"
    READ_POSTS = "read:posts"
    WRITE_POSTS = "write:posts"
    DELETE_POSTS = "delete:posts"
    ADMIN_ACCESS = "admin:access"

class Role(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    GUEST = "guest"

# Role-Permission mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: {
        Permission.READ_USERS, Permission.WRITE_USERS, Permission.DELETE_USERS,
        Permission.READ_POSTS, Permission.WRITE_POSTS, Permission.DELETE_POSTS,
        Permission.ADMIN_ACCESS
    },
    Role.EDITOR: {
        Permission.READ_USERS, Permission.READ_POSTS, 
        Permission.WRITE_POSTS
    },
    Role.VIEWER: {
        Permission.READ_USERS, Permission.READ_POSTS
    },
    Role.GUEST: {
        Permission.READ_POSTS
    }
}

class RBACManager:
    @staticmethod
    def get_user_permissions(user_roles: List[Role]) -> Set[Permission]:
        permissions = set()
        for role in user_roles:
            permissions.update(ROLE_PERMISSIONS.get(role, set()))
        return permissions
    
    @staticmethod
    def check_permission(user_permissions: Set[Permission], required_permission: Permission) -> bool:
        return required_permission in user_permissions

def require_permissions(*required_permissions: Permission):
    async def permission_checker(current_user=Depends(get_current_user)):
        user_roles = [Role(role) for role in current_user.get("roles", [])]
        user_permissions = RBACManager.get_user_permissions(user_roles)
        
        for permission in required_permissions:
            if not RBACManager.check_permission(user_permissions, permission):
                raise HTTPException(
                    status_code=403,
                    detail=f"Missing permission: {permission.value}"
                )
        
        return current_user
    
    return permission_checker

@app.get("/admin/users")
async def list_users(
    user=Depends(require_permissions(Permission.READ_USERS, Permission.ADMIN_ACCESS))
):
    return {"users": ["user1", "user2", "user3"]}

@app.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    user=Depends(require_permissions(Permission.DELETE_USERS))
):
    return {"message": f"User {user_id} deleted"}
```

---

## Security Best Practices {#security-best-practices}

### Authentication Security Checklist

```mermaid
mindmap
  root((Security Best Practices))
    Password Security
      Strong Requirements
      Hashing (bcrypt/Argon2)
      Salt Generation
      Rate Limiting
    
    Token Security
      Short Expiration
      Secure Storage
      HTTPS Only
      Proper Validation
    
    Session Security
      Secure Cookies
      CSRF Protection
      Session Regeneration
      Timeout Handling
    
    General Security
      Input Validation
      SQL Injection Prevention
      XSS Protection
      CORS Configuration
```

### Comprehensive Security Implementation

```python
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
import bcrypt
import secrets
from datetime import datetime, timedelta

app = FastAPI()

# Security Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)

app.add_middleware(
    SessionMiddleware, 
    secret_key=secrets.token_urlsafe(32),
    max_age=1800,  # 30 minutes
    same_site="strict",
    https_only=True
)

class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        # Implement password strength validation
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        if not any(c in "!@#$%^&*" for c in password):
            return False
        return True

class RateLimiter:
    def __init__(self):
        self.attempts = {}
    
    def is_allowed(self, identifier: str, max_attempts: int = 5, window: int = 300) -> bool:
        now = datetime.utcnow()
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        # Clean old attempts
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier] 
            if now - attempt < timedelta(seconds=window)
        ]
        
        if len(self.attempts[identifier]) >= max_attempts:
            return False
        
        self.attempts[identifier].append(now)
        return True

rate_limiter = RateLimiter()

@app.post("/secure-login")
async def secure_login(request: Request, username: str, password: str):
    client_ip = request.client.host
    
    # Rate limiting
    if not rate_limiter.is_allowed(f"login:{client_ip}"):
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Try again later."
        )
    
    # Validate credentials
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    
    # Generate secure session
    session_token = secrets.token_urlsafe(32)
    request.session["user_id"] = user["id"]
    request.session["session_token"] = session_token
    
    return {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "username": user["username"]
        }
    }
```

---

## Performance Optimization {#performance}

### Caching Strategies

```mermaid
graph TD
    A[Authentication Request] --> B{Cache Check}
    B -->|Hit| C[Return Cached Result]
    B -->|Miss| D[Validate Credentials]
    D --> E[Store in Cache]
    E --> F[Return Result]
    
    G[Cache Types] --> H[Memory Cache]
    G --> I[Redis Cache]
    G --> J[Database Cache]
    
    style A fill:#e1f5fe
    style C fill:#e8f5e8
    style F fill:#e8f5e8
```

### Authentication Performance Implementation

```python
import asyncio
from functools import lru_cache
import aioredis
from fastapi import FastAPI

app = FastAPI()

class AuthCache:
    def __init__(self):
        self.redis = None
    
    async def init_redis(self):
        self.redis = await aioredis.from_url("redis://localhost")
    
    async def get_user_cache(self, user_id: str):
        if self.redis:
            cached = await self.redis.get(f"user:{user_id}")
            if cached:
                return json.loads(cached)
        return None
    
    async def set_user_cache(self, user_id: str, user_data: dict, ttl: int = 300):
        if self.redis:
            await self.redis.setex(
                f"user:{user_id}",
                ttl,
                json.dumps(user_data)
            )

auth_cache = AuthCache()

@app.on_event("startup")
async def startup():
    await auth_cache.init_redis()

# Memory caching for frequently accessed data
@lru_cache(maxsize=1000)
def get_user_permissions(user_id: str):
    # Expensive database operation
    return calculate_user_permissions(user_id)

async def get_cached_user(user_id: str):
    # Try cache first
    cached_user = await auth_cache.get_user_cache(user_id)
    if cached_user:
        return cached_user
    
    # Fetch from database
    user = await fetch_user_from_db(user_id)
    if user:
        await auth_cache.set_user_cache(user_id, user)
    
    return user
```

---

## Monitoring and Logging {#monitoring}

### Authentication Event Logging

```python
import logging
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class AuthLogger:
    def __init__(self):
        self.logger = logging.getLogger("auth")
    
    def log_login_attempt(
        self, 
        username: str, 
        ip_address: str, 
        user_agent: str, 
        success: bool
    ):
        self.logger.info(
            f"Login attempt - User: {username}, IP: {ip_address}, "
            f"Success: {success}, UserAgent: {user_agent}"
        )
    
    def log_token_validation(self, token_id: str, success: bool, reason: Optional[str] = None):
        self.logger.info(
            f"Token validation - Token: {token_id}, Success: {success}, "
            f"Reason: {reason or 'Valid'}"
        )
    
    def log_permission_check(
        self, 
        user_id: str, 
        permission: str, 
        granted: bool
    ):
        self.logger.info(
            f"Permission check - User: {user_id}, Permission: {permission}, "
            f"Granted: {granted}"
        )

auth_logger = AuthLogger()

# Usage in authentication endpoints
@app.post("/login")
async def login_with_logging(
    request: Request, 
    username: str, 
    password: str
):
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    
    try:
        user = authenticate_user(username, password)
        if user:
            auth_logger.log_login_attempt(username, client_ip, user_agent, True)
            return {"message": "Login successful"}
        else:
            auth_logger.log_login_attempt(username, client_ip, user_agent, False)
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    except Exception as e:
        auth_logger.log_login_attempt(username, client_ip, user_agent, False)
        raise
```

---

## Testing Authentication Systems {#testing}

### Comprehensive Test Suite

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def valid_token():
    return "valid-test-token"

class TestAuthentication:
    def test_login_success(self, test_client):
        response = test_client.post(
            "/login",
            data={"username": "testuser", "password": "testpass"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_invalid_credentials(self, test_client):
        response = test_client.post(
            "/login",
            data={"username": "invalid", "password": "wrong"}
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_protected_route_with_token(self, test_client, valid_token):
        response = test_client.get(
            "/protected",
            headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response.status_code == 200
    
    def test_protected_route_without_token(self, test_client):
        response = test_client.get("/protected")
        assert response.status_code == 401
    
    @patch('your_app.rate_limiter.is_allowed')
    def test_rate_limiting(self, mock_rate_limiter, test_client):
        mock_rate_limiter.return_value = False
        
        response = test_client.post(
            "/login",
            data={"username": "testuser", "password": "testpass"}
        )
        assert response.status_code == 429

class TestJWTToken:
    def test_jwt_creation(self):
        payload = {"sub": "testuser", "roles": ["user"]}
        token = JWTManager.create_access_token(payload)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_jwt_validation_valid_token(self):
        payload = {"sub": "testuser"}
        token = JWTManager.create_access_token(payload)
        decoded = JWTManager.verify_token(token)
        
        assert decoded["sub"] == "testuser"
    
    def test_jwt_validation_expired_token(self):
        with patch('jwt.decode', side_effect=jwt.ExpiredSignatureError):
            with pytest.raises(HTTPException) as exc_info:
                JWTManager.verify_token("expired-token")
            assert exc_info.value.status_code == 401

class TestRBAC:
    def test_admin_access(self, test_client):
        # Mock admin user
        with patch('your_app.get_current_user', return_value={
            "username": "admin",
            "roles": ["admin"]
        }):
            response = test_client.get(
                "/admin/users",
                headers={"Authorization": "Bearer admin-token"}
            )
            assert response.status_code == 200
    
    def test_insufficient_permissions(self, test_client):
        with patch('your_app.get_current_user', return_value={
            "username": "user",
            "roles": ["viewer"]
        }):
            response = test_client.delete(
                "/admin/users/1",
                headers={"Authorization": "Bearer user-token"}
            )
            assert response.status_code == 403
```

---

## Conclusion

FastAPI provides a robust and flexible authentication system that supports multiple authentication methods, from simple API keys to complex OAuth 2.0 flows. The key principles for implementing secure authentication include:

1. **Defense in Depth**: Multiple layers of security
2. **Principle of Least Privilege**: Users get minimal necessary permissions
3. **Secure by Design**: Security built into the architecture
4. **Regular Security Audits**: Continuous monitoring and improvement
5. **Performance Optimization**: Efficient caching and validation

### Key Takeaways

- **Choose the right authentication method** based on your use case
- **Implement proper error handling** and logging
- **Use strong cryptographic practices** for tokens and passwords
- **Apply rate limiting** to prevent abuse
- **Test thoroughly** including security edge cases
- **Monitor and log** all authentication events
- **Keep dependencies updated** for security patches

This comprehensive guide provides the foundation for implementing secure, scalable authentication systems in FastAPI. By understanding and applying these concepts, developers can protect their applications and users from unauthorized access and potential security threats.
