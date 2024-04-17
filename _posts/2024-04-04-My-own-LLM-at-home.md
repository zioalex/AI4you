---
title: "My own LLM@Home"
date: 2024-04-04
tags: LLL ollama
categories: posts videoblog demo
---

- [Intro](#intro)
  - [What is Ollama](#what-is-ollama)
  - [Requirements](#requirements)
- [How to use Ollama](#how-to-use-ollama)
  - [Installation](#installation)
  - [Other OSs](#other-oss)
  - [Some Examples](#some-examples)
- [Alternatives to Ollama](#alternatives-to-ollama)
- [Hardware and Software used](#hardware-and-software-used)
- [Conclusion](#conclusion)
- [What's next](#whats-next)
- [References](#references)

# Intro

You may have heard of the term LLM (Large Language Model) before. It is a type of model that is trained on a large corpus of text data and can generate text that is similar to the text it was trained on, and not only. The most famous example of an LLM is OpenAI's CHAT-GPT. However, training an LLM like GPT-3 or 4 requires a lot of computational resources and expertise. In this post, I will show you how you can download a pre-trained model and use it to generate text on your own computer.

## What is Ollama

[Ollama](https://github.com/ollama/ollama) is a neat opensource project that allow us to run a large language model on our own computer.

You can find here a lot of opensource models that can be downloaded and used very easily.
![models](/assets/imgs/ollama_models.png)

## Requirements

You do not need any specific hardware to run Ollama. Some memory would help. Surely a GPU will make it faster.

# How to use Ollama

## Installation

It very easy to install Ollama. You can install it on Linux with:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Other OSs

![Ollama installation](/assets/imgs/ollama_installation.png)
Just check it here [Ollama Installation](https://ollama.com/download)

## Some Examples

Let's start with something easy.

- I want to impress my wife! - Write a love song in German

- I want to impress my boss! - Write a business plan for my new project on AI applied to DevOps

- I want to be a bit philosophical - Just give me 3 reasons why God exists and 3 why he doesn't exists

- I need to do some research - Write a python script to scrape the web for the latest news on AI

# Alternatives to Ollama

- [LM Studio](https://lmstudio.ai/)
- [Jan AI](https://jan.ai/)

# Hardware and Software used

PC with Linux Ubuntu 20.04
CPU: AMD Ryzen 7 3700X 8-Core Processor
RAM: 16GiB
GPU: GeForce RTX 2070 SUPER

# Conclusion

Ollama is very easy to use. Everybody with a miminum of IT knowledge can use it.
What we have seen here is just an easy example with a small LLM. You need to know that bigger the LLM is, more powerful it is.

# What's next

- Demo with bigger LLMs
- Demo with [pyautogen](https://pypi.org/project/pyautogen/) to generate code witn multiple agents
- Try [opendevin](https://github.com/OpenDevin/OpenDevin) to have the next level of AI applied to SW Development

# References

- [[1hr Talk] Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) - Andrej Karpathy
- [Autogen: Ollama integration 🤯 Step by Step Tutorial. Mind-blowing!](https://www.youtube.com/watch?v=UQw04VW60U0) -  Mervin Praison
- [Ollama](https://ollama.com/)
