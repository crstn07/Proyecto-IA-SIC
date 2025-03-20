import express from "express";
import cors from "cors";

const app = express();
const port = 5500;

app.use(cors());

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Hello :D");
});

app.listen(port, () => {
  console.log(`Server is listening at http://localhost:${port}`);
});
