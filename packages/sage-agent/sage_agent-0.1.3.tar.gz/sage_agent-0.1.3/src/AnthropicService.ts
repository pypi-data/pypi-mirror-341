import Anthropic from '@anthropic-ai/sdk';
import { ChatRequestStatus } from './types';

/**
 * Service for handling Anthropic API interactions
 */
export class AnthropicService {
  private client: Anthropic | null = null;
  private modelName: string = 'claude-3-5-sonnet-20241022';
  private requestStatus: ChatRequestStatus = ChatRequestStatus.IDLE;
  private abortController: AbortController | null = null;

  /**
   * Initialize the Anthropic client
   * @param apiKey API key for authentication
   */
  initialize(apiKey: string): void {
    if (!apiKey) {
      this.client = null;
      return;
    }

    this.client = new Anthropic({
      apiKey,
      dangerouslyAllowBrowser: true
    });
  }

  /**
   * Set the model name
   * @param modelName Name of the model to use
   */
  setModelName(modelName: string): void {
    this.modelName = modelName;
  }

  /**
   * Get the current model name
   */
  getModelName(): string {
    return this.modelName;
  }

  /**
   * Get the current request status
   */
  getRequestStatus(): ChatRequestStatus {
    return this.requestStatus;
  }

  /**
   * Cancel the current request if any
   */
  cancelRequest(): void {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
      this.requestStatus = ChatRequestStatus.CANCELLED;
    }
  }

  /**
   * Send a message to the Anthropic API
   * @param messages The conversation history
   * @param tools Available tools
   * @param onRetry Callback for retry attempts
   */
  async sendMessage(
    messages: any[],
    tools: any[] = [],
    onRetry?: (error: Error, attemptNumber: number) => Promise<void>
  ): Promise<any> {
    if (!this.client) {
      throw new Error('Anthropic client not initialized');
    }

    this.requestStatus = ChatRequestStatus.PENDING;
    this.abortController = new AbortController();

    try {
      // Only send the last 15 messages to avoid token limits
      const recentMessages = messages.slice(-15);

      // Log the exact messages being sent to help debug
      console.log(
        'Sending messages to Claude:',
        JSON.stringify(recentMessages, null, 2)
      );

      const response = await this.client.messages.create({
        model: this.modelName,
        max_tokens: 4096,
        messages: recentMessages,
        tools: tools.length > 0 ? tools : undefined
      });

      console.log('Anthropic response:', response);
      this.requestStatus = ChatRequestStatus.COMPLETED;
      return response;
    } catch (error: any) {
      console.error('Error calling Anthropic API:', error);

      // If the request was cancelled, don't retry
      if (
        error.name === 'AbortError' ||
        this.requestStatus ===
          (ChatRequestStatus.CANCELLED as ChatRequestStatus)
      ) {
        this.requestStatus = ChatRequestStatus.CANCELLED;
        throw new Error('Request cancelled');
      }

      this.requestStatus = ChatRequestStatus.RETRYING;

      if (onRetry) {
        await onRetry(error, 1);

        // Wait for 45 seconds before retry
        await new Promise(resolve => setTimeout(resolve, 45000));

        // Try the request again
        return this.sendMessage(messages, tools, onRetry);
      }

      this.requestStatus = ChatRequestStatus.ERROR;
      throw error;
    }
  }
}
