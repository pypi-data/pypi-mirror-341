import { Widget } from '@lumino/widgets';
import { PanelLayout } from '@lumino/widgets';
import { Message } from '@lumino/messaging';
import { ChatMessages } from './ChatMessages';
import { AnthropicService } from './AnthropicService';
import { ToolService } from './ToolService';
import { ChatRequestStatus } from './types';

/**
 * ChatBoxWidget: A widget for interacting with Anthropic via a chat interface
 */
export class ChatBoxWidget extends Widget {
  private chatHistory: HTMLDivElement;
  private chatInput: HTMLInputElement;
  private sendButton: HTMLButtonElement;
  private resetButton: HTMLButtonElement;

  // Chat services
  private messageComponent: ChatMessages;
  private anthropicService: AnthropicService;
  private toolService: ToolService;

  // State tracking
  private isProcessingMessage: boolean = false;
  private loadingIndicator: HTMLDivElement | null = null;

  constructor() {
    super();
    this.id = 'sage-ai-chat';
    this.title.label = 'AI Chat';
    this.title.closable = true;
    this.addClass('sage-ai-chatbox');

    // Initialize services
    this.anthropicService = new AnthropicService();
    this.toolService = new ToolService();

    // Create layout for the chat box
    const layout = new PanelLayout();
    this.layout = layout;

    // Create toolbar
    const toolbar = document.createElement('div');
    toolbar.className = 'sage-ai-toolbar';

    // Create reset button
    this.resetButton = document.createElement('button');
    this.resetButton.className = 'sage-ai-reset-button';
    this.resetButton.textContent = 'Reset Chat';
    this.resetButton.addEventListener('click', () => this.resetChat());
    toolbar.appendChild(this.resetButton);

    // Create chat history container
    const historyContainer = document.createElement('div');
    historyContainer.className = 'sage-ai-history-container';
    this.chatHistory = document.createElement('div');
    this.chatHistory.className = 'sage-ai-chat-history';
    historyContainer.appendChild(this.chatHistory);

    // Initialize message component
    this.messageComponent = new ChatMessages(this.chatHistory);

    // Create input container with text input and send button
    const inputContainer = document.createElement('div');
    inputContainer.className = 'sage-ai-input-container';

    this.chatInput = document.createElement('input');
    this.chatInput.className = 'sage-ai-chat-input';
    this.chatInput.placeholder = 'Ask your question...';
    this.chatInput.addEventListener('keydown', event => {
      if (
        event.key === 'Enter' &&
        this.chatInput.value.trim() !== '' &&
        !this.isProcessingMessage
      ) {
        this.sendMessage();
      }
    });

    this.sendButton = document.createElement('button');
    this.sendButton.className = 'sage-ai-send-button';
    this.sendButton.textContent = 'Send';
    this.sendButton.addEventListener('click', () => {
      if (this.isProcessingMessage) {
        this.cancelMessage();
      } else if (this.chatInput.value.trim() !== '') {
        this.sendMessage();
      }
    });

    inputContainer.appendChild(this.chatInput);
    inputContainer.appendChild(this.sendButton);

    // Add components to the layout
    layout.addWidget(new Widget({ node: toolbar }));
    layout.addWidget(new Widget({ node: historyContainer }));
    layout.addWidget(new Widget({ node: inputContainer }));

    // Add welcome message
    this.messageComponent.addSystemMessage(
      `Welcome to AI Chat! Using model: ${this.anthropicService.getModelName()}`
    );

    // Initialize MCP client
    this.initializeServices();
  }

  /**
   * Initialize all services
   */
  private async initializeServices(): Promise<void> {
    try {
      await this.toolService.initialize();
      this.messageComponent.addSystemMessage(
        'Connected to MCP server successfully.'
      );
      this.messageComponent.addSystemMessage(
        `Loaded ${this.toolService.getTools().length} tools from MCP server.`
      );
    } catch (error) {
      console.error('Failed to connect to MCP server:', error);
      this.messageComponent.addSystemMessage(
        '❌ Failed to connect to MCP server. Some features may not work.'
      );
    }
  }

  /**
   * Reset the chat
   */
  private resetChat(): void {
    // Cancel any ongoing request
    if (this.isProcessingMessage) {
      this.cancelMessage();
    }

    // Clear the message history
    this.messageComponent.clearHistory();

    // Add welcome message
    this.messageComponent.addSystemMessage(
      `Welcome to AI Chat! Using model: ${this.anthropicService.getModelName()}`
    );
  }

  /**
   * Cancel the current message processing
   */
  private cancelMessage(): void {
    if (!this.isProcessingMessage) {
      return;
    }

    this.anthropicService.cancelRequest();
    this.isProcessingMessage = false;

    // Remove loading indicator if present
    if (this.loadingIndicator) {
      this.messageComponent.removeElement(this.loadingIndicator);
      this.loadingIndicator = null;
    }

    this.messageComponent.addSystemMessage('Request cancelled by user.');
    this.updateSendButton(false);
  }

  /**
   * Update the send/cancel button state
   */
  private updateSendButton(isProcessing: boolean): void {
    if (isProcessing) {
      this.sendButton.textContent = 'Cancel';
      this.sendButton.className = 'sage-ai-cancel-button';
    } else {
      this.sendButton.textContent = 'Send';
      this.sendButton.className = 'sage-ai-send-button';
    }
  }

