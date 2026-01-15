// src/main.tsx
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import { Layout } from "@/layout";
import "./index.css";
import HomePage from "./pages/Home";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import DashboardPage from "./pages/dashboard/Dashboard";
import GeneratePage from "./pages/dashboard/Generate";
import MyGuidesPage from "./pages/dashboard/MyGuides";
import GuideDetailsPage from "./pages/dashboard/Guide";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <Routes>
      <Route element={<Layout />}>
        <Route path="" element={<HomePage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="dashboard">
          <Route index element={<DashboardPage />}></Route>
          <Route path="generate" element={<GeneratePage />} />
          <Route path="my-guides" element={<MyGuidesPage />} />
          <Route path="my-guides/:id" element={<GuideDetailsPage />} />
        </Route>
        <Route path="*" element={<p>Não achei</p>} />
      </Route>
    </Routes>
  </BrowserRouter>,
);
