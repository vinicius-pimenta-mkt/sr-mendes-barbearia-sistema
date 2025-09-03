# Sistema de Gerenciamento Sr. Mendes Barbearia

## Visão Geral

Este é um sistema completo de gerenciamento para a Sr. Mendes Barbearia, desenvolvido para integrar com automações do N8N via WhatsApp. O sistema permite que os clientes façam agendamentos através do WhatsApp e que o barbeiro gerencie todos os aspectos do negócio através de um dashboard web.

## Funcionalidades

### 🔐 Sistema de Autenticação
- Login seguro para o proprietário da barbearia
- Proteção de rotas com JWT
- Interface de login personalizada com a marca da barbearia

### 📊 Dashboard Administrativo
- Visão geral dos atendimentos do dia
- Receita diária e mensal
- Próximos agendamentos
- Relatórios de serviços realizados

### 👥 Gestão de Clientes
- Cadastro e edição de clientes
- Histórico de atendimentos
- Informações de contato

### 📅 Gestão de Agendamentos
- Visualização de agendamentos por data
- Criação, edição e cancelamento de agendamentos
- Status dos agendamentos (Confirmado, Pendente, Cancelado)

### 🤖 Integração com N8N
- Webhook para receber dados do WhatsApp
- API endpoints para criar/atualizar agendamentos
- Sincronização automática com o sistema

## Estrutura do Projeto

```
barber-system/
├── src/
│   ├── main.py              # Arquivo principal do Flask
│   ├── static/              # Frontend React compilado
│   ├── routes/              # Rotas da API
│   │   ├── auth.py          # Autenticação
│   │   ├── clientes.py      # Gestão de clientes
│   │   ├── agendamentos.py  # Gestão de agendamentos
│   │   └── relatorios.py    # Relatórios e dashboard
│   └── models/              # Modelos do banco de dados
├── .env                     # Variáveis de ambiente
├── requirements.txt         # Dependências Python
├── vercel.json             # Configuração para deploy
└── README.md               # Esta documentação
```

## Configuração das Variáveis de Ambiente

O arquivo `.env` contém as seguintes variáveis:

```env
SUPABASE_URL=https://yrvxuporikccnokatbcp.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
ADMIN_USER=adminmendes
ADMIN_PASS=mendesbarber01
JWT_SECRET=019283
N8N_API_KEY=019283
```

## API Endpoints

### Autenticação
- `POST /api/auth/login` - Login do administrador

### Clientes
- `GET /api/clientes` - Listar todos os clientes
- `POST /api/clientes` - Criar novo cliente
- `PUT /api/clientes/{id}` - Atualizar cliente
- `DELETE /api/clientes/{id}` - Remover cliente

### Agendamentos
- `GET /api/agendamentos` - Listar todos os agendamentos
- `POST /api/agendamentos` - Criar novo agendamento
- `PUT /api/agendamentos/{id}` - Atualizar agendamento
- `DELETE /api/agendamentos/{id}` - Cancelar agendamento
- `GET /api/agendamentos/hoje` - Agendamentos do dia

### Relatórios
- `GET /api/relatorios/dashboard` - Dados do dashboard
- `GET /api/relatorios/mensal` - Relatório mensal
- `POST /api/relatorios/n8n` - Webhook para N8N

## Como Fazer o Deploy na Vercel

### Pré-requisitos
1. Conta na Vercel (https://vercel.com)
2. Vercel CLI instalado (`npm i -g vercel`)
3. Git configurado

### Passos para Deploy

1. **Preparar o repositório:**
   ```bash
   cd barber-system
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Fazer o deploy:**
   ```bash
   vercel
   ```

3. **Configurar variáveis de ambiente na Vercel:**
   - Acesse o dashboard da Vercel
   - Vá em Settings > Environment Variables
   - Adicione todas as variáveis do arquivo `.env`

4. **Testar o sistema:**
   - Acesse a URL fornecida pela Vercel
   - Faça login com as credenciais: `adminmendes` / `mendesbarber01`

## Integração com N8N

### Configuração do Webhook

1. **No N8N, configure um webhook HTTP:**
   - URL: `https://seu-dominio.vercel.app/api/relatorios/n8n`
   - Método: POST
   - Headers: `Content-Type: application/json`

2. **Estrutura dos dados para envio:**
   ```json
   {
     "tipo": "novo_agendamento",
     "cliente": "Nome do Cliente",
     "telefone": "(11) 99999-9999",
     "servico": "Corte e Barba",
     "data": "2025-08-28",
     "hora": "14:30"
   }
   ```

### Exemplos de Integração

#### Criar Novo Agendamento via N8N
```json
POST /api/agendamentos
{
  "cliente": "João Silva",
  "servico": "Corte e Barba",
  "data": "2025-08-28",
  "hora": "14:30",
  "status": "Confirmado",
  "preco": 50.00
}
```

#### Atualizar Status do Agendamento
```json
PUT /api/agendamentos/1
{
  "status": "Confirmado"
}
```

## Credenciais de Acesso

- **Usuário:** adminmendes
- **Senha:** mendesbarber01

## Suporte e Manutenção

Para dúvidas ou problemas:
1. Verifique os logs na Vercel
2. Confirme se as variáveis de ambiente estão configuradas
3. Teste os endpoints da API individualmente

## Próximos Passos

1. **Testar o sistema completo**
2. **Configurar o N8N com os webhooks**
3. **Treinar o uso do dashboard**
4. **Monitorar o funcionamento em produção**

---

**Desenvolvido por:** Manus AI  
**Data:** Agosto 2025  
**Versão:** 1.0.0

