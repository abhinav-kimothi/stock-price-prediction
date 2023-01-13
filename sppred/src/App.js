import logo from './logo.svg';
import './App.css';
import React, {useState} from 'react';

function App() {
  const [selectedStock, setSelectedStock] = useState('');

  const handleChange = (event) => {
      setSelectedStock(event.target.value);
  }

  return (      
      <div>
          <label>Select a stock:</label>
          <select value={selectedStock} onChange={handleChange}>
              <option value="AAPL">Apple</option>
              <option value="MSFT">Microsoft Corp.</option>
              <option value="AMZN">Amazon.com Inc.</option>
              <option value="TSLA">Tesla Inc.</option>
              <option value="GOOGL">Alphabet Inc.</option>
          </select>
      </div>
  );
  }

  export default App;