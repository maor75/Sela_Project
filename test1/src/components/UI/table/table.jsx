import cl from './table.module.css'
import React, { useState, useEffect } from 'react';

function CustomerTable1({ FetchUrl }) {
  const [customers, setCustomers] = useState([]);
  const [editRowIndex, setEditRowIndex] = useState(null);
  const [editFormData, setEditFormData] = useState({});

  useEffect(() => {
    fetch(FetchUrl)
      .then(response => response.json())
      .then(data => setCustomers(data.table))
      .catch(error => console.error('Error fetching customers:', error));
  }, [FetchUrl]);

  const handleEditRow = (rowIndex) => {
    setEditRowIndex(rowIndex);
    setEditFormData(customers[rowIndex]);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setEditFormData({
      ...editFormData,
      [name]: value,
    });
  };

  const handleSubmitEdit = (rowIndex) => {
    fetch('http://localhost:8000/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(editFormData),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      const updatedCustomers = [...customers];
      updatedCustomers[rowIndex] = editFormData;
      setCustomers(updatedCustomers);
      setEditRowIndex(null);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  const handleDeleteRow = (rowIndex) => {
    const personToDelete = customers[rowIndex];

    fetch('http://localhost:8000/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(personToDelete),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      setCustomers(customers.filter((_, index) => index !== rowIndex));
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };
 
  return (
    <div>
      <table className={cl.container}>
        <thead>
          <tr>
            {customers.length > 0 && Object.keys(customers[0]).map(key => (
              <th key={key}>{key}</th>
            ))}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer, rowIndex) => (
            <tr key={rowIndex}>
              {Object.keys(customer).map((key) => (
                <td key={key}>
                  {editRowIndex === rowIndex ? (
                    <input
                      type="text"
                      name={key}
                      value={editFormData[key] || ''}
                      onChange={handleInputChange}
                    />
                  ) : (
                    customer[key]
                  )}
                </td>
              ))}
              <td>
                {editRowIndex === rowIndex ? (
                  <button onClick={() => handleSubmitEdit(rowIndex)}>Submit</button>
                ) : (
                  <>
                    <button onClick={() => handleEditRow(rowIndex)}>Edit</button>
                    <button onClick={() => handleDeleteRow(rowIndex)}>Delete</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CustomerTable1;
