"""
Core client functionality for Dolphin MCP.
"""

import os
import sys
import json
import uuid
import time
import asyncio
import logging
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, AsyncGenerator
from colorama import init, Fore, Style

from mcp.client.sse import sse_client
from mcp import ClientSession

from .utils import load_mcp_config_from_file
from .providers.openai import generate_with_openai
from .providers.anthropic import generate_with_anthropic
from .providers.ollama import generate_with_ollama
from .providers.lmstudio import generate_with_lmstudio

# Initialize colorama
init()

# Configure rich console for logging
from rich.console import Console
console = Console()

class ChatMemory:
    """
    Class to store and manage conversation history across interactions.
    Supports persistent storage in a PostgreSQL database.
    """
    def __init__(self, 
                max_history: int = 10, 
                chat_id: Optional[str] = None,
                db_path: str = "chat_history.db"):
        """
        Initialize a new ChatMemory object.
        
        Args:
            max_history: Maximum number of message pairs to store in history
            chat_id: Optional ID to load an existing conversation (if None, a new ID is generated)
            db_path: Path to the SQLite database file for persistence (kept for backwards compatibility)
        """
        self.conversations = []
        self.max_history = max_history
        self.db_path = db_path
        
        # Initialize database if it doesn't exist
        self._init_db()
        
        # Generate a new ID if not provided
        if chat_id is None:
            self.chat_id = str(uuid.uuid4())
            self.is_new = True
        else:
            self.chat_id = chat_id
            self.is_new = False
            
        # Current timestamp for metadata
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.title = f"Conversation {self.chat_id[:8]}"
        
        # Load conversation history if ID exists and not a new conversation
        if not self.is_new:
            self._load_from_db()
        
    def _init_db(self):
        """Initialize the database tables if they don't exist."""
        try:
            from .db import init_db
            init_db()
        except ImportError:
            console.print("[yellow]PostgreSQL module not available. Using SQLite as fallback.[/yellow]")
            # Fall back to SQLite for backwards compatibility
            # Create directory if it doesn't exist
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                chat_id TEXT PRIMARY KEY,
                title TEXT,
                created_at TEXT,
                updated_at TEXT,
                metadata TEXT
            )
            ''')
            
            # Create messages table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                index_num INTEGER,
                role TEXT,
                content TEXT,
                tool_calls TEXT,
                timestamp TEXT,
                FOREIGN KEY (chat_id) REFERENCES conversations (chat_id)
            )
            ''')
            
            conn.commit()
            conn.close()
        
    def _load_from_db(self):
        """Load conversation history from database using chat_id."""
        try:
            from .db import load_conversation, load_messages
            
            # Get conversation metadata
            conversation = load_conversation(self.chat_id)
            
            if conversation:
                self.title = conversation.get('title', self.title)
                self.created_at = conversation.get('created_at', self.created_at)
                self.updated_at = conversation.get('updated_at', self.updated_at)
                
                # Get messages
                self.conversations = load_messages(self.chat_id)
                # Conversation was found, so it's not new
                self.is_new = False
            else:
                # ID not found, treat as a new conversation
                self.is_new = True
                self.chat_id = str(uuid.uuid4())
                self.created_at = datetime.now().isoformat()
                self.updated_at = self.created_at
                self.title = f"Conversation {self.chat_id[:8]}"
                
        except ImportError:
            # Fall back to SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get conversation metadata
            cursor.execute("SELECT title, created_at, updated_at FROM conversations WHERE chat_id = ?", 
                          (self.chat_id,))
            result = cursor.fetchone()
            
            if result:
                self.title, self.created_at, self.updated_at = result
                
                # Get messages
                cursor.execute(
                    "SELECT role, content, tool_calls FROM messages WHERE chat_id = ? ORDER BY index_num", 
                    (self.chat_id,)
                )
                
                self.conversations = []
                for role, content, tool_calls in cursor.fetchall():
                    message = {"role": role, "content": content}
                    
                    # Add tool calls if present
                    if tool_calls:
                        try:
                            message["tool_calls"] = json.loads(tool_calls)
                        except json.JSONDecodeError:
                            pass
                            
                    self.conversations.append(message)
                # Conversation was found, so it's not new
                self.is_new = False
            else:
                # ID not found, treat as a new conversation
                self.is_new = True
                self.chat_id = str(uuid.uuid4())
                self.created_at = datetime.now().isoformat()
                self.updated_at = self.created_at
                self.title = f"Conversation {self.chat_id[:8]}"
            
            conn.close()
    
    def save_to_db(self):
        """Save the current conversation to the database."""
        try:
            from .db import save_conversation, save_messages
            
            # Update timestamps
            self.updated_at = datetime.now().isoformat()
            
            # Save conversation metadata
            save_conversation(
                self.chat_id, 
                self.title, 
                self.created_at, 
                self.updated_at, 
                {}  # Empty metadata for now
            )
            
            # Save messages
            save_messages(self.chat_id, self.conversations)
            
        except ImportError:
            # Fall back to SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Update timestamps
            self.updated_at = datetime.now().isoformat()
            
            # Update or insert conversation metadata
            cursor.execute('''
            INSERT OR REPLACE INTO conversations (chat_id, title, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.chat_id, self.title, self.created_at, self.updated_at, '{}'))
            
            # Clear existing messages for this chat ID
            cursor.execute("DELETE FROM messages WHERE chat_id = ?", (self.chat_id,))
            
            # Insert all messages
            for i, message in enumerate(self.conversations):
                role = message.get("role", "")
                content = message.get("content", "")
                tool_calls = json.dumps(message.get("tool_calls", [])) if "tool_calls" in message else None
                timestamp = datetime.now().isoformat()
                
                cursor.execute('''
                INSERT INTO messages (chat_id, index_num, role, content, tool_calls, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (self.chat_id, i, role, content, tool_calls, timestamp))
            
            conn.commit()
            conn.close()
                    
    def add_message(self, message: Dict[str, str]):
        """
        Add a message to the conversation history and persist to database.
        
        Args:
            message: A message dict with 'role' and 'content' keys
        """
        self.conversations.append(message)
        
        # Trim history if needed
        if self.max_history > 0:
            keep_count = self.max_history * 2 + 1  # User/assistant pairs + initial system message
            if len(self.conversations) > keep_count:
                # Keep system message (if present) and most recent messages
                if self.conversations[0].get('role') == 'system':
                    self.conversations = [self.conversations[0]] + self.conversations[-(keep_count-1):]
                else:
                    self.conversations = self.conversations[-keep_count:]
        
        # Generate title from first user message if this is a new conversation
        if self.is_new and message.get('role') == 'user' and self.title.startswith('Conversation'):
            content = message.get('content', '')
            # Truncate to create a reasonable title
            title = content[:40] + ('...' if len(content) > 40 else '')
            self.title = title
            self.is_new = False
                    
        # Save to database
        self.save_to_db()
                    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all stored messages in conversation history."""
        return self.conversations.copy()
    
    def clear(self):
        """Clear all conversation history but keep system message."""
        # Keep system message if present
        if self.conversations and self.conversations[0].get('role') == 'system':
            system_message = self.conversations[0]
            self.conversations = [system_message]
        else:
            self.conversations = []
            
        # Save cleared state to database
        self.save_to_db()
            
    def set_system_message(self, content: str):
        """
        Set or update the system message.
        
        Args:
            content: The system message content
        """
        system_message = {"role": "system", "content": content}
        
        # Replace existing system message or add at beginning
        if self.conversations and self.conversations[0].get('role') == 'system':
            self.conversations[0] = system_message
        else:
            self.conversations.insert(0, system_message)
            
        # Save to database
        self.save_to_db()
        
    def set_title(self, title: str):
        """Set a custom title for this conversation."""
        self.title = title
        self.save_to_db()
        
    @classmethod
    def list_conversations(cls, db_path: str = "chat_history.db", limit: int = 10) -> List[Dict]:
        """
        List recent conversations from the database.
        
        Args:
            db_path: Path to the database file (kept for backwards compatibility)
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversation metadata dictionaries
        """
        try:
            from .db import list_conversations
            return list_conversations(limit=limit)
        except ImportError:
            # Fall back to SQLite
            if not os.path.exists(db_path):
                return []
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT chat_id, title, created_at, updated_at FROM conversations
            ORDER BY updated_at DESC LIMIT ?
            ''', (limit,))
            
            conversations = []
            for chat_id, title, created_at, updated_at in cursor.fetchall():
                # Count messages
                cursor.execute("SELECT COUNT(*) FROM messages WHERE chat_id = ?", (chat_id,))
                message_count = cursor.fetchone()[0]
                
                conversations.append({
                    "chat_id": chat_id,
                    "title": title,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "message_count": message_count
                })
            
            conn.close()
            return conversations
        
    @classmethod
    def delete_conversation(cls, chat_id: str, db_path: str = "chat_history.db") -> bool:
        """
        Delete a conversation from the database.
        
        Args:
            chat_id: ID of the conversation to delete
            db_path: Path to the database file (kept for backwards compatibility)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from .db import delete_conversation
            return delete_conversation(chat_id)
        except ImportError:
            # Fall back to SQLite
            if not os.path.exists(db_path):
                return False
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            try:
                # Delete messages first (due to foreign key constraint)
                cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
                # Then delete the conversation
                cursor.execute("DELETE FROM conversations WHERE chat_id = ?", (chat_id,))
                conn.commit()
                success = True
            except Exception as e:
                console.print(f"[red]Failed to delete conversation: {e}[/red]")
                conn.rollback()
                success = False
                
            conn.close()
            return success

class SSEMCPClient:
    """Implementation for a SSE-based MCP server."""

    def __init__(self, server_name: str, url: str):
        self.server_name = server_name
        self.url = url
        self.tools = []
        self._streams_context = None
        self._session_context = None
        self.session = None

    async def start(self):
        try:
            self._streams_context = sse_client(url=self.url)
            streams = await self._streams_context.__aenter__()

            self._session_context = ClientSession(*streams)
            self.session = await self._session_context.__aenter__()

            # Initialize
            await self.session.initialize()
            return True
        except Exception as e:
            console.print(f"[red]Server {self.server_name}: SSE connection error: {str(e)}[/red]")
            return False

    async def list_tools(self):
        if not self.session:
            return []
        try:
            response = await self.session.list_tools()
            # Convert pydantic models to dict format
            self.tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                }
                for tool in response.tools
            ]
            return self.tools
        except Exception as e:
            console.print(f"[red]Server {self.server_name}: List tools error: {str(e)}[/red]")
            return []

    async def call_tool(self, tool_name: str, arguments: dict):
        if not self.session:
            return {"error": "Not connected"}
        try:
            response = await self.session.call_tool(tool_name, arguments)
            return response.model_dump() if hasattr(response, 'model_dump') else response
        except Exception as e:
            console.print(f"[red]Server {self.server_name}: Tool call error: {str(e)}[/red]")
            return {"error": str(e)}

    async def stop(self):
        if self.session:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)


