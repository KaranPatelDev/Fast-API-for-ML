# 🌐 CURL and API Configurations

## 📡 Understanding CURL

### Conceptual Foundation

CURL (Client URL) is a command-line tool and library for transferring data with URLs. It supports numerous protocols including HTTP, HTTPS, FTP, and many others. In the context of FastAPI development, CURL serves as a universal API testing tool that provides precise control over HTTP requests without the need for graphical interfaces or specialized software.

The power of CURL lies in its **ubiquity** and **scriptability**. It's available on virtually every operating system and can be easily integrated into scripts, CI/CD pipelines, and automated testing workflows. Unlike GUI-based tools, CURL commands are easily shareable, version-controllable, and reproducible across different environments.

### Theoretical Framework

**Request-Response Cycle Understanding:**
CURL operates within the standard HTTP request-response paradigm, where:
1. **Client (CURL)** constructs and sends HTTP requests
2. **Server (FastAPI)** processes requests and generates responses  
3. **Response** is returned and displayed by CURL

**Protocol Abstraction:**
CURL abstracts the underlying network protocols, allowing developers to focus on the application layer while handling:
- Connection establishment and teardown
- SSL/TLS encryption and certificate validation
- Authentication mechanisms
- Cookie management
- Redirect handling

## 🔧 CURL Syntax and Components

### Basic Syntax Structure

Based on the provided image, the fundamental CURL syntax follows this pattern:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": [1, 2, 3]}'
```

**Component Breakdown:**

**1. HTTP Method Specification (`-X POST`)**
- **Purpose**: Explicitly defines the HTTP method to use
- **Theory**: HTTP methods define the semantic meaning of the request
- **Common Methods**:
  - `GET`: Retrieve data (default method)
  - `POST`: Create new resources or submit data
  - `PUT`: Update/replace existing resources
  - `PATCH`: Partially update resources
  - `DELETE`: Remove resources

```bash
# GET request (default, -X GET is optional)
curl "http://localhost:8000/users"

# POST request for creating data
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "email": "john@example.com"}'

# PUT request for full updates
curl -X PUT "http://localhost:8000/users/123" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Smith", "email": "john.smith@example.com"}'

# DELETE request
curl -X DELETE "http://localhost:8000/users/123"
```

**2. Header Specification (`-H`)**
- **Purpose**: Adds HTTP headers to customize request behavior
- **Theory**: Headers provide metadata about the request/response
- **Common Headers**:

```bash
# Content-Type: Specifies request body format
curl -H "Content-Type: application/json"

# Authorization: Authentication credentials
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

# Accept: Preferred response format
curl -H "Accept: application/json"

# User-Agent: Client identification
curl -H "User-Agent: MyApp/1.0"

# Custom headers
curl -H "X-API-Key: your-api-key-here" \
     -H "X-Request-ID: req-123456"
```

**3. Data Specification (`-d`)**
- **Purpose**: Sends request body data
- **Theory**: Payload containing information to be processed by the server
- **Data Formats**:

```bash
# JSON data (most common for APIs)
curl -d '{"name": "John", "age": 30}'

# Form data
curl -d "name=John&age=30"

# File contents
curl -d @data.json

# Raw string data
curl -d "plain text data"
```

## 🏗️ Advanced CURL Techniques

### Authentication Patterns

**Bearer Token Authentication:**
```bash
# JWT token authentication
curl -X GET "http://localhost:8000/protected" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Basic Authentication:**
```bash
# Username/password authentication
curl -u "username:password" "http://localhost:8000/admin"

# Alternative syntax
curl -H "Authorization: Basic $(echo -n 'username:password' | base64)" \
     "http://localhost:8000/admin"
```

**API Key Authentication:**
```bash
# Header-based API key
curl -H "X-API-Key: your-secret-key" "http://localhost:8000/api/data"

# Query parameter API key
curl "http://localhost:8000/api/data?api_key=your-secret-key"
```

### Response Handling and Debugging

**Verbose Output (`-v`):**
```bash
# Show detailed request/response information
curl -v -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"features": [1, 2, 3]}'
```

**Response Headers Only (`-I`):**
```bash
# HEAD request - headers only
curl -I "http://localhost:8000/health"
```

