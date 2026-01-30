# MCP M365 Docker Platform

A Docker-based platform for running Model Context Protocol (MCP) server with Microsoft 365 integration.

## Features

- 🐳 Fully containerized MCP server
- 📧 Outlook email integration
- 📅 Calendar events access
- 👥 Microsoft Teams integration
- 👤 User profile management
- 🔐 Secure Azure AD authentication

## Prerequisites

- Docker and Docker Compose installed
- Microsoft 365 account
- Azure AD application registration

## Azure AD Setup

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Give it a name (e.g., "MCP M365 Server")
5. Select **Accounts in this organizational directory only**
6. Click **Register**

### Configure API Permissions

Add the following Microsoft Graph permissions:
- `Mail.Read`
- `Calendars.Read`
- `Team.ReadBasic.All`
- `User.Read`

### Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add description and set expiration
4. Copy the secret value (you won't see it again!)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/chad-atexpedient/mcp-m365-docker.git
cd mcp-m365-docker
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Edit `.env` and add your Azure credentials:
```env
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here
AZURE_TENANT_ID=your_tenant_id_here
```

4. Build and run with Docker Compose:
```bash
docker-compose up -d
```

## Usage

### Using Docker Compose (Recommended)

```bash
# Start the server
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the server
docker-compose down
```

### Using Docker directly

```bash
# Build the image
docker build -t mcp-m365 .

# Run the container
docker run -d \
  --name mcp-m365-server \
  -p 8080:8080 \
  -e AZURE_CLIENT_ID=your_client_id \
  -e AZURE_CLIENT_SECRET=your_client_secret \
  -e AZURE_TENANT_ID=your_tenant_id \
  -v $(pwd)/logs:/app/logs \
  mcp-m365
```

## Available MCP Tools

The server exposes the following tools via MCP:

### 1. `list_emails`
List recent emails from Outlook
- **Parameters:**
  - `top` (optional): Number of emails to retrieve (default: 10)

### 2. `get_calendar_events`
Get upcoming calendar events
- **Parameters:**
  - `days` (optional): Number of days to look ahead (default: 7)

### 3. `list_teams`
List Microsoft Teams the user is a member of

### 4. `get_user_profile`
Get current user's profile information

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_CLIENT_ID` | Azure AD application client ID | Yes |
| `AZURE_CLIENT_SECRET` | Azure AD application client secret | Yes |
| `AZURE_TENANT_ID` | Azure AD tenant ID | Yes |
| `MCP_PORT` | Port for MCP server | No (default: 8080) |

### Volumes

- `./logs:/app/logs` - Server logs
- `./data:/app/data` - Persistent data storage
- `./config:/app/config` - Configuration files

## Logs

Logs are stored in the `logs` directory:
```bash
tail -f logs/mcp_server.log
```

## Troubleshooting

### Authentication Errors

If you see authentication errors:
1. Verify your Azure credentials in `.env`
2. Check that API permissions are granted and admin consented
3. Ensure the client secret hasn't expired

### Connection Issues

If the server won't start:
1. Check if port 8080 is already in use
2. View logs: `docker-compose logs`
3. Verify environment variables are set correctly

### Permission Denied

If you get permission errors:
```bash
chmod +x mcp_server.py
```

## Development

To modify the server:

1. Edit `mcp_server.py`
2. Rebuild the container:
```bash
docker-compose up -d --build
```

## Security Notes

- **Never commit** your `.env` file with real credentials
- Rotate your Azure client secrets regularly
- Use least-privilege permissions in Azure AD
- Consider using Azure Key Vault for production deployments

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

## Roadmap

- [ ] Add support for sending emails
- [ ] Calendar event creation
- [ ] Teams message posting
- [ ] SharePoint integration
- [ ] OneDrive file access
- [ ] Health check endpoint
- [ ] Metrics and monitoring