class MCPClient:
    """Implementation for a single MCP server."""
    def __init__(self, server_name, command, args=None, env=None):
        self.server_name = server_name
        self.command = command
        self.args = args or []
        self.env = env
        self.process = None
        self.tools = []
        self.request_id = 0
        self.protocol_version = "2024-11-05"
        self.receive_task = None
        self.responses = {}
        self.server_capabilities = {}
        self._shutdown = False
        self._cleanup_lock = asyncio.Lock()

    async def _receive_loop(self):
        if not self.process or self.process.stdout.at_eof():
            return
        try:
            while not self.process.stdout.at_eof():
                line = await self.process.stdout.readline()
                if not line:
                    break
                try:
                    message = json.loads(line.decode().strip())
                    self._process_message(message)
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass

    def _process_message(self, message: dict):
        if "jsonrpc" in message and "id" in message:
            if "result" in message or "error" in message:
                self.responses[message["id"]] = message
            else:
                # request from server, not implemented
                resp = {
                    "jsonrpc": "2.0",
                    "id": message["id"],
                    "error": {
                        "code": -32601,
                        "message": f"Method {message.get('method')} not implemented in client"
                    }
                }
                asyncio.create_task(self._send_message(resp))
        elif "jsonrpc" in message and "method" in message and "id" not in message:
            # notification from server
            pass

    async def start(self):
        expanded_args = []
        for a in self.args:
            if isinstance(a, str) and "~" in a:
                expanded_args.append(os.path.expanduser(a))
            else:
                expanded_args.append(a)

        env_vars = os.environ.copy()
        if self.env:
            env_vars.update(self.env)

        try:
            # Check if command exists or is in PATH
            if self.command and self.command.strip():
                # On Windows, check if it's an executable or a command in PATH
                if sys.platform == 'win32':
                    # Remove any trailing spaces from command
                    self.command = self.command.strip()
                    
                    # Check if command exists as is
                    if not os.path.exists(self.command) and not self.command.endswith('.exe'):
                        # Try to find command in PATH
                        from shutil import which
                        cmd_path = which(self.command)
                        if cmd_path:
                            self.command = cmd_path
                        else:
                            console.print(f"[red]Server {self.server_name}: Command '{self.command}' not found in PATH[/red]")
                            return False
            else:
                console.print(f"[red]Server {self.server_name}: Invalid command specified: '{self.command}'[/red]")
                return False
                
            self.process = await asyncio.create_subprocess_exec(
                self.command,
                *expanded_args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env_vars
            )
            self.receive_task = asyncio.create_task(self._receive_loop())
            return await self._perform_initialize()
        except FileNotFoundError as e:
            console.print(f"[red]Server {self.server_name}: Command not found: {self.command}, error: {str(e)}[/red]")
            return False
        except PermissionError as e:
            console.print(f"[red]Server {self.server_name}: Permission denied running: {self.command}, error: {str(e)}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Server {self.server_name}: Failed to start process: {str(e)}[/red]")
            return False

    async def _perform_initialize(self):
        self.request_id += 1
        req_id = self.request_id
        req = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "initialize",
            "params": {
                "protocolVersion": self.protocol_version,
                "capabilities": {"sampling": {}},
                "clientInfo": {
                    "name": "DolphinMCPClient",
                    "version": "1.0.0"
                }
            }
        }
        await self._send_message(req)

        start = asyncio.get_event_loop().time()
        timeout = 10  # Increased timeout to 10 seconds
        while asyncio.get_event_loop().time() - start < timeout:
            if req_id in self.responses:
                resp = self.responses[req_id]
                del self.responses[req_id]
                if "error" in resp:
                    console.print(f"[red]Server {self.server_name}: Initialize error: {resp['error']}[/red]")
                    return False
                if "result" in resp:
                    elapsed = asyncio.get_event_loop().time() - start
                    console.print(f"[green]Server {self.server_name}: Initialized in {elapsed:.2f}s[/green]")
                    note = {"jsonrpc": "2.0", "method": "notifications/initialized"}
                    await self._send_message(note)
                    init_result = resp["result"]
                    self.server_capabilities = init_result.get("capabilities", {})
                    return True
            await asyncio.sleep(0.05)
        console.print(f"[red]Server {self.server_name}: Initialize timed out after {timeout}s[/red]")
        return False

    async def list_tools(self):
        if not self.process:
            return []
        self.request_id += 1
        rid = self.request_id
        req = {
            "jsonrpc": "2.0",
            "id": rid,
            "method": "tools/list",
            "params": {}
        }
        await self._send_message(req)

        start = asyncio.get_event_loop().time()
        timeout = 10  # Increased timeout to 10 seconds
        while asyncio.get_event_loop().time() - start < timeout:
            if rid in self.responses:
                resp = self.responses[rid]
                del self.responses[rid]
                if "error" in resp:
                    console.print(f"[red]Server {self.server_name}: List tools error: {resp['error']}[/red]")
                    return []
                if "result" in resp and "tools" in resp["result"]:
                    elapsed = asyncio.get_event_loop().time() - start
                    console.print(f"[green]Server {self.server_name}: Listed {len(resp['result']['tools'])} tools in {elapsed:.2f}s[/green]")
                    self.tools = resp["result"]["tools"]
                    return self.tools
            await asyncio.sleep(0.05)
        console.print(f"[red]Server {self.server_name}: List tools timed out after {timeout}s[/red]")
        return []

    async def call_tool(self, tool_name: str, arguments: dict):
        if not self.process:
            return {"error": "Not started"}
        self.request_id += 1
        rid = self.request_id
        req = {
            "jsonrpc": "2.0",
            "id": rid,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        await self._send_message(req)

        start = asyncio.get_event_loop().time()
        timeout = 3600  # Increased timeout to 30 seconds
        while asyncio.get_event_loop().time() - start < timeout:
            if rid in self.responses:
                resp = self.responses[rid]
                del self.responses[rid]
                if "error" in resp:
                    console.print(f"[red]Server {self.server_name}: Tool {tool_name} error: {resp['error']}[/red]")
                    return {"error": resp["error"]}
                if "result" in resp:
                    elapsed = asyncio.get_event_loop().time() - start
                    console.print(f"[green]Server {self.server_name}: Tool {tool_name} completed in {elapsed:.2f}s[/green]")
                    return resp["result"]
            await asyncio.sleep(0.01)  # Reduced sleep interval for more responsive streaming
            if asyncio.get_event_loop().time() - start > 5:  # Log warning after 5 seconds
                console.print(f"[yellow]Server {self.server_name}: Tool {tool_name} taking longer than 5s...[/yellow]")
        console.print(f"[red]Server {self.server_name}: Tool {tool_name} timed out after {timeout}s[/red]")
        return {"error": f"Timeout waiting for tool result after {timeout}s"}

    async def _send_message(self, message: dict):
        if not self.process or self._shutdown:
            console.print(f"[red]Server {self.server_name}: Cannot send message - process not running or shutting down[/red]")
            return False
        try:
            data = json.dumps(message) + "\n"
            self.process.stdin.write(data.encode())
            await self.process.stdin.drain()
            return True
        except Exception as e:
            console.print(f"[red]Server {self.server_name}: Error sending message: {str(e)}[/red]")
            return False

    async def stop(self):
        async with self._cleanup_lock:
            if self._shutdown:
                return
            self._shutdown = True

            if self.receive_task and not self.receive_task.done():
                self.receive_task.cancel()
                try:
                    await self.receive_task
                except asyncio.CancelledError:
                    pass

            if self.process:
                try:
                    # Try to send a shutdown notification first
                    try:
                        note = {"jsonrpc": "2.0", "method": "shutdown"}
                        # Only send if stdin is not closed
                        if not self.process.stdin.is_closing():
                            await self._send_message(note)
                            # Give a small window for the process to react
                            await asyncio.sleep(0.5)
                    except Exception:
                        pass

                    # Properly close pipes
                    try:
                        if self.process.stdin and not self.process.stdin.is_closing():
                            self.process.stdin.close()
                            # Wait for close to complete
                            await asyncio.sleep(0.1)
                    except Exception:
                        pass

                    # Try graceful shutdown first
                    try:
                        if self.process.returncode is None:
                            self.process.terminate()
                            # Use a shorter timeout to make cleanup faster
                            await asyncio.wait_for(self.process.wait(), timeout=1.0)
                    except asyncio.TimeoutError:
                        # Force kill if graceful shutdown fails
                        try:
                            if self.process.returncode is None:
                                console.print(f"[yellow]Server {self.server_name}: Force killing process after timeout[/yellow]")
                                self.process.kill()
                                await asyncio.wait_for(self.process.wait(), timeout=1.0)
                        except asyncio.TimeoutError:
                            console.print(f"[red]Server {self.server_name}: Process did not respond to SIGKILL[/red]")
                        except Exception as e:
                            console.print(f"[red]Server {self.server_name}: Error during kill: {str(e)}[/red]")
                    except Exception as e:
                        console.print(f"[red]Server {self.server_name}: Error during termination: {str(e)}[/red]")
                except Exception as e:
                    console.print(f"[red]Server {self.server_name}: Error during process cleanup: {str(e)}[/red]")
                finally:
                    # Make sure we clear the reference to avoid memory leaks
                    self.process = None

    # Alias close to stop for backward compatibility
    async def close(self):
        await self.stop()

    # Add async context manager support
    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

class MCPManager:
    """
    Class to manage MCP servers for one-time initialization.
    This allows reusing the same server connections across multiple interactions.
    """
    def __init__(self, chat_memory: Optional[ChatMemory] = None):
        self.servers = {}
        self.all_functions = []
        self.config = None
        self.models_cfg = []
        self.initialized = False
        self.chat_memory = chat_memory or ChatMemory()

    async def initialize(self, config_path: str = "mcp_config.json"):
        """Initialize MCP servers from config"""
        if self.initialized:
            return True

        # Load config
        self.config = await load_mcp_config_from_file(config_path)
        self.models_cfg = self.config.get("models", [])
        servers_cfg = self.config.get("mcpServers", {})

        # Start servers
        for server_name, conf in servers_cfg.items():
            if "url" in conf:  # SSE server
                client = SSEMCPClient(server_name, conf["url"])
            else:  # Local process-based server
                client = MCPClient(
                    server_name=server_name,
                    command=conf.get("command"),
                    args=conf.get("args", []),
                    env=conf.get("env", {})
                )
            ok = await client.start()
            if not ok:
                console.print(f"[red][WARN] Could not start server {server_name}[/red]")
                continue
            else:
                console.print(f"[green][OK] {server_name}[/green]")

            # gather tools
            tools = await client.list_tools()
            for t in tools:
                input_schema = t.get("inputSchema") or {"type": "object", "properties": {}}
                fn_def = {
                    "name": f"{server_name}_{t['name']}",
                    "description": t.get("description", ""),
                    "parameters": input_schema
                }
                self.all_functions.append(fn_def)

            self.servers[server_name] = client

        if not self.servers:
            console.print("[red]No MCP servers could be started.[/red]")
            return False

        # Add default system message if chat memory is empty
        if not self.chat_memory.conversations:
            default_model = self.get_model_config()
            if default_model:
                system_msg = "You are a helpful assistant."
                if "systemMessage" in default_model:
                    system_msg = default_model["systemMessage"]
                elif "systemMessageFile" in default_model:
                    try:
                        with open(default_model["systemMessageFile"], "r", encoding="utf-8") as f:
                            system_msg = f.read()
                    except Exception as e:
                        console.print(f"[yellow]Failed to read system message file: {e}[/yellow]")
                
                self.chat_memory.set_system_message(system_msg)

        self.initialized = True
        return True

    def get_model_config(self, model_name: Optional[str] = None):
        """Get model configuration by name"""
        chosen_model = None
        if model_name:
            for m in self.models_cfg:
                if m.get("model") == model_name or m.get("title") == model_name:
                    chosen_model = m
                    break
            if not chosen_model:
                # fallback to default or fail
                for m in self.models_cfg:
                    if m.get("default"):
                        chosen_model = m
                        break
        else:
            # if model_name not specified, pick default
            for m in self.models_cfg:
                if m.get("default"):
                    chosen_model = m
                    break
            if not chosen_model and self.models_cfg:
                chosen_model = self.models_cfg[0]
        
        return chosen_model

    async def cleanup(self):
        """Clean up all server connections"""
        # Make a copy of servers to avoid modification during iteration
        servers_to_cleanup = list(self.servers.values())
        
        # First, mark all clients as shutting down to prevent new messages
        for cli in servers_to_cleanup:
            cli._shutdown = True
        
        # Then perform the actual cleanup
        for cli in servers_to_cleanup:
            await cli.stop()
        
        # Clear references to avoid memory leaks
        self.servers = {}
        self.all_functions = []
        self.initialized = False

async def generate_text(conversation: List[Dict], model_cfg: Dict,
                       all_functions: List[Dict], stream: bool = False) -> Union[Dict, AsyncGenerator]:
    """
    Generate text using the specified provider.

    Args:
        conversation: The conversation history
        model_cfg: Configuration for the model
        all_functions: Available functions for the model to call
        stream: Whether to stream the response

    Returns:
        If stream=False: Dict containing assistant_text and tool_calls
        If stream=True: AsyncGenerator yielding chunks of assistant text and tool calls
    """
    provider = model_cfg.get("provider", "").lower()

    if provider == "openai":
        if stream:
            return generate_with_openai(conversation, model_cfg, all_functions, stream=True)
        else:
            return await generate_with_openai(conversation, model_cfg, all_functions, stream=False)

    # For non-streaming providers, wrap the response in an async generator if streaming is requested
    if stream:
        async def wrap_response():
            if provider == "anthropic":
                result = await generate_with_anthropic(conversation, model_cfg, all_functions)
            elif provider == "ollama":
                result = await generate_with_ollama(conversation, model_cfg, all_functions)
            elif provider == "lmstudio":
                result = await generate_with_lmstudio(conversation, model_cfg, all_functions)
            else:
                result = {"assistant_text": f"Unsupported provider '{provider}'", "tool_calls": []}
            yield result
        return wrap_response()

    # Non-streaming path
    if provider == "anthropic":
        return await generate_with_anthropic(conversation, model_cfg, all_functions)
    elif provider == "ollama":
        return await generate_with_ollama(conversation, model_cfg, all_functions)
    elif provider == "lmstudio":
        return await generate_with_lmstudio(conversation, model_cfg, all_functions)
    else:
        return {"assistant_text": f"Unsupported provider '{provider}'", "tool_calls": []}

async def log_messages_to_file(messages: List[Dict], functions: List[Dict], log_path: str):
    """
    Log messages and function definitions to a JSONL file.

    Args:
        messages: List of messages to log
        functions: List of function definitions
        log_path: Path to the log file
    """
    try:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Append to file
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "messages": messages,
                "functions": functions
            }) + "\n")
    except Exception as e:
        console.print(f"[red]Error logging messages to {log_path}: {str(e)}[/red]")

