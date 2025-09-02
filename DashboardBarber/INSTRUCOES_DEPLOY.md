# Instruções Detalhadas para Deploy - Sr. Mendes Barbearia

## 🚀 Guia Passo a Passo para Deploy na Vercel

### Pré-requisitos

Antes de começar, você precisará:

1. **Conta no GitHub** (gratuita): https://github.com
2. **Conta na Vercel** (gratuita): https://vercel.com
3. **Git instalado** no seu computador

### Passo 1: Preparar o Código no GitHub

1. **Criar um repositório no GitHub:**
   - Acesse https://github.com
   - Clique em "New repository"
   - Nome: `sr-mendes-barbearia-sistema`
   - Marque como "Public"
   - Clique em "Create repository"

2. **Fazer upload dos arquivos:**
   - Baixe todos os arquivos da pasta `barber-system`
   - No GitHub, clique em "uploading an existing file"
   - Arraste todos os arquivos para a área de upload
   - Escreva uma mensagem: "Sistema inicial da barbearia"
   - Clique em "Commit changes"

### Passo 2: Conectar com a Vercel

1. **Criar conta na Vercel:**
   - Acesse https://vercel.com
   - Clique em "Sign Up"
   - Escolha "Continue with GitHub"
   - Autorize a Vercel a acessar sua conta GitHub

2. **Importar o projeto:**
   - No dashboard da Vercel, clique em "New Project"
   - Encontre o repositório `sr-mendes-barbearia-sistema`
   - Clique em "Import"

3. **Configurar o projeto:**
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** (deixe vazio)
   - **Output Directory:** (deixe vazio)
   - **Install Command:** pip install -r requirements.txt

### Passo 3: Configurar Variáveis de Ambiente

1. **Após o deploy inicial:**
   - Vá em "Settings" no projeto
   - Clique em "Environment Variables"

2. **Adicionar as seguintes variáveis:**
   ```
   SUPABASE_URL = https://yrvxuporikccnokatbcp.supabase.co
   SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlydnh1cG9yaWtjY25va2F0YmNwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczOTExMzgwMywiZXhwIjoyMDU0Njg5ODAzfQ.IXeEOx3QhPYhFYimYLDkvfHghneMw6uviw2OLD7SEjI
   ADMIN_USER = adminmendes
   ADMIN_PASS = mendesbarber01
   JWT_SECRET = 019283
   N8N_API_KEY = 019283
   ```

3. **Fazer redeploy:**
   - Vá em "Deployments"
   - Clique nos três pontos do último deploy
   - Clique em "Redeploy"

### Passo 4: Testar o Sistema

1. **Acessar o sistema:**
   - A Vercel fornecerá uma URL como: `https://sr-mendes-barbearia-sistema.vercel.app`
   - Acesse essa URL

2. **Fazer login:**
   - Usuário: `adminmendes`
   - Senha: `mendesbarber01`

3. **Verificar funcionalidades:**
   - Dashboard deve carregar
   - Navegação entre páginas deve funcionar
   - Dados mock devem aparecer

## 🤖 Configuração do N8N

### Passo 1: Configurar Webhooks

1. **No seu fluxo N8N, adicione um nó HTTP Request:**
   - URL: `https://sua-url.vercel.app/api/agendamentos`
   - Método: POST
   - Headers: `Content-Type: application/json`

2. **Estrutura para criar agendamento:**
   ```json
   {
     "cliente": "{{$node['WhatsApp'].json['nome']}}",
     "servico": "{{$node['WhatsApp'].json['servico']}}",
     "data": "{{$node['WhatsApp'].json['data']}}",
     "hora": "{{$node['WhatsApp'].json['hora']}}",
     "status": "Pendente",
     "preco": 50.00
   }
   ```

### Passo 2: Endpoints Disponíveis

#### Criar Cliente
```
POST https://sua-url.vercel.app/api/clientes
{
  "nome": "João Silva",
  "telefone": "(11) 99999-9999",
  "email": "joao@email.com"
}
```