  /**
   * Send a message to the Anthropic API
   */
  private async sendMessage(): Promise<void> {
    const message = this.chatInput.value.trim();
    if (!message || this.isProcessingMessage) {
      return;
    }

    // Set processing state
    this.isProcessingMessage = true;
    this.updateSendButton(true);

    // Clear the input and focus it for the next message
    this.chatInput.value = '';
    this.chatInput.focus();

    if (!this.anthropicService.getRequestStatus()) {
      this.messageComponent.addSystemMessage(
        '❌ API key is not set. Please configure it in the settings.'
      );
      this.isProcessingMessage = false;
      this.updateSendButton(false);
      return;
    }

    // Augment query with last cell info
    let augmentedMessage = message;
    try {
      const cellInfo = await this.toolService.getLastCellInfo();
      if (cellInfo) {
        augmentedMessage += cellInfo;
        console.log('Augmented message with cell info:', augmentedMessage);
      }
    } catch (error) {
      console.warn('Failed to augment message:', error);
    }

    // Display the user message in the UI
    this.messageComponent.addUserMessage(message);

    // Start with loading indicator
    this.loadingIndicator = this.messageComponent.addLoadingIndicator();

    // Initialize messages with the user query
    const messages: Array<any> = [{ role: 'user', content: augmentedMessage }];

    try {
      // Process conversation with tool calls
      await this.processConversation(messages);
    } catch (error) {
      console.error('Error in conversation processing:', error);

      // Only show error if we're not cancelled
      if (
        this.anthropicService.getRequestStatus() !== ChatRequestStatus.CANCELLED
      ) {
        this.messageComponent.addErrorMessage(
          `❌ ${error instanceof Error ? error.message : 'An error occurred while communicating with the AI service.'}`
        );
      }
    } finally {
      // Remove the loading indicator if it still exists
      if (this.loadingIndicator) {
        this.messageComponent.removeElement(this.loadingIndicator);
        this.loadingIndicator = null;
      }

      // Reset state
      this.isProcessingMessage = false;
      this.updateSendButton(false);
    }
  }

  /**
   * Process the conversation with the AI service
   */
  private async processConversation(messages: any[]): Promise<void> {
    // Process conversation with tool calls
    let response;

    try {
      // Call Claude with retry handling
      response = await this.anthropicService.sendMessage(
        messages,
        this.toolService.getTools(),
        async (error, attempt) => {
          // Update UI to show retry status
          if (this.loadingIndicator) {
            this.messageComponent.removeElement(this.loadingIndicator);
          }

          this.messageComponent.addErrorMessage(
            `API request failed: ${error.message}. Retrying in 45 seconds... (Attempt ${attempt})`
          );

          this.loadingIndicator = this.messageComponent.addLoadingIndicator(
            'Waiting to retry...'
          );
        }
      );
    } catch (error) {
      // If cancelled, just return
      if (
        this.anthropicService.getRequestStatus() === ChatRequestStatus.CANCELLED
      ) {
        return;
      }
      throw error;
    }

    // Process responses until there are no more tool calls
    // eslint-disable-next-line no-constant-condition
    while (true) {
      const assistantMessageContent: any[] = [];
      let hasToolCall = false;

      if (response.content && response.content.length > 0) {
        for (const content of response.content) {
          if (content.type === 'text') {
            console.log('Received text response from Claude');
            assistantMessageContent.push(content);
          } else if (content.type === 'tool_use') {
            hasToolCall = true;
            const toolName = content.name;
            const toolArgs = content.input;
            console.log(`Claude wants to use tool: ${toolName}`);

            // Show the tool call in the UI
            this.messageComponent.addToolCalls([
              {
                id: content.id,
                name: content.name,
                input: content.input
              }
            ]);

            // Add the assistant's message with tool call to the conversation
            messages.push({
              role: 'assistant',
              content: [content] // Only include the current tool call
            });

            // Execute the tool and get results
            const toolResult = await this.toolService.executeTool({
              id: content.id,
              name: toolName,
              input: toolArgs
            });

            // Show the tool result in the UI
            this.messageComponent.addToolResult(toolName, toolResult.content);

            // Add the tool result as a user message
            messages.push({
              role: 'user',
              content: [toolResult]
            });

            // Check if we've been cancelled
            if (
              this.anthropicService.getRequestStatus() ===
              ChatRequestStatus.CANCELLED
            ) {
              return;
            }

            // Get a new response from Claude with the tool results
            try {
              // Update loading indicator to show we're processing tool results
              if (this.loadingIndicator) {
                this.messageComponent.removeElement(this.loadingIndicator);
              }
              this.loadingIndicator = this.messageComponent.addLoadingIndicator(
                'Processing tool results...'
              );

              response = await this.anthropicService.sendMessage(
                messages,
                this.toolService.getTools()
              );
            } catch (error) {
              if (
                this.anthropicService.getRequestStatus() ===
                ChatRequestStatus.CANCELLED
              ) {
                return;
              }
              throw error;
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
            this.messageComponent.addAIResponse(textResponses.join('\n\n'));
          }
        }
        break;
      }
    }
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
    this.anthropicService.initialize(apiKey);

    if (apiKey) {
      this.messageComponent.addSystemMessage(
        'API key configured successfully.'
      );
    } else {
      this.messageComponent.addSystemMessage(
        '⚠️ No API key set. Please configure it in the settings.'
      );
    }
  }

  /**
   * Set the model name
   */
  setModelName(model: string): void {
    if (model && model !== this.anthropicService.getModelName()) {
      this.anthropicService.setModelName(model);
      this.messageComponent.addSystemMessage(`Model changed to: ${model}`);
    }
  }
}
