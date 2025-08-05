import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FeatureList from "./pages/FeatureList";
import CreateFeature from "./pages/CreateFeature";
import EditFeature from "./pages/EditFeature";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<FeatureList />} />
          <Route path="/features/new" element={<CreateFeature />} />
          <Route path="/features/:id/edit" element={<EditFeature />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
