/**
 * Interface for chat message
 */
export interface IChatMessage {
  role: string;
  content: string;
}

/**
 * Interface for tool call
 */
export interface IToolCall {
  id: string;
  name: string;
  input: any;
}

/**
 * Interface for tool result
 */
export interface IToolResult {
  type: string;
  tool_use_id: string;
  content: string;
}

/**
 * Interface for message handler events
 */
export interface IMessageHandlers {
  onUserMessage?: (message: string) => void;
  onAIResponse?: (message: string) => void;
  onSystemMessage?: (message: string) => void;
  onErrorMessage?: (message: string) => void;
  onToolCall?: (toolCalls: IToolCall[]) => void;
  onToolResult?: (toolName: string, result: any) => void;
}

/**
 * Chat request status
 */
export enum ChatRequestStatus {
  IDLE = 'idle',
  PENDING = 'pending',
  RETRYING = 'retrying',
  COMPLETED = 'completed',
  ERROR = 'error',
  CANCELLED = 'cancelled'
}
