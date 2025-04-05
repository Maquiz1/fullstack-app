import React, { useState } from 'react';
import axios from 'axios';

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async e => {
    e.preventDefault();
    const res = await axios.post('http://localhost:8000/api/token/', {
      username, password
    });
    const token = res.data.access;
    setToken(token);
    localStorage.setItem('token', token);
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="text" onChange={e => setUsername(e.target.value)} placeholder="Username" />
      <input type="password" onChange={e => setPassword(e.target.value)} placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
