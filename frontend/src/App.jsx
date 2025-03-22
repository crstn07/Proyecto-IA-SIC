import React from "react";
import ChatComponent from "./ChatComponent";
import { Film } from "lucide-react"; 
import "./App.css"; 

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <Film className="logo-icon" /> {}
        <h1 className="titulo-principal">CineBot 🎬</h1>
        <p className="subtitulo">"Tu guía personal para descubrir historias inolvidables."</p>
      </header>
        <ChatComponent />
    </div>
  );
}

export default App;