async def process_tool_call(tc: Dict, servers: Dict[str, MCPClient], quiet_mode: bool) -> Optional[Dict]:
    """Process a single tool call and return the result"""
    func_name = tc["function"]["name"]
    func_args_str = tc["function"].get("arguments", "{}")
    try:
        func_args = json.loads(func_args_str)
    except:
        func_args = {}

    parts = func_name.split("_", 1)
    if len(parts) != 2:
        return {
            "role": "tool",
            "tool_call_id": tc["id"],
            "name": func_name,
            "content": json.dumps({"error": "Invalid function name format"})
        }

    srv_name, tool_name = parts
    if not quiet_mode:
        console.print(f"\n[cyan]View result from {tool_name} from {srv_name} {json.dumps(func_args)}[/cyan]")
    else:
        console.print(f"\n[cyan]Processing tool call...{tool_name}[/cyan]")

    if srv_name not in servers:
        return {
            "role": "tool",
            "tool_call_id": tc["id"],
            "name": func_name,
            "content": json.dumps({"error": f"Unknown server: {srv_name}"})
        }

    # Get the tool's schema
    tool_schema = None
    for tool in servers[srv_name].tools:
        if tool["name"] == tool_name:
            tool_schema = tool.get("inputSchema", {})
            break

    if tool_schema:
        # Ensure required parameters are present
        required_params = tool_schema.get("required", [])
        for param in required_params:
            if param not in func_args:
                return {
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "name": func_name,
                    "content": json.dumps({"error": f"Missing required parameter: {param}"})
                }

    result = await servers[srv_name].call_tool(tool_name, func_args)
    if not quiet_mode:
        console.print(f"[green]{json.dumps(result, indent=2)}[/green]")

    return {
        "role": "tool",
        "tool_call_id": tc["id"],
        "name": func_name,
        "content": json.dumps(result)
    }

