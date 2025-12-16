---
title: Physical AI Humanoid Robotics Textbook Chatbot
emoji: 🤖
colorFrom: blue
colorTo: red
sdk: docker
pinned: false
license: mit
---

# Physical AI Humanoid Robotics Textbook Chatbot

This is an AI-powered chatbot that helps users understand the Physical AI Humanoid Robotics textbook content using Retrieval-Augmented Generation (RAG).

## Overview

This application provides an interactive chatbot interface for exploring the Physical AI Humanoid Robotics textbook. It uses RAG (Retrieval-Augmented Generation) to provide accurate, context-aware answers to questions about the textbook content.

## Features

- Interactive chat interface
- RAG-powered responses based on textbook content
- Session management to maintain conversation context
- Support for selected text context queries

## How it Works

1. The system uses vector embeddings to index the textbook content
2. When a user asks a question, relevant content is retrieved from the vector database
3. The retrieved context is combined with the user's question and sent to an LLM
4. The LLM generates a response based on the textbook content

## Environment Variables

To run this application, you'll need to set the following environment variables:

- `GROQ_API_KEY`: Your Groq API key for LLM access
- `QDRANT_HOST`: Qdrant vector database host (default: localhost)
- `QDRANT_PORT`: Qdrant vector database port (default: 6333)
- `DATABASE_URL`: Database URL (default: sqlite:///./chatbot.db)

## Usage

1. Ask questions about the Physical AI Humanoid Robotics textbook
2. The chatbot will provide answers based on the textbook content

## Architecture

- Backend: FastAPI application with RAG functionality
- Database: SQLite for session data
- Vector Database: Qdrant for textbook content embeddings
- LLM: Groq API for response generation