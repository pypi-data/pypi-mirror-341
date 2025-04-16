# fastapi-jsend

A lightweight FastAPI extension to return responses in [JSend](https://github.com/omniti-labs/jsend) format.

## 🚀 Install

```bash
pip install fastapi-jsend
```

## 📦 Usage

`fastapi-jsend` helps you build clean, consistent API responses using the JSend specification. It simplifies success, fail, and error responses by providing utility functions and a base response class for FastAPI.

---

### 🔧 Basic Setup

Set `JSendResponse` as the default response class for your FastAPI app:

```python
from fastapi import FastAPI
from fastapi_jsend import JSendResponse, jsend_success, jsend_fail, jsend_error

app = FastAPI(default_response_class=JSendResponse)

@app.get("/ping")
async def ping():
    return jsend_success(data={"message": "pong"})
```

---

### ✅ Success Response

Use `jsend_success(data)` to return a successful response with payload:

```python
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    user = {"id": user_id, "name": "John Doe"}
    return jsend_success(data=user)
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "John Doe"
  }
}
```

---

### ⚠️ Fail Response

Use `jsend_fail(data)` for failed operations due to user input, validation, or missing data:

```python
@app.get("/validate-age/{age}")
async def validate_age(age: int):
    if age < 18:
        return jsend_fail(data={"error": "User must be at least 18 years old"})
    return jsend_success(data={"age": age})
```

**Response:**

```json
{
  "status": "fail",
  "data": {
    "error": "User must be at least 18 years old"
  }
}
```

---

### ❌ Error Response

Use `jsend_error(message, code=None, data=None)` for internal or unexpected errors:

```python
@app.get("/error-demo")
async def error_demo():
    try:
        raise ValueError("Something went wrong")
    except Exception as e:
        return jsend_error(message=str(e))
```

**Response:**

```json
{
  "status": "error",
  "message": "Something went wrong"
}
```

---

## 🔍 About JSend

[JSend](https://github.com/omniti-labs/jsend) is a specification that standardizes how JSON responses are formatted:

- **success**: The request was successful and the response contains data.
- **fail**: The request was valid but failed due to a known issue (e.g., validation).
- **error**: An unexpected issue occurred during request processing.

Using this format ensures your APIs are predictable, consistent, and easy to consume on the frontend.

---

## 💡 Tips

- You can override the response format per endpoint using `response_class=JSendResponse`.
- Works seamlessly with FastAPI dependencies, middlewares, and routers.
- Combine with FastAPI response models for even stronger type guarantees.
