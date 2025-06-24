# Code Examples

Here are some programming examples that will be converted to video:

## Python Example

```python
def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    print("Fibonacci sequence:")
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

if __name__ == '__main__':
    main()
```

## JavaScript Example

```javascript
// Factorial function using recursion
const factorial = (n) => {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
};

// Array methods demonstration
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(x => x * 2);
const sum = numbers.reduce((acc, x) => acc + x, 0);

console.log(`Original: ${numbers}`);
console.log(`Doubled: ${doubled}`);
console.log(`Sum: ${sum}`);
console.log(`5! = ${factorial(5)}`);
```

## Shell Commands

```bash
#!/bin/bash

# Create a new directory
mkdir -p my_project
cd my_project

# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# List files with details
ls -la

echo "Project setup complete!"
```

## SQL Example

```sql
-- Create a users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email) VALUES
    ('alice', 'alice@example.com'),
    ('bob', 'bob@example.com'),
    ('charlie', 'charlie@example.com');

-- Query the data
SELECT username, email, created_at 
FROM users 
WHERE created_at > '2024-01-01'
ORDER BY username;
```
