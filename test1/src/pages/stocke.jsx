import React from "react";
import Table from "../components/UI/table/table";

const Stock = () => {
    const httpUrl = 'http://localhost:8000/product'; // Define the HTTP URL here

    return (
        <div>
            <h1>Welcome To Stok Page</h1>
            <Table FetchUrl={httpUrl}></Table>
        </div>
    );
};

export default Stock;
