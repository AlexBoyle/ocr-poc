import ChatbotConfigTable from "../Components/ChatbotConfigTable";
import React, { useState, useEffect, useCallback } from "react";
import Request from "../Utils/Request";
import ENDPOINTS from "../Utils/EndpointMaster";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import Box from "@mui/material/Box";
import Select from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
function ChatbotConfigurationPage() {
  const [data, setData] = useState([]);
  const [connection, setConnection] = useState("");
  const params = useParams();
  useEffect(() => {
    if (params.id != "new") {
      let url = ENDPOINTS.GET_CHATBOT_CONFIG;
      url = url.replace(":id", params.id);
      Request.get(
        url,
        (res) => {
          console.log(res.data);
          setData(res.data);
        },
        (err) => {
          setData([]);
          console.log(err);
        }
      );
    }
  }, []);
  return (
    <>
      <h1>EditPage</h1>
      <div>
        <Link to={"/chat-config"}>
          <Button variant="contained" color="error" className="actionButton">
            Back
          </Button>
        </Link>
      </div>
      <div
        style={{
          width: "500px",
          textAlign: "left",
          margin: "auto",
          marginTop: "20px"
        }}
      >
        <FormControl
          style={{
            width: "100%",
          }}
        >
          <Container>
            <Row>
              <Col md="5">
                <FormControl style={{width: "100%"}}>
                  <InputLabel id="ConnectionTypeLabel">
                    ConnectionType
                  </InputLabel>
                  <Select
                    labelId="ConnectionTypeLabel"
                    value={connection}
                    label="ConnectionType"
                    onChange={(chg) => {
                      setConnection(chg.target.value);
                    }}
                  >
                    <MenuItem value={"Slack"}>Slack</MenuItem>
                    <MenuItem value={"Teams"}>Teams</MenuItem>
                    <MenuItem value={"SMS"}>SMS</MenuItem>
                    <MenuItem value={"Cisco"}>Cisco</MenuItem>
                    <MenuItem value={"Web"}>Web</MenuItem>
                  </Select>
                </FormControl>
              </Col>
              <Col md="7">
                <TextField
                style={{ width: "100%"}}
                  required
                  id="outlined-required"
                  label="Connection Name"
                  defaultValue=""
                />
              </Col>
            </Row>
            <Row style={{marginTop: "10px"}}>
                <Col md="12">
                    <TextField
                    style={{ width: "100%"}}
                                      required
                                      id="outlined-required"
                                      label="Connection"
                                      defaultValue=""
                                    />
                </Col>
            </Row>
            <Row>
             <Col style={{display: "flex", justifyContent: "right"}}>
                    <Button variant="contained" color="success" className="actionButton">
                      Update
                    </Button>
                  </Col>
            </Row>
          </Container>
        </FormControl>
      </div>

    </>
  );
}

export default ChatbotConfigurationPage;
