import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./screens/Login";
import Register from "./screens/Register";
import Profile from "./screens/Profile";
import SentimentAnalysis from "./screens/SentimentAnalysis";
import NewsAnalysis from "./screens/NewsAnalysis";
import Forecast from "./screens/Forecast";
import Nav from "./components/Nav";
import Index from "./screens/Index";
import Dashboard from "./screens/Dashboard";

function App() {
    return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Index />} />
				<Route path="/login" element={<Login />} />
				<Route path="/register" element={<Register />} />
				<Route path="/profile" element={<Profile />} />
				<Route path="/sentiment-analysis" element={<SentimentAnalysis />} />
				<Route path="/news-analysis" element={<NewsAnalysis />} />
				<Route path="/forecast" element={<Forecast />} />
				<Route path="/dashboard" element={<Dashboard />} />
				<Route path="/nav" element={<Nav />} />
			</Routes>
		</BrowserRouter>
    );
}

export default App;
