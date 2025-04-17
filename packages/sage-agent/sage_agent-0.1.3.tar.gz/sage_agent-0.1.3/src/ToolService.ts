import { Client } from '@modelcontextprotocol/sdk/client/index';
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse';
import { IToolCall } from './types';

/**
 * Service for handling tool executions and MCP client
 */
export class ToolService {
  private client: Client | null = null;
  private tools: any[] = [];

  /**
   * Initialize the MCP client
   */
  async initialize(): Promise<void> {
    try {
      this.client = new Client({
        name: 'sage-ai-client',
        version: '1.0.0'
      });

      const transport = new SSEClientTransport(
        new URL('/sse', 'http://localhost:3001'),
        {
          requestInit: {
            headers: {
              Accept: 'text/event-stream'
            }
          }
        }
      );

      await this.client.connect(transport);
      await this.refreshTools();

      return;
    } catch (error) {
      console.error('Failed to initialize MCP client:', error);
      throw error;
    }
  }

  /**
   * Refresh available tools from MCP server
   */
  async refreshTools(): Promise<any[]> {
    if (!this.client) {
      throw new Error('MCP client not initialized');
    }

    try {
      const capabilities = (await this.client.listTools()) as any;
      console.log('Available MCP tools:', capabilities);

      this.tools = [];
      for (const tool of capabilities.tools) {
        this.tools.push({
          name: tool.name,
          description: tool.description,
          input_schema: tool.inputSchema
        });
      }

      console.log(`Updated ${this.tools.length} tools from MCP server.`);
      return this.tools;
    } catch (error) {
      console.error('Failed to update tools:', error);
      throw error;
    }
  }

  /**
   * Get available tools
   */
  getTools(): any[] {
    return this.tools;
  }

  /**
   * Execute a tool call
   */
  async executeTool(toolCall: IToolCall, maxRetries = 3): Promise<any> {
    if (!this.client) {
      throw new Error('MCP client not initialized');
    }

    const { name: toolName, input: toolArgs, id: toolId } = toolCall;
    let retries = 0;

    while (retries <= maxRetries) {
      try {
        console.log(`Executing tool ${toolName} with args:`, toolArgs);

        // Call the tool
        const result = await this.client.callTool({
          name: toolName,
          arguments: { ...toolArgs }
        });

        console.log(`Tool ${toolName} returned:`, result);

        // Format the result as a string
        const resultContent =
          typeof result === 'object' ? JSON.stringify(result) : String(result);

        // Return proper tool result format for Claude
        return {
          type: 'tool_result',
          tool_use_id: toolId,
          content: resultContent
        };
      } catch (error) {
        retries++;
        console.error(
          `Tool execution failed (attempt ${retries}/${maxRetries + 1}):`,
          error
        );

        if (retries > maxRetries) {
          return {
            type: 'tool_result',
            tool_use_id: toolId,
            content: `Error: ${error instanceof Error ? error.message : String(error)}`
          };
        }

        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 1000 * retries));
      }
    }

    // This should never happen (while loop ensures it), but TypeScript needs a return
    throw new Error('Tool execution failed after all retries');
  }

  /**
   * Get the last cell info to augment the query
   */
  async getLastCellInfo(): Promise<string> {
    if (!this.client) {
      return '';
    }

    try {
      const lastCellInfo = (await this.client.callTool({
        name: 'get_last_cell_info'
      })) as any;

      console.log('Last cell info:', lastCellInfo);

      if (
        lastCellInfo &&
        lastCellInfo.content &&
        lastCellInfo.content.cell_id
      ) {
        const info = lastCellInfo.content;
        return `\n\n[last_cell_id: ${info.cell_id}]`;
      }
    } catch (error) {
      console.warn('Could not get last cell info:', error);
    }

    return '';
  }
}
