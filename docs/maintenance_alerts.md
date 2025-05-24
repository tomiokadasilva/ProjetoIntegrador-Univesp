# Documentação do Sistema de Alertas de Manutenção

## Visão Geral
Este documento fornece instruções para utilização do sistema de alertas de manutenção no Sistema de Gestão de Clientes da i9Robótica. Como as tarefas agendadas estão atualmente desativadas, este guia foca em alternativas manuais para envio de alertas de manutenção.

## Script de Alerta por Email

O sistema inclui um script Python (`scripts/send_maintenance_alerts.py`) que pode ser executado manualmente para enviar alertas de manutenção via email. Este script:

1. Consulta o banco de dados para clientes que necessitam de manutenção
2. Gera um email HTML formatado com detalhes do cliente
3. Envia o email para destinatários específicos

## Instruções para Execução Manual

### Pré-requisitos
- Detalhes do servidor SMTP (endereço do servidor, porta, nome de usuário, senha)
- Endereço de email do destinatário

### Executando o Script
Execute o script pela linha de comando com os seguintes parâmetros:

```bash
python scripts/send_maintenance_alerts.py \
  --recipient "equipe@i9robotica.com" \
  --smtp_server "smtp.exemplo.com" \
  --smtp_port 587 \
  --smtp_user "notificacoes@i9robotica.com" \
  --smtp_password "sua_senha" \
  --days 30
```

### Explicação dos Parâmetros
- `--recipient`: Endereço de email para receber os alertas
- `--smtp_server`: Endereço do servidor SMTP
- `--smtp_port`: Porta do servidor SMTP (padrão: 587)
- `--smtp_user`: Nome de usuário da conta SMTP
- `--smtp_password`: Senha da conta SMTP
- `--days`: Limite de dias para alertas de manutenção (padrão: 30)

## Processos Manuais Alternativos

### Opção 1: Execução Manual Regular
Configure um lembrete no calendário para executar o script em intervalos regulares (ex: semanalmente nas manhãs de segunda-feira).

### Opção 2: Revisão do Painel
Verifique regularmente o Painel de Alertas na interface web para visualizar as próximas manutenções necessárias.

### Opção 3: Exportação para Sistema Externo
Use a API para exportar dados de manutenção para um sistema externo que suporte tarefas agendadas:

1. Acesse o endpoint da API de alertas: `/api/alerts`
2. Salve ou encaminhe os dados para seu sistema de notificação preferido

## Melhores Práticas

1. **Cronograma Regular**: Estabeleça um cronograma consistente para verificar alertas de manutenção
2. **Atribuição de Responsabilidade**: Designe membros específicos da equipe responsáveis por monitorar alertas
3. **Documentação**: Mantenha registros de notificações enviadas e manutenções concluídas
4. **Verificação**: Confirme o recebimento de notificações pela equipe de manutenção

## Melhorias Futuras

Quando as tarefas agendadas estiverem disponíveis, o sistema poderá ser aprimorado para:
- Executar automaticamente o script de alerta diariamente
- Enviar notificações personalizadas para diferentes membros da equipe
- Integrar com serviços de notificação por SMS
- Implementar procedimentos de escalonamento para manutenções atrasadas
