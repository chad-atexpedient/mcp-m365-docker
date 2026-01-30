#!/usr/bin/env python3
"""
MCP Server for Microsoft 365 Integration
"""
import os
import logging
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
from msal import ConfidentialClientApplication
from msgraph import GraphServiceClient
from azure.identity import ClientSecretCredential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/mcp_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class M365MCPServer:
    def __init__(self):
        self.server = Server("mcp-m365")
        self.graph_client: Optional[GraphServiceClient] = None
        self.setup_handlers()
        
    def get_graph_client(self):
        """Initialize Microsoft Graph client"""
        if self.graph_client is None:
            client_id = os.getenv("AZURE_CLIENT_ID")
            client_secret = os.getenv("AZURE_CLIENT_SECRET")
            tenant_id = os.getenv("AZURE_TENANT_ID")
            
            if not all([client_id, client_secret, tenant_id]):
                raise ValueError("Azure credentials not configured")
            
            credential = ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
            self.graph_client = GraphServiceClient(credential)
        
        return self.graph_client
    
    def setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="list_emails",
                    description="List recent emails from Outlook",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "top": {
                                "type": "number",
                                "description": "Number of emails to retrieve",
                                "default": 10
                            }
                        }
                    }
                ),
                Tool(
                    name="get_calendar_events",
                    description="Get upcoming calendar events",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "days": {
                                "type": "number",
                                "description": "Number of days to look ahead",
                                "default": 7
                            }
                        }
                    }
                ),
                Tool(
                    name="list_teams",
                    description="List Microsoft Teams the user is a member of",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_user_profile",
                    description="Get current user's profile information",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            try:
                if name == "list_emails":
                    return await self.list_emails(arguments.get("top", 10))
                elif name == "get_calendar_events":
                    return await self.get_calendar_events(arguments.get("days", 7))
                elif name == "list_teams":
                    return await self.list_teams()
                elif name == "get_user_profile":
                    return await self.get_user_profile()
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def list_emails(self, top: int) -> list[TextContent]:
        """List recent emails"""
        try:
            graph = self.get_graph_client()
            messages = await graph.me.messages.get(top=top)
            
            result = "Recent Emails:\n\n"
            for msg in messages.value[:top]:
                result += f"From: {msg.from_.email_address.address}\n"
                result += f"Subject: {msg.subject}\n"
                result += f"Received: {msg.received_date_time}\n"
                result += "-" * 50 + "\n"
            
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error retrieving emails: {str(e)}")]
    
    async def get_calendar_events(self, days: int) -> list[TextContent]:
        """Get upcoming calendar events"""
        try:
            graph = self.get_graph_client()
            events = await graph.me.calendar.events.get()
            
            result = f"Calendar Events (next {days} days):\n\n"
            for event in events.value:
                result += f"Subject: {event.subject}\n"
                result += f"Start: {event.start.date_time}\n"
                result += f"End: {event.end.date_time}\n"
                result += "-" * 50 + "\n"
            
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error retrieving events: {str(e)}")]
    
    async def list_teams(self) -> list[TextContent]:
        """List Microsoft Teams"""
        try:
            graph = self.get_graph_client()
            teams = await graph.me.joined_teams.get()
            
            result = "Microsoft Teams:\n\n"
            for team in teams.value:
                result += f"Team: {team.display_name}\n"
                result += f"Description: {team.description or 'N/A'}\n"
                result += "-" * 50 + "\n"
            
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error retrieving teams: {str(e)}")]
    
    async def get_user_profile(self) -> list[TextContent]:
        """Get user profile"""
        try:
            graph = self.get_graph_client()
            user = await graph.me.get()
            
            result = "User Profile:\n\n"
            result += f"Name: {user.display_name}\n"
            result += f"Email: {user.mail or user.user_principal_name}\n"
            result += f"Job Title: {user.job_title or 'N/A'}\n"
            result += f"Office Location: {user.office_location or 'N/A'}\n"
            
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error retrieving profile: {str(e)}")]
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

async def main():
    logger.info("Starting MCP M365 Server...")
    server = M365MCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