#### Criar Agendamento
```
POST https://sua-url.vercel.app/api/agendamentos
{
  "cliente": "João Silva",
  "servico": "Corte e Barba",
  "data": "2025-08-28",
  "hora": "14:30",
  "status": "Confirmado",
  "preco": 50.00
}
```

#### Atualizar Agendamento
```
PUT https://sua-url.vercel.app/api/agendamentos/1
{
  "status": "Confirmado"
}
```

#### Webhook Genérico (Recomendado)
```
POST https://sua-url.vercel.app/api/relatorios/n8n
{
  "tipo": "novo_agendamento",
  "dados": {
    "cliente": "João Silva",
    "telefone": "(11) 99999-9999",
    "servico": "Corte e Barba",
    "data": "2025-08-28",
    "hora": "14:30"
  }
}
```

## 🔧 Solução de Problemas

### Problema: Site não carrega
**Solução:**
1. Verifique se o deploy foi bem-sucedido na Vercel
2. Confirme se todas as variáveis de ambiente foram configuradas
3. Verifique os logs na aba "Functions" da Vercel

### Problema: Login não funciona
**Solução:**
1. Confirme as credenciais: `adminmendes` / `mendesbarber01`
2. Verifique se as variáveis `ADMIN_USER` e `ADMIN_PASS` estão corretas
3. Teste a API diretamente: `POST /api/auth/login`

### Problema: N8N não consegue enviar dados
**Solução:**
1. Verifique se a URL está correta
2. Confirme se o Content-Type é `application/json`
3. Teste o endpoint com Postman ou similar

### Problema: Dados não aparecem no dashboard
**Solução:**
1. Os dados iniciais são mock (fictícios)
2. Para dados reais, configure o banco de dados Supabase
3. Ou modifique os arquivos de rotas para usar dados persistentes

## 📱 Como Usar o Sistema

### Para o Barbeiro (Você)

1. **Acessar o sistema:**
   - Abra o navegador
   - Vá para sua URL da Vercel
   - Faça login

2. **Dashboard principal:**
   - Veja atendimentos do dia
   - Receita atual
   - Próximos agendamentos

3. **Gerenciar agendamentos:**
   - Clique em "Agendamentos"
   - Veja, edite ou cancele agendamentos
   - Marque como confirmado/realizado

4. **Gerenciar clientes:**
   - Clique em "Clientes"
   - Adicione novos clientes
   - Edite informações de contato

### Para os Clientes (Via WhatsApp + N8N)

1. **Cliente envia mensagem no WhatsApp**
2. **N8N processa a mensagem**
3. **N8N envia dados para o sistema**
4. **Agendamento aparece no seu dashboard**
5. **Você confirma ou ajusta conforme necessário**

## 🔄 Atualizações Futuras

### Para adicionar novas funcionalidades:

1. **Modificar o código:**
   - Edite os arquivos necessários
   - Teste localmente se possível

2. **Atualizar no GitHub:**
   - Faça upload dos arquivos modificados
   - Ou use Git se souber

3. **Deploy automático:**
   - A Vercel detecta mudanças no GitHub
   - Faz deploy automaticamente
   - Você recebe notificação por email

## 📞 Suporte

Se tiver problemas:

1. **Verifique os logs na Vercel**
2. **Teste os endpoints individualmente**
3. **Confirme as variáveis de ambiente**
4. **Documente o erro específico**

## ✅ Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Projeto importado na Vercel
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] Login funcionando
- [ ] Dashboard carregando
- [ ] N8N configurado (se aplicável)
- [ ] Testes realizados

---

**Lembre-se:** Este sistema está pronto para uso imediato. Os dados iniciais são fictícios para demonstração. Conforme você usar com o N8N, os dados reais irão substituir os dados de exemplo.

**Importante:** Guarde bem a URL do seu sistema e as credenciais de login!