async def run_interaction(
    user_query: str,
    model_name: Optional[str] = None,
    config: Optional[dict] = None,
    config_path: str = "mcp_config.json",
    quiet_mode: bool = False,
    log_messages_path: Optional[str] = None,
    stream: bool = False,
    mcp_manager: Optional[MCPManager] = None
) -> Union[str, AsyncGenerator[str, None]]:
    """
    Run an interaction with the MCP servers.

    Args:
        user_query: The user's query
        model_name: Name of the model to use (optional)
        config: Configuration dict (optional, if not provided will load from config_path)
        config_path: Path to the configuration file (default: mcp_config.json)
        quiet_mode: Whether to suppress intermediate output (default: False)
        log_messages_path: Path to log messages in JSONL format (optional)
        stream: Whether to stream the response (default: False)
        mcp_manager: Optional MCPManager for reusing initialized servers

    Returns:
        If stream=False: The final text response
        If stream=True: AsyncGenerator yielding chunks of the response
    """
    # Use existing MCPManager or create a new one for single use
    using_external_manager = mcp_manager is not None
    servers = {}
    all_functions = []
    cleanup_required = not using_external_manager
    
    if mcp_manager and mcp_manager.initialized:
        # Use existing initialized manager
        servers = mcp_manager.servers
        all_functions = mcp_manager.all_functions
        chosen_model = mcp_manager.get_model_config(model_name)
    else:
        # 1) If config is not provided, load from file:
        if config is None:
            config = await load_mcp_config_from_file(config_path)

        servers_cfg = config.get("mcpServers", {})
        models_cfg = config.get("models", [])

        # 2) Choose a model
        chosen_model = None
        if model_name:
            for m in models_cfg:
                if m.get("model") == model_name or m.get("title") == model_name:
                    chosen_model = m
                    break
            if not chosen_model:
                # fallback to default or fail
                for m in models_cfg:
                    if m.get("default"):
                        chosen_model = m
                        break
        else:
            # if model_name not specified, pick default
            for m in models_cfg:
                if m.get("default"):
                    chosen_model = m
                    break
            if not chosen_model and models_cfg:
                chosen_model = models_cfg[0]

        if not chosen_model:
            error_msg = "No suitable model found in config."
            if stream:
                async def error_gen():
                    yield error_msg
                return error_gen()
            return error_msg

        # 3) Start servers (only if not using external manager)
        if not using_external_manager:
            for server_name, conf in servers_cfg.items():
                if "url" in conf:  # SSE server
                    client = SSEMCPClient(server_name, conf["url"])
                else:  # Local process-based server
                    client = MCPClient(
                        server_name=server_name,
                        command=conf.get("command"),
                        args=conf.get("args", []),
                        env=conf.get("env", {})
                    )
                ok = await client.start()
                if not ok:
                    if not quiet_mode:
                        console.print(f"[red][WARN] Could not start server {server_name}[/red]")
                    continue
                else:
                    console.print(f"[green][OK] {server_name}[/green]")

                # gather tools
                tools = await client.list_tools()
                for t in tools:
                    input_schema = t.get("inputSchema") or {"type": "object", "properties": {}}
                    fn_def = {
                        "name": f"{server_name}_{t['name']}",
                        "description": t.get("description", ""),
                        "parameters": input_schema
                    }
                    all_functions.append(fn_def)

                servers[server_name] = client

    if not servers:
        error_msg = "No MCP servers could be started."
        if stream:
            async def error_gen():
                yield error_msg
            return error_gen()
        return error_msg

    # Initialize conversation history
    if mcp_manager and mcp_manager.chat_memory:
        # Use existing chat memory if available
        conversation = mcp_manager.chat_memory.get_messages()
        # Add the current user query
        conversation.append({"role": "user", "content": user_query})
        mcp_manager.chat_memory.add_message({"role": "user", "content": user_query})
    else:
        # Build new conversation history
        conversation = []
        
        # Get system message - either from systemMessageFile, systemMessage, or default
        system_msg = "You are a helpful assistant."
        if "systemMessageFile" in chosen_model:
            try:
                with open(chosen_model["systemMessageFile"], "r", encoding="utf-8") as f:
                    system_msg = f.read()
            except Exception as e:
                console.print(f"[yellow]Failed to read system message file: {e}[/yellow]")
                # Fall back to direct systemMessage if available
                conversation.append({"role": "system", "content": chosen_model.get("systemMessage", system_msg)})
        else:
            conversation.append({"role": "system", "content": chosen_model.get("systemMessage", system_msg)})
        if "systemMessageFiles" in chosen_model:
            for file in chosen_model["systemMessageFiles"]:
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        system_msg = f.read()
                        conversation.append({"role": "system", "content": "File: " + file + "\n" + system_msg})
                except Exception as e:
                    console.print(f"[yellow]Failed to read system message file: {e}[/yellow]")

        conversation.append({"role": "user", "content": user_query})

    async def cleanup():
        """Clean up servers and log messages"""
        if log_messages_path:
            await log_messages_to_file(conversation, all_functions, log_messages_path)
        # Only clean up servers if we created them in this function call
        if cleanup_required:
            # Make a copy of servers to avoid modification during iteration
            servers_to_cleanup = list(servers.values())
            
            # First mark all as shutting down
            for cli in servers_to_cleanup:
                cli._shutdown = True
                
            # Then perform the actual cleanup
            for cli in servers_to_cleanup:
                await cli.stop()

    if stream:
        async def stream_response():
            try:
                while True:  # Main conversation loop
                    generator = await generate_text(conversation, chosen_model, all_functions, stream=True)
                    accumulated_text = ""
                    tool_calls_processed = False
                    
                    async for chunk in await generator:
                        if chunk.get("is_chunk", False):
                            # Immediately yield each token without accumulation
                            if chunk.get("token", False):
                                yield chunk["assistant_text"]
                            accumulated_text += chunk["assistant_text"]
                        else:
                            # This is the final chunk with tool calls
                            if accumulated_text != chunk["assistant_text"]:
                                # If there's any remaining text, yield it
                                remaining = chunk["assistant_text"][len(accumulated_text):]
                                if remaining:
                                    yield remaining
                            
                            # Process any tool calls from the final chunk
                            tool_calls = chunk.get("tool_calls", [])
                            if tool_calls:
                                # Add type field to each tool call
                                for tc in tool_calls:
                                    tc["type"] = "function"
                                # Add the assistant's message with tool calls
                                assistant_message = {
                                    "role": "assistant",
                                    "content": chunk["assistant_text"],
                                    "tool_calls": tool_calls
                                }
                                conversation.append(assistant_message)
                                if mcp_manager and mcp_manager.chat_memory:
                                    mcp_manager.chat_memory.add_message(assistant_message)
                                
                                # Process each tool call
                                for tc in tool_calls:
                                    if tc.get("function", {}).get("name"):
                                        result = await process_tool_call(tc, servers, quiet_mode)
                                        if result:
                                            conversation.append(result)
                                            if mcp_manager and mcp_manager.chat_memory:
                                                mcp_manager.chat_memory.add_message(result)
                                            tool_calls_processed = True
                    
                    # Break the loop if no tool calls were processed
                    if not tool_calls_processed:
                        break
                    
            finally:
                await cleanup()
        
        return stream_response()
    else:
        try:
            final_text = ""
            while True:
                gen_result = await generate_text(conversation, chosen_model, all_functions, stream=False)
                
                assistant_text = gen_result["assistant_text"]
                final_text = assistant_text
                tool_calls = gen_result.get("tool_calls", [])

                # Add the assistant's message
                assistant_message = {"role": "assistant", "content": assistant_text}
                if tool_calls:
                    # Add type field to each tool call
                    for tc in tool_calls:
                        tc["type"] = "function"
                    assistant_message["tool_calls"] = tool_calls
                
                conversation.append(assistant_message)
                if mcp_manager and mcp_manager.chat_memory:
                    mcp_manager.chat_memory.add_message(assistant_message)
                
                console.print(f"[cyan]Added assistant message: {json.dumps(assistant_message, indent=2)}[/cyan]")

                if not tool_calls:
                    break

                for tc in tool_calls:
                    result = await process_tool_call(tc, servers, quiet_mode)
                    if result:
                        conversation.append(result)
                        if mcp_manager and mcp_manager.chat_memory:
                            mcp_manager.chat_memory.add_message(result)
                        console.print(f"[cyan]Added tool result: {json.dumps(result, indent=2)}[/cyan]")

            return final_text
        finally:
            await cleanup()

async def initialize_mcp(
    config_path: str = "mcp_config.json", 
    quiet_mode: bool = False,
    chat_memory: Optional[ChatMemory] = None,
    chat_id: Optional[str] = None,
    db_path: str = "chat_history.db"
) -> MCPManager:
    """
    Initialize MCP servers and return a manager that can be reused.
    
    Args:
        config_path: Path to the configuration file (default: mcp_config.json)
        quiet_mode: Whether to suppress intermediate output (default: False)
        chat_memory: Optional ChatMemory instance to maintain conversation history
        chat_id: Optional ID to load an existing conversation
        db_path: Path to the database file for conversation persistence
        
    Returns:
        An initialized MCPManager instance
    """
    # Create chat memory if not provided
    if chat_memory is None:
        chat_memory = ChatMemory(chat_id=chat_id, db_path=db_path)
    
    manager = MCPManager(chat_memory=chat_memory)
    success = await manager.initialize(config_path)
    if not success:
        if not quiet_mode:
            console.print("[red]Failed to initialize MCP servers[/red]")
            # Make sure to clean up any partially initialized state
            await manager.cleanup()
    return manager
