# Sistema de Gestão de Clientes i9Robótica - Manual do Usuário

## Visão Geral

Este documento fornece instruções para utilização do Sistema de Gestão de Clientes da i9Robótica, uma aplicação web projetada para gerenciar dados de clientes e alertas de manutenção para sistemas repelentes de pombos.

## Funcionalidades do Sistema

1. **Gestão de Clientes**
   - Cadastro de novos clientes com validação
   - Visualização, edição e exclusão de informações de clientes
   - Busca e filtragem de clientes por nome e data de instalação

2. **Alertas de Manutenção**
   - Cálculo automático de datas de manutenção (6 meses após a instalação)
   - Visualização de manutenções programadas
   - Filtragem de alertas por período
   - Geração e envio de notificações por email

3. **Autenticação de Usuários**
   - Sistema de login seguro
   - Controle de acesso baseado em funções (administrador/usuários comuns)
   - Autenticação baseada em tokens JWT

## Primeiros Passos

### Requisitos do Sistema
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexão com a internet

### Acessando o Sistema
1. Acesse a URL fornecida
2. Faça login com suas credenciais
   - Para a primeira configuração, registre uma conta de administrador

## Utilizando o Sistema

### Cadastro de Clientes
1. Navegue até a seção "Clientes"
2. Clique em "Adicionar Novo Cliente"
3. Preencha as informações necessárias:
   - Nome
   - Endereço
   - Número de telefone
   - Data de instalação
4. Clique em "Salvar" para cadastrar o cliente

### Lista de Clientes
1. Navegue até a seção "Clientes"
2. Visualize todos os clientes em formato de tabela
3. Use a caixa de busca para filtrar por nome
4. Use os filtros de data para encontrar clientes por data de instalação
5. Clique em um cliente para ver detalhes ou editar informações

### Alertas de Manutenção
1. Navegue até a seção "Alertas de Manutenção"
2. Visualize as manutenções programadas
3. Filtre alertas por período
4. Clique em um cliente para ver detalhes

### Enviando Notificações de Manutenção
Siga as instruções no documento `maintenance_alerts.md` para enviar notificações por email manualmente.

## Administração

### Gestão de Usuários
1. Navegue até a seção "Usuários" (apenas administradores)
2. Visualize todos os usuários do sistema
3. Adicione, edite ou remova usuários
4. Defina funções de usuário (administrador/comum)

### Configuração do Sistema
1. Navegue até a seção "Configurações" (apenas administradores)
2. Configure parâmetros do sistema
3. Atualize configurações de notificação

## Solução de Problemas

### Problemas Comuns
- **Problemas de Login**: Certifique-se de que o nome de usuário e senha estão corretos
- **Dados Ausentes**: Verifique se todos os campos obrigatórios foram preenchidos durante o cadastro
- **Discrepâncias nos Alertas**: Verifique a precisão das datas de instalação

### Suporte
Para suporte técnico, entre em contato com o administrador do sistema.

## Recomendações de Segurança
- Use senhas fortes
- Faça logout quando não estiver usando o sistema
- Atualize regularmente as credenciais de usuário
- Não compartilhe informações de login

## Backup de Dados
O sistema faz backup automático dos dados no banco de dados. Para segurança adicional, backups regulares do banco de dados são recomendados.
