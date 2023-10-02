import React from "react";
import ChatbotConfigTable from "../Components/ChatbotConfigTable";
import Button from "@mui/material/Button";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Link } from "react-router-dom";
function ChatbotConfigurationPage() {
  return (
    <>
      <h1>ChatbotConfigurationPage</h1>
      <Container
        style={{ maxWidth: "90%", textAlign: "left", marginLeft: "5%" }}
      >
        <Row>
          <Col md></Col>
          <Col md style={{ display: "contents", justifyContent: "right" }}>
            <Link to="/chat-config/new">
              <Button variant="contained" color="success">
                + Add New Config
              </Button>
            </Link>
          </Col>
        </Row>
      </Container>

      <ChatbotConfigTable />
    </>
  );
}

export default ChatbotConfigurationPage;
