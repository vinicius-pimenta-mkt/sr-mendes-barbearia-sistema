// src/routes/relatorios.js
import express from "express";
import { supabase } from "../db.js";
import { authenticateToken, authenticateApiKey } from "../middleware/auth.js";
import PDFDocument from "pdfkit";

const router = express.Router();

/**
 * Util: Obtém intervalo de datas a partir da query (?from=...&to=...).
 * Se não vier nada, usa o dia de hoje (início/fim) no fuso do servidor.
 * from/to devem estar em formato ISO (ex.: 2025-08-27T00:00:00-03:00).
 */
function getDateRange(query) {
  const { from, to } = query || {};
  if (from && to) {
    return {
      fromISO: new Date(from).toISOString(),
      toISO: new Date(to).toISOString(),
      label: `${from} → ${to}`,
    };
  }
  // default: hoje (00:00 até 23:59:59.999)
  const now = new Date();
  const start = new Date(now);
  start.setHours(0, 0, 0, 0);
  const end = new Date(now);
  end.setHours(23, 59, 59, 999);
  return {
    fromISO: start.toISOString(),
    toISO: end.toISOString(),
    label: `${start.toISOString()} → ${end.toISOString()}`,
  };
}

/**
 * Agrega os dados por serviço: qty e revenue.
 * Espera linhas com { servico, preco }.
 */
function aggregateByService(rows) {
  const byService = {};
  for (const row of rows) {
    const name = row.servico || "Indefinido";
    const price = Number(row.preco) || 0;
    if (!byService[name]) byService[name] = { service: name, qty: 0, revenue: 0 };
    byService[name].qty += 1;
    byService[name].revenue += price;
  }
  const list = Object.values(byService).sort((a, b) => b.qty - a.qty);
  const totals = list.reduce(
    (acc, it) => {
      acc.qty += it.qty;
      acc.revenue += it.revenue;
      return acc;
    },
    { qty: 0, revenue: 0 },
  );
  return { list, totals };
}

/**
 * GET /relatorios/resumo (dashboard do dono)
 * Protegido por JWT (authenticateToken)
 * Query params: ?from=ISO&to=ISO
 */
router.get("/resumo", authenticateToken, async (req, res) => {
  try {
    const { fromISO, toISO } = getDateRange(req.query);

    const { data, error } = await supabase
      .from("agendamentos")
      .select("servico, preco, data_hora")
      .gte("data_hora", fromISO)
      .lt("data_hora", toISO);

    if (error) throw error;

    const { list, totals } = aggregateByService(data || []);

    return res.json({
      by_service: list, // [{ service, qty, revenue }]
      totals,           // { qty, revenue }
      range: { from: fromISO, to: toISO },
    });
  } catch (err) {
    return res.status(400).json({ error: String(err.message || err) });
  }
});

/**
 * GET /relatorios/export.pdf
 * Gera um PDF do resumo no período.
 * Protegido por JWT (authenticateToken)
 * Query params: ?from=ISO&to=ISO
 */
router.get("/export.pdf", authenticateToken, async (req, res) => {
  try {
    const { fromISO, toISO, label } = getDateRange(req.query);

    const { data, error } = await supabase
      .from("agendamentos")
      .select("servico, preco, data_hora")
      .gte("data_hora", fromISO)
      .lt("data_hora", toISO);

    if (error) throw error;

    const { list, totals } = aggregateByService(data || []);

    // Cabeçalhos do PDF
    res.setHeader("Content-Type", "application/pdf");
    res.setHeader("Content-Disposition", 'inline; filename="relatorio-barbearia.pdf"');

    const doc = new PDFDocument({ margin: 40 });
    doc.pipe(res);

    doc.fontSize(18).text("Relatório da Barbearia", { underline: true });
    doc.moveDown(0.5);
    doc.fontSize(11).text(`Período: ${label}`);
    doc.moveDown(1);

    doc.fontSize(14).text("Resumo por Serviço");
    doc.moveDown(0.5);

    // Cabeçalho da "tabela"
    doc.fontSize(11).text("Serviço".padEnd(28) + "Qtd".padEnd(6) + "Receita (R$)");
    doc.moveTo(40, doc.y).lineTo(555, doc.y).stroke();
    doc.moveDown(0.5);

    list.forEach((it) => {
      const revenueBRL = (it.revenue / 100).toFixed(2).replace(".", ",");
      doc.text(
        `${(it.service || "").padEnd(28)}${String(it.qty).padEnd(6)}${revenueBRL}`,
      );
    });

    doc.moveDown(1);
    doc.fontSize(12).text("Totais", { underline: true });
    const totalBRL = (totals.revenue / 100).toFixed(2).replace(".", ",");
    doc.fontSize(11).text(`Atendimentos: ${totals.qty}`);
    doc.text(`Receita total: R$ ${totalBRL}`);

    doc.end();
  } catch (err) {
    return res.status(400).json({ error: String(err.message || err) });
  }
});

/**
 * (Opcional) endpoint para o n8n puxar via API Key
 * Ex.: GET /relatorios/resumo-n8n?from=...&to=...
 */
router.get("/resumo-n8n", authenticateApiKey, async (req, res) => {
  try {
    const { fromISO, toISO } = getDateRange(req.query);
    const { data, error } = await supabase
      .from("agendamentos")
      .select("servico, preco, data_hora")
      .gte("data_hora", fromISO)
      .lt("data_hora", toISO);

    if (error) throw error;

    const { list, totals } = aggregateByService(data || []);
    return res.json({ by_service: list, totals, range: { from: fromISO, to: toISO } });
  } catch (err) {
    return res.status(400).json({ error: String(err.message || err) });
  }
});

export default router;