**Save Response to File (`-o`):**
```bash
# Save response body to file
curl "http://localhost:8000/export/data" -o data.json

# Save with original filename
curl -O "http://localhost:8000/files/report.pdf"
```

**Follow Redirects (`-L`):**
```bash
# Automatically follow HTTP redirects
curl -L "http://localhost:8000/redirect-endpoint"
```

### Performance and Timeout Configuration

**Timeout Settings:**
```bash
# Connection timeout (seconds)
curl --connect-timeout 5 "http://localhost:8000/api"

# Maximum time for entire operation
curl --max-time 30 "http://localhost:8000/slow-endpoint"

# Keep-alive timeout
curl --keepalive-time 60 "http://localhost:8000/api"
```

**Retry Configuration:**
```bash
# Retry failed requests
curl --retry 3 --retry-delay 2 "http://localhost:8000/unreliable-endpoint"

# Retry only on specific conditions
curl --retry 3 --retry-connrefused "http://localhost:8000/api"
```

## 📊 Testing Strategies with CURL

### Data-Driven Testing

**Parameterized Requests:**
```bash
# Using variables for dynamic testing
API_BASE="http://localhost:8000"
USER_ID="123"
AUTH_TOKEN="Bearer eyJhbGciOiJIUzI1NiIs..."

curl -X GET "${API_BASE}/users/${USER_ID}" \
     -H "Authorization: ${AUTH_TOKEN}"
```

**Batch Testing with Scripts:**
```bash
#!/bin/bash
# test_api_endpoints.sh

declare -a endpoints=(
    "GET /health"
    "GET /users"
    "POST /users"
    "GET /users/123"
)

for endpoint in "${endpoints[@]}"; do
    method=$(echo $endpoint | cut -d' ' -f1)
    path=$(echo $endpoint | cut -d' ' -f2)
    
    echo "Testing $method $path"
    curl -X $method "http://localhost:8000$path" \
         -H "Content-Type: application/json" \
         -w "Status: %{http_code}, Time: %{time_total}s\n"
done
```

### Response Validation

**JSON Response Parsing with jq:**
```bash
# Extract specific fields from JSON response
curl "http://localhost:8000/users/123" | jq '.name'

# Validate response structure
curl "http://localhost:8000/users" | jq 'type == "array"'

# Complex filtering
curl "http://localhost:8000/users" | jq '.[] | select(.age > 25)'
```

**HTTP Status Code Checking:**
```bash
# Get only the status code
status_code=$(curl -o /dev/null -s -w "%{http_code}" "http://localhost:8000/api")

if [ $status_code -eq 200 ]; then
    echo "API is healthy"
else
    echo "API returned status: $status_code"
fi
```

## ⚙️ Development Configuration Patterns

### Environment-Specific Configurations

**Configuration Management:**
```bash
# Development environment
export API_BASE_URL="http://localhost:8000"
export API_KEY="dev-key-12345"
export DEBUG_MODE="true"

# Staging environment
export API_BASE_URL="https://staging.api.example.com"
export API_KEY="staging-key-67890"
export DEBUG_MODE="false"

# Production environment
export API_BASE_URL="https://api.example.com"
export API_KEY="prod-key-abcdef"
export DEBUG_MODE="false"
```

**Configuration Files:**
```bash
# .env file loading in shell scripts
if [ -f .env ]; then
    source .env
fi

curl -X POST "${API_BASE_URL}/predict" \
     -H "Authorization: Bearer ${API_TOKEN}" \
     -H "Content-Type: application/json" \
     -d @prediction_data.json
```

### Development Workflow Integration

**API Development Testing:**
```bash
# Development server testing
dev_test() {
    echo "Testing development server..."
    curl -f "http://localhost:8000/health" || {
        echo "Development server not responding"
        return 1
    }
    
    echo "Running API tests..."
    curl -X POST "http://localhost:8000/test-endpoint" \
         -H "Content-Type: application/json" \
         -d '{"test": true}' \
         --fail || return 1
    
    echo "All tests passed!"
}
```

**Pre-deployment Validation:**
```bash
# Validate API before deployment
validate_api() {
    local base_url=$1
    local auth_token=$2
    
    # Health check
    health_status=$(curl -s -o /dev/null -w "%{http_code}" "${base_url}/health")
    if [ $health_status -ne 200 ]; then
        echo "Health check failed: $health_status"
        return 1
    fi
    
    # Authentication test
    auth_status=$(curl -s -o /dev/null -w "%{http_code}" \
                      -H "Authorization: Bearer $auth_token" \
                      "${base_url}/protected")
    if [ $auth_status -ne 200 ]; then
        echo "Authentication test failed: $auth_status"
        return 1
    fi
    
    echo "API validation successful"
}
```

