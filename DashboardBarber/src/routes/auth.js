import express from "express";
import jwt from "jsonwebtoken";


const router = express.Router();


// Login do dono (usuário/senha em variáveis de ambiente)
router.post("/login", (req, res) => {
const { email, username, password } = req.body;
const loginField = email || username; // Aceita tanto email quanto username
console.log("Login attempt:", { loginField, password });
console.log("Expected:", { 
  user: process.env.ADMIN_USER, 
  password: process.env.ADMIN_PASS 
});
if (
loginField === process.env.ADMIN_USER &&
password === process.env.ADMIN_PASS
) {
const token = jwt.sign({ role: "admin", username: loginField }, process.env.JWT_SECRET, {
expiresIn: "8h",
});
const user = {
id: "1",
email: loginField,
nome: "Sr. Mendes"
};
return res.json({ token, user });
}
res.status(401).json({ message: "Credenciais inválidas" });
});


export default router;