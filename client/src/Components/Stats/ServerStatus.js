import Request from "../../Utils/Request";
import ENDPOINTS from "../../Utils/EndpointMaster";
import React, { useState, useEffect, useCallback } from "react";
import "./Stats.css";
function ServerStatus() {
  const [data, setData] = useState({
    msg: "Waiting for server response",
    status: "waiting",
  });
  useEffect(() => {
    Request.get(
      ENDPOINTS.GET_SERVER_STATUS,
      (res) => {
        setData(res.data);
        console.log(res);
      },
      (err) => {
        setData({ msg: "Failed to reach server", status: "failed" });
        console.log(err);
      }
    );
  }, []);

  return (
    <div
      className={
        data.status == "failed"
          ? "bgRed"
          : data.status == "connected"
          ? "bgGreen"
          : "bgYellow"
      }
    >
      {data.msg}
    </div>
  );
}

export default ServerStatus;
