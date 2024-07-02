# vite_vue_prompt_7.md

## prompt
As a seasoned programmer, fix this react code using axios to avoid the error `Access to XMLHttpRequest at 'http://localhost:8000/todos' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.`


```js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({name: "", due_date: "", description: ""});

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = () => {
    axios.get('http://localhost:8000/todos')
      .then(response => {
        setTodos(response.data);
      });
  }

  const addTodo = () => {
    axios.post('http://localhost:8000/todos', newTodo)
      .then(() => {
        fetchTodos();
        setNewTodo({name: "", due_date: "", description: ""});
      });
  }

  const deleteTodo = (todoId) => {
    axios.delete(`http://localhost:8000/todos/${todoId}`)
      .then(() => {
        fetchTodos();
      });
  }

  return (
    <div className="App">
      {/* Display form to add new todo */}
      <div>
        <h2>Add a New Todo</h2>
        <input
          type="text"
          placeholder="Name"
          value={newTodo.name}
          onChange={e => setNewTodo({ ...newTodo, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Due Date"
          value={newTodo.due_date}
          onChange={e => setNewTodo({ ...newTodo, due_date: e.target.value })}
        />
        <textarea
          placeholder="Description"
          value={newTodo.description}
          onChange={e => setNewTodo({ ...newTodo, description: e.target.value })}
        />
        <button onClick={addTodo}>Add Todo</button>
      </div>

      {/* Display list of todos */}
      <div>
        <h2>Your Todos</h2>
        {todos.map((todo, index) => (
          <div key={index}>
            <h3>{todo.name}</h3>
            <p>Due: {todo.due_date}</p>
            <p>{todo.description}</p>
            <button onClick={() => deleteTodo(index)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

```

## ChatGPT



