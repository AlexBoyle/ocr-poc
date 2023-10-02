import logo from "./logo.svg";
import "./App.css";
import PageMaster from "./Pages/PageMaster";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./Components/Layout.js";
import "bootstrap/dist/css/bootstrap.min.css";
function App() {
  return (
    <div className="App">
      <Router>
        <Layout>
          <Routes>
            {Object.values(PageMaster.pageMetadata).map((d) => {
              return <Route key={d.url} path={d.url} exact element={d.page} />;
            })}
          </Routes>
        </Layout>
      </Router>
    </div>
  );
}

export default App;
