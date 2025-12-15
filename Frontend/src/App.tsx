// import Loginpage from "./pages/loginpage"
import ChatPage from "./pages/chatpage"
import { Provider } from "@/components/ui/provider"

import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// import ProtectedRoute from "./pages/auth/ProtectedRoute";
function App() {
  return (
    <Provider>
      <Router>
        <Routes>
          <Route path="/chat" element={<ChatPage />} />
          <Route path="*" element={<Navigate to="/chat" />} />
        </Routes>
      </Router>
    </Provider>
  );
}


export default App;
