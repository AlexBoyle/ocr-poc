import React from "react";
import ServerStatus from "../Components/Stats/ServerStatus";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";
function DashboardPage() {
  console.log(process.env);
  const data = [
    { date: "12/01", num: 345 },
    { date: "12/02", num: 274 },
    { date: "12/03", num: 532 },
    { date: "12/04", num: 465 },
    { date: "12/05", num: 492 },
    { date: "12/06", num: 134 },
    { date: "12/07", num: 363 },
    { date: "12/08", num: 745 },
    { date: "12/09", num: 345 },
    { date: "12/10", num: 655 },
    { date: "12/11", num: 435 },
    { date: "12/12", num: 666 },
  ];

  return (
    <div style={{ height: "100%" }}>
      <h1>Welcome </h1>
      <ServerStatus />
      <div>
        <Container>
          <Row>
            <Col sm="12" md="6">
              <LineChart width={400} height={400} data={data}>
                <Line type="monotone" dataKey="num" stroke="#8884d8" />
                <CartesianGrid stroke="#ccc" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
              </LineChart>
            </Col>
            <Col sm="12" md="6">
              <LineChart width={400} height={400} data={data}>
                <Line type="monotone" dataKey="uv" stroke="#8884d8" />
              </LineChart>
            </Col>
          </Row>
        </Container>
      </div>
    </div>
  );
}

export default DashboardPage;
