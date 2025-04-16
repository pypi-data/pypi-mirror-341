/**
 * Main entry point for the sage-agent extension
 */

// Export components
export * from './types';
export * from './chatbox';

// Import and re-export plugin
import { plugin } from './plugin';
export default plugin;
