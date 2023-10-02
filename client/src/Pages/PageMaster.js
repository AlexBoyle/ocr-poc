import ChatbotConfigurationPage from "./ChatbotConfigurationPage";
import DashboardPage from "./DashboardPage";
import DataManagementPage from "./DataManagementPage";
import ServerManagementPage from "./ServerManagementPage";
import SupportPage from "./SupportPage";
import ChatbotConfigEditPage from "./ChatbotConfigEditPage";
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
    ChatbotConfiguration: {
      icon: <BiSolidBot />,
      name: "Chatbot Config",
      page: <ChatbotConfigurationPage></ChatbotConfigurationPage>,
      url: "/chat-config",
      sidebar: true,
    },
    DataManagement: {
      icon: <BsServer />,
      name: "Data Config",
      page: <DataManagementPage></DataManagementPage>,
      url: "/data-config",
      sidebar: true,
    },
    ServerManagement: {
      icon: <FaServer />,
      name: "Server Config",
      page: <ServerManagementPage></ServerManagementPage>,
      url: "/server-config",
      sidebar: true,
    },
    Test: {
      name: "Chatbot Edit Page",
      page: <ChatbotConfigEditPage></ChatbotConfigEditPage>,
      url: "/chat-config/:id",
      sidebar: false,
    },
  };
}

export default new PageMaster();
