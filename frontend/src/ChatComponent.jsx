import React, { useState, useEffect, useRef } from "react";
import "./ChatComponent.css";

const ChatComponent = () => {
  const [name, setName] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [step, setStep] = useState("name");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleNameSubmit = () => {
    if (name.trim()) {
      setMessages([
        { text: `¡Hola ${name}! ¿Qué tipo de película o serie buscas hoy? 🎬`, sender: "bot" }
      ]);
      setStep("description");
    }
  };

  const handleDescriptionSubmit = async () => {
    if (input.trim()) {
      const formattedInput = `- ${input}`; // Agrega el guion al inicio
      const newMessages = [...messages, { text: formattedInput, sender: "user" }];
      setMessages(newMessages);
      setInput("");

      let botResponse = { text: "No tengo recomendaciones, pero intenta de nuevo.", sender: "bot" };
      try {
        const response = await fetch("http://localhost:5000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: input }),
        });
        const result = await response.json();
        botResponse = { text: result.recomendaciones, sender: "bot" };
      } catch (error) {
        console.error("Error al realizar la petición:", error);
      }

      setMessages([
        ...newMessages,
        { text: `Gracias, ${name}. Déjame pensar... 🤔`, sender: "bot" },
        botResponse
      ]);
    }
  };

  // Estilo personalizado del mensaje del usuario
  const userStyle = {
    backgroundColor: "#0a0a0a",           // Negro profundo
    color: "#ffffff",                     // Texto blanco
    border: "2px solid #00fff7",          // Aqua fluorescente
    boxShadow: "0 0 12px #00fff766",      // Resplandor suave
    alignSelf: "flex-end",
    borderRadius: "20px",
    borderBottomRightRadius: "0",
    padding: "10px 15px",
    maxWidth: "80%",
    margin: "8px 0",
    lineHeight: "1.4",
    wordWrap: "break-word",
    textAlign: "left",
    fontFamily: "monospace",              // Le da un look más tech
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
              <div
                key={index}
                className={`chat-message ${msg.sender}`}
                style={msg.sender === "user" ? userStyle : undefined}
              >
                {msg.sender === "bot" && msg.text.includes("Te recomendamos las siguientes películas/shows:") && (
                  <p>Te recomendamos las siguientes películas/shows:</p>
                )}
                {msg.sender === "bot" ? (
                  <ul>
                    {msg.text.split("\n").map((line, i) => {
                      if (line.trim() === "------------------------------------------------------------------------------------------") {
                        return <React.Fragment key={i}>{line}</React.Fragment>;
                      }
                      return (
                        line.trim() &&
                        line !== "Te recomendamos las siguientes películas/shows:" && (
                          <li key={i}>
                            {line.includes("https") ? (
                              <>
                                <strong>{line.split(":")[0]}:</strong>{" "}
                                <a
                                  href={line.split(":").slice(1).join(":").trim()}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                >
                                  {line.split(":").slice(1).join(":").trim()}
                                </a>
                              </>
                            ) : (
                              <>
                                {line.includes(":") ? (
                                  <>
                                    <strong>{line.split(":")[0]}:</strong>{" "}
                                    {line.split(":").slice(1).join(":").trim()}
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
                ) : (
                  <p>{msg.text}</p>
                )}
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          <div className="container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ejemplo: Quiero ver una película futurista con mucha acción"
              onKeyDown={(e) => e.key === "Enter" && handleDescriptionSubmit()}
            />
            <button onClick={handleDescriptionSubmit}>Obtener Recomendación</button>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatComponent;
