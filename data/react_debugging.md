---
topic: React Debugging
framework: React
difficulty: Intermediate
---

# React Debugging Guide

## Common React Errors and Solutions

### Hydration Errors

**What is hydration?**
Hydration is the process where React attaches event listeners to the server-rendered HTML in the browser.

**Common causes:**
1. Mismatch between server and client rendering
2. Using browser-only APIs during SSR
3. Inconsistent data between server and client
4. Conditional rendering based on client-side state

**How to fix:**

```jsx
// ❌ Bad: Using window during SSR
function MyComponent() {
  const width = window.innerWidth; // Error in SSR
  return <div>Width: {width}</div>;
}

// ✅ Good: Check if window exists
function MyComponent() {
  const [width, setWidth] = useState(0);
  
  useEffect(() => {
    setWidth(window.innerWidth);
  }, []);
  
  return <div>Width: {width}</div>;
}
```

**Suppress hydration warning (use carefully):**
```jsx
<div suppressHydrationWarning={true}>
  {new Date().toLocaleDateString()}
</div>
```

### "Cannot read property of undefined"

This error occurs when trying to access a property on an undefined object.

**Common scenarios:**

```jsx
// ❌ Bad: No null check
function UserProfile({ user }) {
  return <div>{user.name}</div>; // Error if user is undefined
}

// ✅ Good: Optional chaining
function UserProfile({ user }) {
  return <div>{user?.name || "Guest"}</div>;
}

// ✅ Good: Early return
function UserProfile({ user }) {
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

### Infinite Re-render Loop

**Causes:**
1. Setting state directly in render
2. Missing dependencies in useEffect
3. Creating new objects/arrays in render

**Solutions:**

```jsx
// ❌ Bad: Setting state in render
function Counter() {
  const [count, setCount] = useState(0);
  setCount(count + 1); // Infinite loop!
  return <div>{count}</div>;
}

// ✅ Good: Set state in event handler or useEffect
function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const timer = setTimeout(() => setCount(count + 1), 1000);
    return () => clearTimeout(timer);
  }, [count]);
  
  return <div>{count}</div>;
}
```

### "Too many re-renders" Error

**Common cause:** Setting state in render without condition

```jsx
// ❌ Bad
function MyComponent() {
  const [data, setData] = useState(null);
  
  if (!data) {
    setData(fetchData()); // Causes infinite loop
  }
  
  return <div>{data}</div>;
}

// ✅ Good
function MyComponent() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetchData().then(setData);
  }, []);
  
  return <div>{data}</div>;
}
```

### useEffect Cleanup Function

**Why cleanup is important:**
- Prevent memory leaks
- Cancel subscriptions
- Clear timers
- Abort fetch requests

```jsx
// ✅ Proper cleanup
function Timer() {
  const [seconds, setSeconds] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);
    
    // Cleanup function
    return () => clearInterval(interval);
  }, []);
  
  return <div>Seconds: {seconds}</div>;
}

// ✅ Cleanup with fetch
function UserData({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    let cancelled = false;
    
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        if (!cancelled) setUser(data);
      });
    
    return () => {
      cancelled = true;
    };
  }, [userId]);
  
  return <div>{user?.name}</div>;
}
```

### Key Prop Warnings

**Why keys matter:**
Keys help React identify which items have changed, added, or removed.

```jsx
// ❌ Bad: Using index as key
{items.map((item, index) => (
  <div key={index}>{item.name}</div>
))}

// ✅ Good: Using unique ID
{items.map(item => (
  <div key={item.id}>{item.name}</div>
))}
```

### State Not Updating Immediately

**Remember:** setState is asynchronous!

```jsx
// ❌ Bad: Expecting immediate update
function Counter() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(count + 1);
    console.log(count); // Still shows old value!
  };
  
  return <button onClick={handleClick}>{count}</button>;
}

// ✅ Good: Use functional update
function Counter() {
  const [count, setCount] = useState(0);
  
  const handleClick = () => {
    setCount(prevCount => {
      const newCount = prevCount + 1;
      console.log(newCount); // Shows new value
      return newCount;
    });
  };
  
  return <button onClick={handleClick}>{count}</button>;
}
```

## Debugging Tools

### React DevTools
- Inspect component hierarchy
- View props and state
- Profile performance
- Track component updates

### Console Debugging
```jsx
// Add strategic console.logs
useEffect(() => {
  console.log('Component mounted');
  console.log('Props:', props);
  console.log('State:', state);
}, []);
```

### Error Boundaries
```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}
```

## Best Practices

1. **Always add dependency arrays** to useEffect
2. **Use optional chaining** (?.) for nested properties
3. **Implement error boundaries** for production apps
4. **Clean up side effects** in useEffect
5. **Use React DevTools** for debugging
6. **Avoid setting state in render**
7. **Use unique keys** for list items
