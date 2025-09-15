# MCP Chat Client

This project is a full-stack web application that serves as a client for the Model Context Protocol (MCP). It provides a web-based chat interface that can connect to any MCP-compliant server, allowing users to interact with language models that are enhanced with external tools.

## Features

-   **Web-based Chat Interface:** A simple and intuitive chat window to interact with the MCP client.
-   **Multi-Server Support:** Connect to multiple MCP servers by configuring them in a `config.json` file.
-   **Server Selection:** A dropdown menu to easily switch between different MCP servers.
-   **Powered by Gemini:** Uses Google's Gemini API for its language model capabilities.
-   **Example MCP Server:** Includes a sample weather server to demonstrate the client's functionality.

## Prerequisites

Before you begin, ensure you have the following installed:
-   [Python](https://www.python.org/) (version 3.8 or higher)
-   [`uv`](https://github.com/astral-sh/uv) (a fast Python package installer and resolver)
-   [Node.js](https://nodejs.org/) (version 16 or higher)
-   [`bun`](https://bun.sh/) (a fast JavaScript runtime, bundler, and package manager)

## Setup and Installation

1.  **Clone the repository (or download the code):**
    ```bash
    git clone <repository_url>
    cd mcp-chat-client
    ```

2.  **Set up the Python environment:**
    -   Create a virtual environment:
        ```bash
        uv venv
        ```
    -   Activate the virtual environment:
        -   On Windows:
            ```bash
            .venv\Scripts\activate
            ```
        -   On Unix or macOS:
            ```bash
            source .venv/bin/activate
            ```
    -   Install the Python dependencies:
        ```bash
        uv pip install Flask "mcp[cli]" google-generativeai python-dotenv
        ```

3.  **Configure the Gemini API Key:**
    -   Open the `.env` file and replace `YOUR_API_KEY_HERE` with your actual Gemini API key.
        ```
        GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```

4.  **Configure the MCP Servers:**
    -   Open the `config.json` file.
    -   Add or modify the list of MCP servers you want to connect to. Each server should have a `name` and a `url`.
        ```json
        {
          "servers": [
            {
              "name": "Local Weather Server",
              "url": "http://127.0.0.1:8000/mcp"
            },
            {
              "name": "Another Example Server",
              "url": "http://example.com/mcp"
            }
          ]
        }
        ```

5.  **Set up the example weather server:**
    -   Navigate to the `mcp-weather` directory:
        ```bash
        cd mcp-weather
        ```
    -   Install the dependencies:
        ```bash
        bun install
        ```
    -   Go back to the root directory:
        ```bash
        cd ..
        ```

## Running the Application

You need to run two components: the example MCP server and the Flask web application.

1.  **Run the example MCP server:**
    -   Open a terminal and navigate to the `mcp-weather` directory.
    -   Run the following command:
        ```bash
        bunx --bun tsx src/main.ts
        ```
    -   This will start the weather server. Keep this terminal window open.

2.  **Run the Flask web application:**
    -   Open a new terminal and navigate to the root directory of the project.
    -   Make sure your Python virtual environment is activated.
    -   Run the following command:
        ```bash
        python app.py
        ```
    -   This will start the Flask application on `http://127.0.0.1:5000`.

## Usage

1.  Open your web browser and go to `http://127.0.0.1:5000`.
2.  You should see the chat interface with a dropdown menu listing the servers from your `config.json` file.
3.  Select a server from the dropdown and click the "Connect" button.
4.  Once connected, you can start chatting with the language model.
5.  If you are connected to the weather server, you can ask questions like "What's the weather in London?". The model will use the `get-weather` tool from the MCP server to answer your question.
