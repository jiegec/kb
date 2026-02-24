# Agentic Chat

## VS Code

1. Run `Chat: Open Chat` command
2. Select `Agent` mode
3. Change model, `Manage Models...` to use other providers
4. Add MCP: `MCP: Add Server`, configure server in `mcp.json`

## Claude Code

1. Use `npx @anthropic-ai/claude-code` to run
2. Add `"hasCompletedOnboarding": true` to `~/.claude.json`
3. Set `ANTHROPIC_BASE_URL` to custom endpoint, `ANTHROPIC_API_KEY` to custom API key, e.g. use DeepSeek platform instead of anthropic; or use `npx @musistudio/claude-code-router ui`, configure [claude-code-router](https://github.com/musistudio/claude-code-router) in ui, for other providers
4. Add MCP: `npx @anthropic-ai/claude-code mcp add [name] --transport [transport] [url]`

## MCP Servers

- [Fetch MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch): `npx @anthropic-ai/claude-code mcp add --scope user fetch pipx run mcp-server-fetch --transport stdio`, disable `WebFetch` using `/permissions` (saved in `~/.claude/settings.json`)
- [Web Search MCP Server](https://github.com/mrkrsl/web-search-mcp) to replace `WebSearch`
