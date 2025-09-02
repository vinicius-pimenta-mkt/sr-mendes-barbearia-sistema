// src/routes/agendamentos.js
import express from "express";
import { supabase } from "../db.js";
import { authenticateToken, authenticateApiKey } from "../middleware/auth.js";

const router = express.Router();

// Criar agendamento (via n8n → API Key)
router.post("/", authenticateApiKey, async (req, res) => {
  try {
    const { cliente_id, servico, data_hora, preco } = req.body;

    const { data, error } = await supabase
      .from("agendamentos")
      .insert([{ cliente_id, servico, data_hora, preco }])
      .select();

    if (error) throw error;

    res.json(data[0]);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Criar agendamento (via dono da barbearia → dashboard)
router.post("/owner", authenticateToken, async (req, res) => {
  try {
    const { cliente_id, servico, data_hora, preco } = req.body;

    const { data, error } = await supabase
      .from("agendamentos")
      .insert([{ cliente_id, servico, data_hora, preco }])
      .select();

    if (error) throw error;

    res.json(data[0]);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Listar agendamentos do dono
router.get("/owner", authenticateToken, async (req, res) => {
  try {
    const { data, error } = await supabase
      .from("agendamentos")
      .select("id, cliente_id, servico, data_hora, preco");

    if (error) throw error;

    res.json(data);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

export default router;
