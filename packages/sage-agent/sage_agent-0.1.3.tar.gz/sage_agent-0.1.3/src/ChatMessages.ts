import { IChatMessage, IToolCall } from './types';

/**
 * Component for handling chat message display
 */
export class ChatMessages {
  private container: HTMLDivElement;
  private messageHistory: Array<IChatMessage> = [];

  constructor(container: HTMLDivElement) {
    this.container = container;
  }

  /**
   * Clear all messages from the chat history
   */
  clearHistory(): void {
    this.container.innerHTML = '';
    this.messageHistory = [];
  }

  /**
   * Add a user message to the chat history
   */
  addUserMessage(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-user-message';
    messageElement.innerHTML = `<strong>You:</strong> ${message}`;
    this.container.appendChild(messageElement);
    this.container.scrollTop = this.container.scrollHeight;

    // Add to message history for context
    this.messageHistory.push({ role: 'user', content: message });
  }

  /**
   * Add an AI response to the chat history
   */
  addAIResponse(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-ai-message';
    messageElement.innerHTML = `<strong>AI:</strong> ${message}`;
    this.container.appendChild(messageElement);
    this.container.scrollTop = this.container.scrollHeight;

    // Add to message history for context
    this.messageHistory.push({ role: 'assistant', content: message });
  }

  /**
   * Add a system message to the chat history
   */
  addSystemMessage(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-system-message';
    messageElement.textContent = message;
    this.container.appendChild(messageElement);
    this.container.scrollTop = this.container.scrollHeight;
  }

  /**
   * Add an error message to the chat history
   */
  addErrorMessage(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-error-message';
    messageElement.textContent = message;
    this.container.appendChild(messageElement);
    this.container.scrollTop = this.container.scrollHeight;
  }

  /**
   * Add tool calls to the chat history
   */
  addToolCalls(toolCalls: IToolCall[]): void {
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

      console.log(`Tool Call ${index + 1}:`, toolCall);
    });

    this.container.appendChild(toolCallContainer);
    this.container.scrollTop = this.container.scrollHeight;
  }

  /**
   * Add a tool execution result to the chat history
   */
  addToolResult(toolName: string, result: any): void {
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

    this.container.appendChild(resultContainer);
    this.container.scrollTop = this.container.scrollHeight;
  }

  /**
   * Add a loading indicator to the chat history
   */
  addLoadingIndicator(text: string = 'AI is thinking...'): HTMLDivElement {
    const loadingElement = document.createElement('div');
    loadingElement.className = 'sage-ai-message sage-ai-loading';
    loadingElement.textContent = text;
    this.container.appendChild(loadingElement);
    this.container.scrollTop = this.container.scrollHeight;
    return loadingElement;
  }

  /**
   * Remove an element from the chat history
   */
  removeElement(element: HTMLElement): void {
    if (this.container.contains(element)) {
      this.container.removeChild(element);
    }
  }

  /**
   * Get the message history
   */
  getMessageHistory(): Array<IChatMessage> {
    return this.messageHistory;
  }
}
