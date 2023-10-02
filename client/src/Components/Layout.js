import "./Layout.css";
import React, { useState, useEffect, useCallback } from "react";
import PageMaster from "../Pages/PageMaster";
import { Link } from "react-router-dom";
import { FaBars } from "react-icons/fa";
function Layout(props) {
  const [isOpen, setIsOpen] = useState(false);
  let togglePanel = useCallback(
    function () {
      setIsOpen(!isOpen);
    },
    [isOpen, setIsOpen]
  );
  return (
    <>
      <header>
        <panelButton onClick={togglePanel}>
          <span className="icon">
            <FaBars />
          </span>
        </panelButton>
      </header>
      <panel className={isOpen ? "open" : ""}>
        {Object.values(PageMaster.pageMetadata).map((d) => {
          if (d.sidebar)
            return (
              <Link key={d.url} to={d.url}>
                <div className="panelRow">
                  <span className="icon">{d.icon}</span>
                  <span className="name">{d.name}</span>
                </div>
              </Link>
            );
        })}
      </panel>
      <content className={isOpen ? "mainOpen" : ""}>{props.children}</content>
    </>
  );
}

export default Layout;
