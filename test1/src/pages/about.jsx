import React from "react";
import Table from "../components/UI/table/table";

const About = () => {
    const httpUrl = 'http://localhost:8000/customers';

    return (
        <div>
             <h1>Welcome To Providers Page</h1>
            <Table FetchUrl={httpUrl}></Table>
        </div>
    );
};
export default About;