## 🔄 Configuration Management

### FastAPI Configuration Integration

**Settings-Based Configuration:**
```python
# settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug_mode: bool = False
    database_url: str
    redis_url: str
    jwt_secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**Corresponding CURL Tests:**
```bash
# Test different configuration scenarios

# Local development
curl "http://localhost:8000/config" | jq '.environment'

# Docker container
curl "http://0.0.0.0:8000/config" | jq '.environment'

# Production with environment variables
API_HOST=${API_HOST:-localhost}
API_PORT=${API_PORT:-8000}
curl "http://${API_HOST}:${API_PORT}/config"
```

### Dynamic Configuration Testing

**Feature Flag Testing:**
```bash
# Test feature flags with different configurations
test_feature_flags() {
    local base_url=$1
    
    # Test with feature enabled
    curl -X POST "${base_url}/api/test" \
         -H "X-Feature-Flag: new-feature:enabled" \
         -H "Content-Type: application/json" \
         -d '{"test_data": "enabled"}'
    
    # Test with feature disabled
    curl -X POST "${base_url}/api/test" \
         -H "X-Feature-Flag: new-feature:disabled" \
         -H "Content-Type: application/json" \
         -d '{"test_data": "disabled"}'
}
```

**A/B Testing Configuration:**
```bash
# Test different API versions
test_api_versions() {
    local base_url=$1
    
    # Version 1
    curl "${base_url}/api/v1/users" \
         -H "Accept: application/json" \
         -w "Version 1 - Status: %{http_code}, Time: %{time_total}s\n"
    
    # Version 2
    curl "${base_url}/api/v2/users" \
         -H "Accept: application/json" \
         -w "Version 2 - Status: %{http_code}, Time: %{time_total}s\n"
}
```

## 🛡️ Security and Best Practices

### Secure CURL Usage

**Credential Management:**
```bash
# Never put credentials directly in commands
# BAD: curl -u "user:password123" 

# GOOD: Use environment variables
curl -u "$API_USERNAME:$API_PASSWORD"

# GOOD: Use credential files with restricted permissions
curl -u @credentials.txt  # chmod 600 credentials.txt
```

**SSL/TLS Configuration:**
```bash
# Verify SSL certificates (default)
curl "https://api.example.com/secure"

# Skip certificate verification (only for development)
curl -k "https://localhost:8000/api"

# Use specific certificate
curl --cert client.pem --key client.key "https://api.example.com"

# Specify CA bundle
curl --cacert ca-bundle.crt "https://api.example.com"
```

### Production Considerations

**Rate Limiting Awareness:**
```bash
# Implement backoff strategies
make_request_with_backoff() {
    local url=$1
    local max_retries=5
    local delay=1
    
    for i in $(seq 1 $max_retries); do
        response=$(curl -s -w "%{http_code}" "$url")
        status_code=${response: -3}
        
        if [ $status_code -eq 429 ]; then
            echo "Rate limited, waiting ${delay}s..."
            sleep $delay
            delay=$((delay * 2))
        else
            echo "${response%???}"  # Remove status code from end
            break
        fi
    done
}
```

**Monitoring Integration:**
```bash
# Log CURL operations for monitoring
log_api_call() {
    local method=$1
    local url=$2
    local response_code=$3
    local response_time=$4
    
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) API_CALL method=$method url=$url status=$response_code time=${response_time}s" >> api_calls.log
}

# Enhanced CURL with logging
monitored_curl() {
    local start_time=$(date +%s.%N)
    local response=$(curl -w "%{http_code}" -s "$@")
    local end_time=$(date +%s.%N)
    
    local status_code=${response: -3}
    local response_body=${response%???}
    local response_time=$(echo "$end_time - $start_time" | bc)
    
    log_api_call "GET" "$1" "$status_code" "$response_time"
    echo "$response_body"
}
```

This comprehensive guide provides both theoretical understanding and practical implementation of CURL for FastAPI development, covering everything from basic syntax