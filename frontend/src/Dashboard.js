import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard({ token, onLogout }) {
  const [wallet, setWallet] = useState({ balance: 0 });

  useEffect(() => {
    axios.get('http://localhost:8000/api/wallet/', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setWallet(res.data));
  }, [token]);

  return (
    <div>
      <h2>Wallet Balance: ${wallet.balance}</h2>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default Dashboard;
