<p align="center">
  <img src="https://github.com/user-attachments/assets/fe76e7d7-e13b-4977-8a79-7c6781c20386" alt="Nexum Logo" width="300">
</p>


# 🌐 Nexum - Seu Chat IA Independente & Multiusuário

[App do Nexum]](https://hamgvhxec9mjwroryx3x5i.streamlit.app/)

**Nexum** é uma plataforma web interativa de Inteligência Artificial Generativa construída em **Python** com **Streamlit**. O projeto
foi desenhado sob o conceito *Bring Your Own Key* (Traga sua Própria Chave), garantindo controle total de custos, privacidade e
isolamento de dados para múltiplos usuários simultâneos.

---

## 🚀 Funcionalidades Premium

*   **🔒 Arquitetura Blindada (Anti-Vazamento):** Chaves de API isoladas por sessão de navegador. O uso de uma pessoa nunca interfere
*    na cota ou nos créditos de outra.
*   **📊 Painel de Estatísticas ao Vivo:** Controle de consumo em tempo real com medidor de mensagens trocadas e estimativa de tokens
*    acumulados.
*   **💾 Histórico Autônomo e Exclusivo:** O sistema gera um banco de arquivos `.txt` único baseado no ID de cada chave, permitindo
*    salvar e continuar conversas sem misturar dados.
*   **🤖 Respostas Inteligentes e Diretas:** Prompt de sistema personalizado que elimina respostas artificiais de robôs, garantindo
*    diálogos naturais e blocos de códigos limpos prontos para cópia.

## 🛠️ Tecnologias Utilizadas

*   **Linguagem Principal:** Python 3.12
*   **Interface Web:** Streamlit
*   **Processamento de IA:** Google GenAI SDK (Interface Web) / Hugging Face Transformers (Versão Local)

---

## 💻 Como Rodar o Nexum Localmente (Modo Turbo GPU)

Se você deseja rodar o motor do Nexum de forma 100% gratuita, local e offline usando aceleração por placa de vídeo (GPU T4), você
pode executar o nosso ecossistema de desenvolvimento através do Google Colab:

1. Ative o ambiente de execução **GPU T4** no menu do Colab.
2. Instale os drivers de compressão de 4-bits:
   ```bash
   pip install transformers accelerate bitsandbytes ipywidgets
   ```
3. Execute a interface interativa em Python carregando o modelo `microsoft/Phi-3-mini-4k-instruct`.

---

## 📈 Roadmap de Atualizações Futuras

*   [ ] **Módulo de Visão:** Upload e análise multimodal de imagens (PNG/JPG).
*   [ ] **Leitura de Documentos:** Suporte para carregamento e resumo de arquivos de texto e códigos.
*   [ ] **Exportação Direta:** Botão para o usuário baixar o histórico de conversas direto para o computador em Markdown.

---
💡 *Desenvolvido com foco no aprendizado de arquiteturas modernas de IA Generativa, ciclo de vida de aplicações web e segurança da
informação.*
