import React, { useState } from "react";
import "./ChatComponent.css";

const ChatComponent = () => {
  const [name, setName] = useState(""); // Estado para el nombre
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [step, setStep] = useState("name"); // Controla en qué paso está el usuario

  const handleNameSubmit = () => {
    if (name.trim()) {
      setMessages([{ text: `¡Hola ${name}! ¿Qué tipo de película o serie buscas hoy? 🎬`, sender: "bot" }]);
      setStep("genre");
    }
  };

  const handleGenreSubmit = () => {
    if (input.trim()) {
      setMessages([...messages, { text: `Entendido, ${name}. ¿Puedes darme una breve descripción de lo que buscas?`, sender: "bot" }]);
      setStep("description");
      setInput(""); // Limpiar el input
    }
  };

  const handleDescriptionSubmit = () => {
    if (input.trim()) {
      const genre = messages[messages.length - 1].text; // Obtener género de la última entrada
      const botResponse = getRecommendation(genre, input);

      setMessages([...messages, { text: `Gracias, ${name}. Déjame pensar... 🤔`, sender: "bot" }, botResponse]);
      setStep("genre"); // Permite seguir pidiendo más recomendaciones
      setInput(""); // Limpiar el input
    }
  };

  const getRecommendation = (genre, desc) => {
    const recommendations = {
      "acción": `Si buscas algo ${desc}, te recomiendo 'John Wick' o 'Mad Max: Fury Road'.`,
      "ciencia ficción": `Como buscas algo ${desc}, podrías ver 'Interstellar' o 'Blade Runner 2049'.`,
      "terror": `Si quieres algo ${desc}, te recomiendo 'Hereditary' o 'El Conjuro'.`,
      "comedia": `Para algo ${desc}, 'Brooklyn Nine-Nine' o 'Superbad' serían ideales.`,
      "drama": `Si buscas ${desc}, 'Breaking Bad' o 'Forrest Gump' podrían gustarte.`,
      "anime": `Si quieres anime con ${desc}, prueba 'Attack on Titan' o 'Steins;Gate'.`,
    };
    return { text: recommendations[genre.toLowerCase()] || `No tengo recomendaciones exactas para ${genre}, pero intenta con otro género.`, sender: "bot" };
  };

  return (
    <div className="chat-container">
      {step === "name" ? (
        <div className="name-input-container">
          <h2>¡Bienvenido! 🎬</h2>
          <p>Por favor, ingresa tu nombre para comenzar:</p>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Escribe tu nombre..."
          />
          <button onClick={handleNameSubmit}>Iniciar Chat</button>
        </div>
      ) : (
        <>
          <div className="chat-box">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                step === "genre"
                  ? "Ejemplo: Acción, Terror, Comedia..."
                  : "Ejemplo: Quiero algo futurista y con mucha acción"
              }
            />
            <button
              onClick={step === "genre" ? handleGenreSubmit : handleDescriptionSubmit}
            >
              {step === "genre" ? "Siguiente" : "Obtener Recomendación"}
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatComponent;
