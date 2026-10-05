# ⚡ Sift AI

> **Automated Multi-Agent Intelligence Engine & Serverless GPU Pipeline**  
> *Autonomous research agents powered by open-source LLMs, executing on headless Nvidia T4 GPUs with zero infrastructure overhead.*

[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue?style=for-the-badge&logo=githubactions)](https://github.com)
[![Kaggle GPU](https://img.shields.io/badge/Cloud%20GPU-Nvidia%20T4-20BEFF?style=for-the-badge&logo=kaggle)](https://kaggle.com)
[![CrewAI](https://img.shields.io/badge/Agents-CrewAI-FF4B4B?style=for-the-badge)](https://crewai.com)

---

## 🌟 Executive Summary

**Sift AI** is an enterprise-grade, serverless news curation and intelligence engine. Every morning, the system autonomously queries global sources, coordinates multi-agent research tasks, synthesizes findings into a structured digest, and dispatches a formatted PDF report directly to subscribers.

To eliminate recurring API costs and vendor lock-in, Sift AI offloads inference to open-weight model architectures (**Qwen** via **Ollama**) running on cloud GPUs triggered via a headless API pipeline.

---

## 🏗️ System Architecture

```text
                     ┌────────────────────────┐
                     │   GitHub Actions CRON  │
                     │   (Daily @ 6:30 AM)    │
                     └───────────┬────────────┘
                                 │
                                 ▼ (Kaggle CLI API)
                     ┌────────────────────────┐
                     │   Kaggle Cloud Kernel  │
                     │  (Headless Nvidia T4)  │
                     └───────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │    Ollama + CrewAI     │
                     │ (Qwen Agent Workflows) │
                     └───────────┬────────────┘
                                 │
                                 ▼
┌──────────────────┐  (PDF + SMTP) ┌────────────────────────┐
│ Subscriber Inbox │ <──────────── │ ReportLab PDF Generator│
└──────────────────┘               └────────────────────────┘
```

---

## 🚀 Engineering Highlights & Impact

* 🤖 **Multi-Agent Orchestration:** Powered by **CrewAI**, orchestrating specialized agent roles (Researcher, Synthesizer, Editor) to perform non-deterministic news extraction and cross-verification.
* ⚡ **Serverless GPU Offloading:** Executes open-source LLMs on **Nvidia T4 GPU instances** using the official **Kaggle Kernel API**, achieving zero compute costs without self-hosting infrastructure.
* 🔄 **Headless CI/CD Pipeline:** Fully automated via **GitHub Actions** (`cron` & `repository_dispatch` webhooks), removing human intervention and maintaining high availability.
* 🛡️ **Zero-Trust Secret Handling:** Cloud credentials and API keys are injected dynamically at runtime via Kaggle’s isolated `UserSecretsClient` vault—ensuring zero sensitive keys in repository source code.
* 🎛️ **Modern Control Panel:** Coupled with a **Next.js 14** web application deployed on Vercel, allowing on-demand manual triggers via encrypted dispatch hooks.

---

## 🛠️ Tech Stack & Tooling

| Domain | Technology |
| :--- | :--- |
| **Agentic Framework** | [CrewAI](https://crewai.com) |
| **LLM Inference** | [Ollama](https://ollama.com) (Qwen Open-Weight Models) |
| **Compute Engine** | Kaggle GPU API (Python 3.10 / Headless Container) |
| **Orchestration / CI-CD** | GitHub Actions Workflows |
| **Frontend / Dashboard** | Next.js 14, React, Tailwind CSS, Vercel |
| **Integrations** | NewsData API, ReportLab (PDF Engine), Python `smtplib` |

---

## 📐 Technical Evolution: Browser Automation vs. Headless API

| Architecture Metric | Legacy Approach (Playwright + Colab) | **Current Approach (Sift AI - Kaggle API)** |
| :--- | :--- | :--- |
| **Execution Path** | Simulated headless browser clicks | **Direct REST / CLI API Dispatch** |
| **Authentication** | Fragile session cookies & UI logins | **Scoped API Key Credentials** |
| **Reliability** | Susceptible to DOM changes & captcha | **Deterministic Cloud Execution** |
| **Overhead** | High (Browser boot + DOM parsing) | **Minimal (Lightweight API Payload)** |

---

## 📂 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── daily_colab_trigger.yml   # Scheduled CI/CD automation workflow
├── app/                              # Next.js control panel dashboard
├── sift-ai.ipynb                     # Core agent pipeline & PDF generation notebook
├── kernel-metadata.json              # Kaggle GPU execution specifications
└── package.json                      # Next.js dependencies
```

---

## ⚡ Quick Start

### 1. Local Configuration
Clone the project and verify `kernel-metadata.json`:
```json
{
  "id": "YOUR_KAGGLE_USERNAME/sift-ai-daily-runner",
  "title": "Sift AI Daily Runner",
  "code_file": "sift-ai.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": true
}
```

### 2. Manual Trigger via Kaggle CLI
```bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"

kaggle kernels push -p .
```

---

<p align="center">
  Built by <b>Manas</b> • Engine Powering Autonomous Intelligence
</p>
