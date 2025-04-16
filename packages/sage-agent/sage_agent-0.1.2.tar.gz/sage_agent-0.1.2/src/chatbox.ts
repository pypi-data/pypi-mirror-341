import { Widget } from '@lumino/widgets';
import { PanelLayout } from '@lumino/widgets';
import { Message } from '@lumino/messaging';
import { IChatMessage } from './types';
import { Client } from '@modelcontextprotocol/sdk/client/index';
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse';
import Anthropic from '@anthropic-ai/sdk';

/**
 * ChatBoxWidget: A widget for interacting with Anthropic via a chat interface
 */
export class ChatBoxWidget extends Widget {
  private chatHistory: HTMLDivElement;
  private chatInput: HTMLInputElement;
  private sendButton: HTMLButtonElement;
  private apiKey: string = '';
  private modelName: string = 'claude-3-5-sonnet-20241022';
  private messageHistory: Array<IChatMessage> = [];
  private mcpClient: Client | null = null;
  private anthropicClient: Anthropic | null = null;
  private formattedTools: any[] = [];

  constructor() {
    super();
    this.id = 'sage-ai-chat';
    this.title.label = 'AI Chat';
    this.title.closable = true;
    this.addClass('sage-ai-chatbox');

    // Create layout for the chat box
    const layout = new PanelLayout();
    this.layout = layout;

    // Create chat history container
    const historyContainer = document.createElement('div');
    historyContainer.className = 'sage-ai-history-container';
    this.chatHistory = document.createElement('div');
    this.chatHistory.className = 'sage-ai-chat-history';
    historyContainer.appendChild(this.chatHistory);

    // Create input container with text input and send button
    const inputContainer = document.createElement('div');
    inputContainer.className = 'sage-ai-input-container';

    this.chatInput = document.createElement('input');
    this.chatInput.className = 'sage-ai-chat-input';
    this.chatInput.placeholder = 'Ask your question...';
    this.chatInput.addEventListener('keydown', event => {
      if (event.key === 'Enter' && this.chatInput.value.trim() !== '') {
        this.sendMessage();
      }
    });

    this.sendButton = document.createElement('button');
    this.sendButton.className = 'sage-ai-send-button';
    this.sendButton.textContent = 'Send';
    this.sendButton.addEventListener('click', () => {
      if (this.chatInput.value.trim() !== '') {
        this.sendMessage();
      }
    });

    inputContainer.appendChild(this.chatInput);
    inputContainer.appendChild(this.sendButton);

    // Add history and input containers to the layout
    layout.addWidget(new Widget({ node: historyContainer }));
    layout.addWidget(new Widget({ node: inputContainer }));

    // Add welcome message
    this.addSystemMessage(`Welcome to AI Chat! Using model: ${this.modelName}`);

    // Initialize MCP client
    this.initializeMcpClient();
  }

