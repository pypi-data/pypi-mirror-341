# Streamlit State Manager

The Streamlit State Manager `StateManager` is essentially a wrapper around [Streamlit's](https://github.com/streamlit/streamlit) native `st.session_state` dictionary, that simplifies how you interact with it.

## Features

1. **Cleaner Code**: Reduces boilerplate for initialization and access
2. **Error Prevention**: Reduces common pitfalls like missing initialization

## Installation

```bash
pip install streamlit-state-manager
```

## Examples

### 1. Simplified Access Patterns

**Without StateManager:**

```python
# Check if exists, initialize, then get
if "counter" not in st.session_state:
    st.session_state["counter"] = 0
count = st.session_state["counter"]

# Updating value
st.session_state["counter"] += 1
```

**With StateManager:**

```python
# Get with auto-initialization
count = StateManager.get("counter", 0)

# Updating value
StateManager.set("counter", count + 1)
```

### 2. Prevention of Common Errors

**Without StateManager:**

```python
# Potential KeyError if key doesn't exist
value = st.session_state["maybe_missing_key"]

# Forgetting to check existence before using
st.session_state["counter"] += 1  # Error if counter doesn't exist
```

**With StateManager:**

```python
# Safe access with optional default
value = StateManager.get("maybe_missing_key", default_value=None)
```

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
