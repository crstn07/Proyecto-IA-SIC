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
      setStep("description");
    }
  };

  const handleDescriptionSubmit = async () => {
    if (input.trim()) {
      let botResponse = { text: "No tengo recomendaciones, pero intenta de nuevo.", sender: "bot" };
      try {
        const response = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({query: input}),
        });
        const result = await response.json();
        console.log('Respuesta de la API:', result);
        botResponse = { text: result.recomendaciones, sender: "bot" };
      } catch (error) {
        console.error('Error al realizar la petición:', error);
      }

      setMessages([...messages, { text: `Gracias, ${name}. Déjame pensar... 🤔`, sender: "bot" }, botResponse]);
      setStep("description"); // Permite seguir pidiendo más recomendaciones
      setInput(""); // Limpiar el input
    }
  };

  return (
    <div className="chat-container">
      {step === "name" ? (
        <div className="container">
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
                {msg.text.includes("Te recomendamos las siguientes películas/shows:") && (
                  <p>Te recomendamos las siguientes películas/shows:</p> // Mostrar fuera del <ul>
                )}
                <ul>
                  {msg.text.split('\n').map((line, index) => {
                    if (line.trim() === "------------------------------------------------------------------------------------------") {
                      return (
                        <React.Fragment key={index}>
                          {line}
                        </React.Fragment>
                      );
                    }
                    return (
                      line.trim() &&
                      line !== "Te recomendamos las siguientes películas/shows:" && ( // Excluir del <ul>
                        <li key={index}>
                        {line.includes("https") ? (
                          <>
                            <strong>{line.split(':')[0]}:</strong>{' '}
                            <a href={line.includes("https") ? line.split(':').slice(1).join(':').trim() : ''} target="_blank" rel="noopener noreferrer">
                              {line.split(':').slice(1).join(':').trim()}
                            </a>
                          </>
                        ) : (
                          <>
                            {line.includes(':') ? (
                              <>
                                <strong>{line.split(':')[0]}:</strong>{' '}
                                {line.split(':').slice(1).join(':').trim()}
                              </>
                            ) : (
                              line
                            )}
                          </>
                        )}
                      </li>
                      )
                    );
                  })}
                </ul>
              </div>
            ))}
          </div>

          <div className="container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={"Ejemplo: Quiero ver una película futurista con mucha acción"}
            />
            <button
              onClick={handleDescriptionSubmit}
            >
              Obtener Recomendación
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatComponent;
