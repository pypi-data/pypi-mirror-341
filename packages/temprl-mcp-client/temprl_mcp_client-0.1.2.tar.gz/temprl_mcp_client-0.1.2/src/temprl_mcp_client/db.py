"""
Database operations for PostgreSQL integration with ChatMemory.
"""

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Optional, Any
from datetime import datetime

# Get PostgreSQL connection parameters from environment variables
def get_postgres_config():
    """Get PostgreSQL connection parameters from environment variables."""
    return {
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': os.environ.get('POSTGRES_PORT', '5432'),
        'database': os.environ.get('POSTGRES_DB', 'temprl_mcp'),
        'user': os.environ.get('POSTGRES_USER', 'postgres'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'password')
    }

def get_connection():
    """Get a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(**get_postgres_config())
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

def init_db():
    """Initialize the database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create conversations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            chat_id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            metadata JSONB DEFAULT '{}'
        )
        ''')
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            chat_id TEXT,
            index_num INTEGER,
            role TEXT,
            content TEXT,
            tool_calls JSONB,
            timestamp TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES conversations (chat_id) ON DELETE CASCADE
        )
        ''')
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def save_conversation(chat_id: str, title: str, created_at: str, updated_at: str, metadata: Dict = None):
    """Save or update conversation metadata in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO conversations (chat_id, title, created_at, updated_at, metadata)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (chat_id) DO UPDATE SET
            title = EXCLUDED.title,
            updated_at = EXCLUDED.updated_at,
            metadata = EXCLUDED.metadata
        ''', (chat_id, title, created_at, updated_at, json.dumps(metadata or {})))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error saving conversation: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def load_conversation(chat_id: str) -> Optional[Dict]:
    """Load conversation metadata from the database."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('''
        SELECT chat_id, title, created_at, updated_at, metadata
        FROM conversations
        WHERE chat_id = %s
        ''', (chat_id,))
        
        result = cursor.fetchone()
        if result is None:
            # Explicit handling when the conversation is not found
            return None
            
        return dict(result)
    except Exception as e:
        print(f"Error loading conversation: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def save_messages(chat_id: str, messages: List[Dict]):
    """Save messages for a conversation, replacing any existing messages."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Delete existing messages for this chat
        cursor.execute("DELETE FROM messages WHERE chat_id = %s", (chat_id,))
        
        # Insert all messages
        for i, message in enumerate(messages):
            role = message.get("role", "")
            content = message.get("content", "")
            tool_calls = json.dumps(message.get("tool_calls", [])) if "tool_calls" in message else None
            timestamp = datetime.now().isoformat()
            
            cursor.execute('''
            INSERT INTO messages (chat_id, index_num, role, content, tool_calls, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (chat_id, i, role, content, tool_calls, timestamp))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error saving messages: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def load_messages(chat_id: str) -> List[Dict]:
    """Load messages for a conversation from the database."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('''
        SELECT role, content, tool_calls
        FROM messages
        WHERE chat_id = %s
        ORDER BY index_num
        ''', (chat_id,))
        
        messages = []
        for row in cursor.fetchall():
            message = {"role": row["role"], "content": row["content"]}
            
            # Add tool calls if present
            if row["tool_calls"]:
                message["tool_calls"] = row["tool_calls"]
                
            messages.append(message)
            
        return messages
    except Exception as e:
        print(f"Error loading messages: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def list_conversations(limit: int = 10) -> List[Dict]:
    """List recent conversations from the database."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('''
        SELECT c.chat_id, c.title, c.created_at, c.updated_at, COUNT(m.id) as message_count
        FROM conversations c
        LEFT JOIN messages m ON c.chat_id = m.chat_id
        GROUP BY c.chat_id, c.title, c.created_at, c.updated_at
        ORDER BY c.updated_at DESC
        LIMIT %s
        ''', (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error listing conversations: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def delete_conversation(chat_id: str) -> bool:
    """Delete a conversation and its messages from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # PostgreSQL will automatically delete messages due to CASCADE
        cursor.execute("DELETE FROM conversations WHERE chat_id = %s", (chat_id,))
        row_count = cursor.rowcount
        conn.commit()
        return row_count > 0
    except Exception as e:
        conn.rollback()
        print(f"Error deleting conversation: {e}")
        return False
    finally:
        cursor.close()
        conn.close() 