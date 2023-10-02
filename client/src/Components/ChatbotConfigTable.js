import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "@mui/material/Button";
import "./ChatbotConfigTable.css";
import React, { useState, useEffect, useCallback } from "react";
import Request from "../Utils/Request";
import ENDPOINTS from "../Utils/EndpointMaster";
import { Link } from "react-router-dom";
function ChatbotConfigTable() {
  const [data, setData] = useState([]);
  useEffect(() => {
    Request.get(
      ENDPOINTS.GET_CHATBOT_CONFIGS,
      (res) => {
        console.log(res.data);
        setData(res.data);
      },
      (err) => {
        setData([]);
        console.log(err);
      }
    );
  }, []);
  return (
    <div className="pageContainer">
      <div>
        <div style={{ maxWidth: "100%", textAlign: "left" }}></div>
        <div className="entryContainer">
          <Container
            style={{
              maxWidth: "calc( 100% - 18px)",
              textAlign: "left",
              margin: "0px",
            }}
          >
            <Row className="rowElement">
              <Col md="2" className="textRowElement">
                Name
              </Col>
              <Col md="2" className="textRowElement">
                Connection Type
              </Col>
              <Col md="2" className="textRowElement">
                Status
              </Col>
              <Col md className="primaryActionButtonContainer">
                Actions
              </Col>
            </Row>
          </Container>
          <Container
            style={{
              maxWidth: "100%",
              textAlign: "left",
              maxHeight: "calc( 100vh - 300px )",
              height: "calc( 100vh - 300px )",
              overflowY: "scroll",
            }}
          >
            {data.map((obj) => {
              return (
                <Row className="rowElement">
                  <Col md="2" className="textRowElement">
                    {obj.name}
                  </Col>
                  <Col md="2" className="textRowElement">
                    {obj.type}
                  </Col>
                  <Col md="2" className="textRowElement">
                    {obj.status}
                  </Col>
                  <Col md className="primaryActionButtonContainer">
                    <Button
                      variant="contained"
                      color="error"
                      className="actionButton"
                    >
                      delete
                    </Button>
                    <Link to={"/chat-config/" + obj.id}>
                      <Button
                        variant="contained"
                        color="success"
                        className="actionButton"
                      >
                        Edit
                      </Button>
                    </Link>
                  </Col>
                </Row>
              );
            })}
          </Container>
        </div>
      </div>
    </div>
  );
}

export default ChatbotConfigTable;