  /**
   * Initialize MCP client
   */
  private async initializeMcpClient(): Promise<void> {
    try {
      this.mcpClient = new Client({
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

      await this.mcpClient.connect(transport);
      this.addSystemMessage('Connected to MCP server successfully.');

      // Get tools from server capabilities
      const capabilities = (await this.mcpClient.listTools()) as any;
      console.log('Available MCP tools:', capabilities);

      this.formattedTools = [];
      for (const tool of capabilities.tools) {
        this.formattedTools.push({
          name: tool.name,
          description: tool.description,
          input_schema: tool.inputSchema
        });
      }

      this.addSystemMessage(
        `Loaded ${this.formattedTools.length} tools from MCP server.`
      );
    } catch (error) {
      console.error('Failed to connect to MCP server:', error);
      this.addSystemMessage(
        '❌ Failed to connect to MCP server. Some features may not work.'
      );
    }
  }

  /**
   * Update available tools from MCP server
   */
  private async updateAvailableTools(): Promise<void> {
    try {
      if (!this.mcpClient) {
        await this.initializeMcpClient();
        if (!this.mcpClient) {
          throw new Error('Failed to initialize MCP client');
        }
      }

      const capabilities = (await this.mcpClient.listTools()) as any;
      console.log('Available MCP tools:', capabilities);

      this.formattedTools = [];
      for (const tool of capabilities.tools) {
        this.formattedTools.push({
          name: tool.name,
          description: tool.description,
          input_schema: tool.inputSchema
        });
      }

      console.log(
        `Updated ${this.formattedTools.length} tools from MCP server.`
      );
    } catch (error) {
      console.error('Failed to update tools:', error);
      throw new Error(
        `Failed to update tools: ${error instanceof Error ? error.message : String(error)}`
      );
    }
  }

  /**
   * Execute a tool call
   */
  private async executeTool(
    toolName: string,
    toolArgs: any,
    toolId: string,
    maxRetries = 3
  ): Promise<any> {
    let retries = 0;

    while (retries <= maxRetries) {
      try {
        if (!this.mcpClient) {
          throw new Error('MCP client not initialized');
        }

        console.log(`Executing tool ${toolName} with args:`, toolArgs);

        // Format tool arguments properly based on the tool name and expected schema
        const formattedArgs: Record<string, any> = { name: toolName };

        // Add all properties from toolArgs as top-level parameters
        if (toolArgs && typeof toolArgs === 'object') {
          Object.entries(toolArgs).forEach(([key, value]) => {
            formattedArgs[key] = value;
          });
        }

        console.log('Formatted tool args:', formattedArgs);

        // Call the tool with properly formatted arguments
        const result = await this.mcpClient.callTool({
          name: toolName,
          arguments: { ...toolArgs }
        });

        console.log(`Tool ${toolName} returned:`, result);

        // Format the tool result for Claude - ensuring content is a string and tool_use_id is preserved exactly
        return {
          type: 'tool_result',
          tool_use_id: toolId,
          content:
            typeof result === 'object' ? JSON.stringify(result) : String(result)
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
  }

  /**
   * Add a tool execution result to the chat history
   */
  private addToolResult(toolName: string, result: any): void {
    const resultContainer = document.createElement('div');
    resultContainer.className = 'sage-ai-tool-result';

    const resultHeader = document.createElement('div');
    resultHeader.className = 'sage-ai-tool-result-header';
    resultHeader.innerHTML = `<strong>Tool Result (${toolName}):</strong>`;
    resultContainer.appendChild(resultHeader);

    const resultContent = document.createElement('pre');
    resultContent.className = 'sage-ai-tool-result-content';
    resultContent.textContent = JSON.stringify(result, null, 2);
    resultContainer.appendChild(resultContent);

    this.chatHistory.appendChild(resultContainer);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
  }

  /**
   * Get the last cell info to augment the query
   */
  private async getLastCellInfo(): Promise<string> {
    if (!this.mcpClient) {
      return '';
    }

    try {
      const lastCellInfo = (await this.mcpClient.callTool({
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

  /**
   * Send a message to the Anthropic API
   */
  private async sendMessage(): Promise<void> {
    const message = this.chatInput.value.trim();
    if (!message) {
      return;
    }

    // Clear the input and focus it for the next message
    this.chatInput.value = '';
    this.chatInput.focus();

    if (!this.apiKey) {
      this.addSystemMessage(
        '❌ API key is not set. Please configure it in the settings.'
      );
      return;
    }

    if (!this.anthropicClient) {
      this.setApiKey(this.apiKey); // Initialize the client if it doesn't exist
    }

    // Augment query with last cell info
    let augmentedMessage = message;
    try {
      const cellInfo = await this.getLastCellInfo();
      if (cellInfo) {
        augmentedMessage += cellInfo;
        console.log('Augmented message with cell info:', augmentedMessage);
      }
    } catch (error) {
      console.warn('Failed to augment message:', error);
    }

    // Display the user message in the UI
    this.addUserMessage(message); // Show original message to the user

    // Start with loading indicator
    const loadingElement = document.createElement('div');
    loadingElement.className = 'sage-ai-message sage-ai-loading';
    loadingElement.textContent = 'AI is thinking...';
    this.chatHistory.appendChild(loadingElement);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;

    // Initialize messages with the user query
    const messages: Array<any> = [{ role: 'user', content: augmentedMessage }];

    try {
      // Ensure tools are up to date
      await this.updateAvailableTools();

      // Process conversation with tool calls
      const finalText: string[] = [];
      let response = await this.callClaude(messages);

      // Process responses until there are no more tool calls
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const assistantMessageContent: any[] = [];
        let hasToolCall = false;

        if (response.content && response.content.length > 0) {
          for (const content of response.content) {
            if (content.type === 'text') {
              console.log('Received text response from Claude');
              finalText.push(content.text);
              assistantMessageContent.push(content);
            } else if (content.type === 'tool_use') {
              hasToolCall = true;
              const toolName = content.name;
              const toolArgs = content.input;
              console.log(`Claude wants to use tool: ${toolName}`);

              // Add the tool call to displayed text
              const toolCallText = `[Calling tool ${toolName} with args ${JSON.stringify(toolArgs)}]`;
              finalText.push(toolCallText);

              // Show the tool call in the UI
              this.addToolCalls([
                {
                  id: content.id,
                  name: content.name,
                  input: content.input
                }
              ]);

              // Add the assistant's message with tool call to the conversation
              assistantMessageContent.push(content);
              messages.push({
                role: 'assistant',
                content: assistantMessageContent
              });

              // Execute the tool and get results
              const toolResult = await this.executeTool(
                toolName,
                toolArgs,
                content.id
              );

              // Show the tool result in the UI
              this.addToolResult(toolName, toolResult.content);

              messages.push({
                role: 'user',
                content: [toolResult]
              });

              // Get a new response from Claude with the tool results
              try {
                response = await this.callClaude(messages);
              } catch (error) {
                finalText.push(
                  `Error from Claude API: ${error instanceof Error ? error.message : String(error)}`
                );
                break;
              }

              break; // Process one tool at a time
            }
          }
        }

        // Break the loop if no tool calls were made in this iteration
        if (!hasToolCall) {
          // Add the final AI response to the UI if not already added
          if (assistantMessageContent.length > 0) {
            const textResponses = assistantMessageContent
              .filter(c => c.type === 'text')
              .map(c => c.text);

            if (textResponses.length > 0) {
              this.addAIResponse(textResponses.join('\n\n'));
            }
          }
          break;
        }
      }

      // Remove the loading indicator
      if (this.chatHistory.contains(loadingElement)) {
        this.chatHistory.removeChild(loadingElement);
      }
    } catch (error) {
      // Remove loading indicator
      if (loadingElement.parentNode === this.chatHistory) {
        this.chatHistory.removeChild(loadingElement);
      }

      // Show error message
      this.addSystemMessage(
        `❌ ${error instanceof Error ? error.message : 'An error occurred while communicating with the AI service.'}`
      );
    }
  }

  /**
   * Call Claude API
   */
  private async callClaude(messages: any[]): Promise<any> {
    if (!this.anthropicClient) {
      throw new Error('Anthropic client not initialized');
    }

    // Only send the last 15 messages to avoid token limits
    const recentMessages = messages.slice(-15);

    const response = await this.anthropicClient.messages.create({
      model: this.modelName,
      max_tokens: 4096,
      messages: recentMessages,
      tools: this.formattedTools.length > 0 ? this.formattedTools : undefined
    });

    console.log('Anthropic response:', response);
    return response;
  }

  /**
   * Handle a message after the widget is shown.
   */
  protected onAfterShow(msg: Message): void {
    this.chatInput.focus();
  }

  /**
   * Set the API key
   */
  setApiKey(apiKey: string): void {
    this.apiKey = apiKey;

    // Initialize Anthropic client with the new API key
    if (apiKey) {
      this.anthropicClient = new Anthropic({
        apiKey: apiKey,
        dangerouslyAllowBrowser: true
      });
      this.addSystemMessage('API key configured successfully.');
    } else {
      this.anthropicClient = null;
      this.addSystemMessage(
        '⚠️ No API key set. Please configure it in the settings.'
      );
    }
  }

  /**
   * Set the model name
   */
  setModelName(model: string): void {
    if (model && model !== this.modelName) {
      this.modelName = model;
      this.addSystemMessage(`Model changed to: ${this.modelName}`);
    }
  }

  /**
   * Add a user message to the chat history
   */
  private addUserMessage(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-user-message';
    messageElement.innerHTML = `<strong>You:</strong> ${message}`;
    this.chatHistory.appendChild(messageElement);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;

    // Add to message history for context
    this.messageHistory.push({ role: 'user', content: message });
  }

  /**
   * Add an AI response to the chat history
   */
  private addAIResponse(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-ai-message';
    messageElement.innerHTML = `<strong>AI:</strong> ${message}`;
    this.chatHistory.appendChild(messageElement);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;

    // Add to message history for context
    this.messageHistory.push({ role: 'assistant', content: message });
  }

  /**
   * Add tool calls to the chat history
   */
  private addToolCalls(toolCalls: any[]): void {
    if (!toolCalls || toolCalls.length === 0) {
      return;
    }

    const toolCallContainer = document.createElement('div');
    toolCallContainer.className = 'sage-ai-tool-calls';

    const toolCallHeader = document.createElement('div');
    toolCallHeader.className = 'sage-ai-tool-calls-header';
    toolCallHeader.innerHTML = '<strong>Tool Calls:</strong>';
    toolCallContainer.appendChild(toolCallHeader);

    toolCalls.forEach((toolCall, index) => {
      const toolCallElement = document.createElement('div');
      toolCallElement.className = 'sage-ai-tool-call';

      const toolCallBadge = document.createElement('span');
      toolCallBadge.className = 'sage-ai-tool-call-badge';
      toolCallBadge.textContent = toolCall.name || 'Unknown Tool';

      const toolCallContent = document.createElement('pre');
      toolCallContent.className = 'sage-ai-tool-call-content';
      toolCallContent.textContent = JSON.stringify(
        toolCall.input || {},
        null,
        2
      );

      toolCallElement.appendChild(toolCallBadge);
      toolCallElement.appendChild(toolCallContent);
      toolCallContainer.appendChild(toolCallElement);

      // Log tool calls as required
      console.log(`Tool Call ${index + 1}:`, toolCall);
    });

    this.chatHistory.appendChild(toolCallContainer);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
  }

  /**
   * Add a system message to the chat history
   */
  private addSystemMessage(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-system-message';
    messageElement.textContent = message;
    this.chatHistory.appendChild(messageElement);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
  }
}
