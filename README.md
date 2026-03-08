# 🚇 Totem de Autoatendimento para Compra de Bilhete Digital — Metrô-DF

> MVP acadêmico para compra de bilhete unitário comum via totem, pagamento por Pix, geração de bilhete eletrônico em QR Code e validação posterior no acesso por API REST.

---

## 📌 Visão Geral

Este repositório contém a implementação do **MVP de um totem de autoatendimento** para o **Metrô-DF**, com foco na compra de **bilhete unitário comum** de forma rápida, simples e adequada ao contexto de uso em estação.

A proposta do projeto é oferecer um **canal adicional de atendimento**, sem substituir os canais já existentes do Metrô-DF, permitindo ao usuário:

- iniciar atendimento no totem;
- comprar um bilhete unitário comum;
- pagar via **Pix**;
- receber o **bilhete digital** em forma de QR Code;
- capturar esse bilhete no celular;
- apresentar o bilhete no acesso;
- ter o uso controlado por **validação única via API REST**.

---

## 🎯 Finalidade do Projeto

A finalidade deste projeto é construir um **MVP funcional e demonstrável** que represente um fluxo viável de autoatendimento no contexto metroviário, equilibrando:

- simplicidade de uso;
- clareza operacional;
- coerência arquitetural;
- rastreabilidade no banco de dados;
- aderência ao escopo acadêmico.

Este projeto **não busca substituir** o ecossistema atual do Metrô-DF, e sim representar uma solução complementar para compra de bilhete unitário comum em ambiente de estação.

---

## ✅ Escopo do MVP

### Incluído no escopo

- atendimento inicial em **modo quiosque**;
- compra de **1 bilhete unitário comum por operação**;
- pagamento via **Pix**;
- exibição de **QR Code Pix** para pagamento;
- confirmação do pagamento;
- geração automática de **bilhete eletrônico**;
- exibição do QR Code do bilhete no totem;
- captura do bilhete pelo celular do usuário;
- página web do bilhete no navegador do celular;
- ação de **baixar imagem** do bilhete;
- ação de **enviar bilhete para outra pessoa**;
- API REST para validação posterior no acesso;
- controle de **uso único** do bilhete;
- rastreabilidade de sessão, pedido, pagamento, bilhete e validação.

---

## ❌ Fora do Escopo

Este projeto **não contempla**:

- aplicativo móvel completo;
- login ou cadastro de usuário;
- autenticação gov.br;
- biometria facial;
- carteira digital própria;
- integração com **carteiras digitais**;
- integração com **apps de mobilidade**;
- múltiplos bilhetes por operação;
- múltiplos trechos;
- saldo, extrato ou histórico do usuário;
- programas de benefício como:
  - passe estudantil;
  - passe para idosos;
  - gratuidades;
  - outros títulos subsidiados;
- mensageria, fila, eventos ou componentes arquiteturais avançados.

---

## 🧱 Arquitetura do Projeto

A arquitetura foi mantida **intencionalmente simples**, adequada ao escopo do MVP.

### Stack adotada

- **Frontend:** React Native
- **Backend:** Python (MVC)
- **Banco de Dados:** MySQL 8
- **Integração:** API REST
- **Execução do Totem:** modo quiosque
- **Validação do Bilhete:** API REST consumida posteriormente no ponto de acesso

### Decisões arquiteturais

- sem mensageria;
- sem fila;
- sem eventos assíncronos complexos;
- sem microsserviços;
- sem componentes avançados de infraestrutura além do necessário ao MVP.

A intenção foi preservar:

- clareza de implementação;
- facilidade de demonstração;
- coerência com o prazo e contexto acadêmico.

---

## 🗂️ Estrutura Conceitual do Domínio

As principais entidades do sistema são:

- **Totem**
- **Sessão de Atendimento**
- **Pedido**
- **Pagamento**
- **Bilhete Eletrônico**
- **Validação de Bilhete**

### Relação de alto nível

```text
Totem
 └── Sessão de Atendimento
      └── Pedido
           ├── Pagamento
           └── Bilhete Eletrônico
                └── Validação de Bilhete
