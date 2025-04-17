import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ICommandPalette, WidgetTracker } from '@jupyterlab/apputils';
import { ChatBoxWidget } from './chatbox';

/**
 * Initialization data for the sage-ai extension.
 */
export const plugin: JupyterFrontEndPlugin<void> = {
  id: 'sage-agent:plugin',
  description: 'Sage AI - Your AI Data Partner',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null
  ) => {
    console.log('JupyterLab extension sage-agent is activated!');

    // Create a widget tracker to keep track of the chat widgets
    const tracker = new WidgetTracker<ChatBoxWidget>({
      namespace: 'sage-ai-chat'
    });

    // Create a new chat widget
    const createChatWidget = () => {
      const chatWidget = new ChatBoxWidget();
      tracker.add(chatWidget);

      // Add the chat widget to the right side panel
      app.shell.add(chatWidget, 'right', { rank: 1000 });

      return chatWidget;
    };

    // Create the initial chat widget
    let chatWidget = createChatWidget();

    // Function to load settings
    const loadSettings = (settings: ISettingRegistry.ISettings) => {
      // Get the API key from the settings
      const apiKey = settings.get('apiKey').composite as string;
      chatWidget.setApiKey(apiKey);

      // Get the model name from the settings
      const modelName = settings.get('modelName').composite as string;
      chatWidget.setModelName(modelName);

      // Listen for setting changes
      settings.changed.connect(() => {
        const updatedApiKey = settings.get('apiKey').composite as string;
        const updatedModelName = settings.get('modelName').composite as string;

        chatWidget.setApiKey(updatedApiKey);
        chatWidget.setModelName(updatedModelName);
      });
    };

    // Load settings if available
    if (settingRegistry) {
      Promise.all([settingRegistry.load(plugin.id), app.restored])
        .then(([settings]) => {
          loadSettings(settings);
        })
        .catch(error => {
          console.error('Failed to load sage-ai settings', error);
        });
    }

    // Add an application command to open the chat widget
    const command: string = 'sage-ai:open-chat';
    app.commands.addCommand(command, {
      label: 'Open AI Chat',
      execute: () => {
        // If the widget is disposed, create a new one
        if (chatWidget.isDisposed) {
          chatWidget = createChatWidget();
        }

        // If the widget is not attached to the DOM, add it
        if (!chatWidget.isAttached) {
          app.shell.add(chatWidget, 'right', { rank: 1000 });
        }

        // Activate the widget
        app.shell.activateById(chatWidget.id);
      }
    });

    // Add the command to the command palette
    palette.addItem({ command, category: 'AI Tools' });
  }
};
