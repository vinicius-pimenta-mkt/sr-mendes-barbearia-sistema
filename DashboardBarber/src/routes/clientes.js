import express from "express";
import { authenticateToken, authenticateApiKey } from "../middleware/auth.js";


const router = express.Router();


// ↙️ Criação via n8n (SEM login; protegido por X-API-KEY)
router.post("/", authenticateApiKey, async (req, res) => {
try {
const { nome, telefone, aniversario, obs } = req.body;
if (!nome || !telefone) return res.status(400).json({ error: "nome e telefone são obrigatórios" });


const { data, error } = await supabase
.from("clientes")
.insert([{ nome, telefone, aniversario: aniversario || null, obs: obs || null }])
.select("*")
.single();


if (error) return res.status(500).json({ error });
res.json(data);
} catch (e) {
res.status(500).json({ error: e.message });
}
});


// ↙️ Criação via Dashboard (COM login)
router.post("/owner", authenticateToken, async (req, res) => {
try {
const { nome, telefone, aniversario, obs } = req.body;
if (!nome || !telefone) return res.status(400).json({ error: "nome e telefone são obrigatórios" });


const { data, error } = await supabase
.from("clientes")
.insert([{ nome, telefone, aniversario: aniversario || null, obs: obs || null }])
.select("*")
.single();


if (error) return res.status(500).json({ error });
res.json(data);
} catch (e) {
res.status(500).json({ error: e.message });
}
});


// ↙️ Listagem (COM login)
router.get("/", authenticateToken, async (req, res) => {
try {
const { data, error } = await supabase
.from("clientes")
.select("*")
.order("created_at", { ascending: false });


if (error) return res.status(500).json({ error });
res.json(data);
} catch (e) {
res.status(500).json({ error: e.message });
}
});


export default router;