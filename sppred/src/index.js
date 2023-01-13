import React, {useState} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';


function StockSelector() {
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

export default StockSelector;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App>
      <StockSelector />
      </App>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
