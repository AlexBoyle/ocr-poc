import DashboardPage from "./DashboardPage";
import TestOcrPage from "./TestOcrPage";

import { FaHome, FaWrench, FaServer } from "react-icons/fa";
import { BiSolidBot } from "react-icons/bi";
import { BsServer } from "react-icons/bs";
function PageMaster() {
  this.pageMetadata = {
    Dashboard: {
      icon: <FaHome />,
      name: "Dashboard",
      page: <DashboardPage></DashboardPage>,
      url: "/",
      sidebar: true,
    },
    TestOcrPage: {
      icon: <BiSolidBot />,
      name: "TestOcrPage",
      page: <TestOcrPage></TestOcrPage>,
      url: "/chat-config",
      sidebar: true,
    },
  };
}

export default new PageMaster();
