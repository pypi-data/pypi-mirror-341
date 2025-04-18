# Kafka MCP Server

A Message Context Protocol (MCP) server that integrates with Apache Kafka to provide publish and consume functionalities for LLM and Agentic applications.

## Overview

This project implements a server that allows AI models to interact with Kafka topics through a standardized interface. It supports:

- Publishing messages to Kafka topics
- Consuming messages from Kafka topics

## Prerequisites

- Python 3.8+
- Apache Kafka instance
- Python dependencies (see Installation section)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   If no requirements.txt exists, install the following packages:
   ```bash
   pip install aiokafka python-dotenv pydantic-settings mcp-server
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TOPIC_NAME=your-topic-name
IS_TOPIC_READ_FROM_BEGINNING=False
DEFAULT_GROUP_ID_FOR_CONSUMER=kafka-mcp-group

# Optional: Custom Tool Descriptions
# TOOL_PUBLISH_DESCRIPTION="Custom description for the publish tool"
# TOOL_CONSUME_DESCRIPTION="Custom description for the consume tool"
```

## Usage

### Running the Server

You can run the server using the provided `main.py` script:

```bash
python main.py --transport stdio
```

Available transport options:
- `stdio`: Standard input/output (default)
- `sse`: Server-Sent Events

### Integrating with Claude Desktop

To use this Kafka MCP server with Claude Desktop, add the following configuration to your Claude Desktop configuration file:

```json
{
    "mcpServers": {
        "kafka": {
            "command": "python",
            "args": [
                "<PATH TO PROJECTS>/main.py"
            ]
        }
    }
}
```

Replace `<PATH TO PROJECTS>` with the absolute path to your project directory.

## Project Structure

- `main.py`: Entry point for the application
- `kafka.py`: Kafka connector implementation
- `server.py`: MCP server implementation with tools for Kafka interaction
- `settings.py`: Configuration management using Pydantic

## Available Tools

### kafka-publish

Publishes information to the configured Kafka topic.

### kafka-consume

consume information from the configured Kafka topic.
- Note: once a message is read from the topic it can not be read again using the same groupid
