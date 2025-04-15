import {JupyterFrontEnd} from '@jupyterlab/application';

import { Widget } from '@lumino/widgets';
import { Message } from '@lumino/messaging';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

import {VoittaToolRouter} from "./voitta/voittaServer";
import { initPythonBridge, callPython, registerFunction, get_ws } from './voitta/pythonBridge_browser'

import { get_tools } from "./integrations/jupyter_integrations"

import { createEscobarSplitButton } from "./js/ui_elements"
import { SettingsPage } from "./js/setting_page"

/**
 * Interface for chat settings
 */
interface IChatSettings {
  defaultGreeting: string;
  maxMessages: number;
  serverUrl: string;
  apiKey: string;
}

/**
 * Default settings
 */
const DEFAULT_SETTINGS: IChatSettings = {
  defaultGreeting: 'Hello! How can I assist you today?',
  maxMessages: 100,
  serverUrl: 'ws://192.168.128.2:8777/ws',
  apiKey: 'The Future Of Computing'
};

/**
 * A class representing a chat message
 */
export class ResponseMessage {
  public readonly id: string;
  public readonly role: 'user' | 'assistant';
  private messageElement: HTMLDivElement;
  private contentElement: HTMLDivElement;
  private content: string;

  /**
   * Create a new ResponseMessage
   * @param id Unique identifier for the message
   * @param role The role of the message sender ('user' or 'assistant')
   * @param initialContent Optional initial content for the message
   */
  constructor(id: string, role: 'user' | 'assistant', initialContent: string = '') {
    this.id = id;
    this.role = role;
    this.content = initialContent;
    
    // Create message element
    this.messageElement = document.createElement('div');
    this.messageElement.className = `escobar-message escobar-message-${role}`;
    this.messageElement.dataset.messageId = id;
    
    // Create content element
    this.contentElement = document.createElement('div');
    this.contentElement.className = 'escobar-message-content';
    this.contentElement.textContent = initialContent;
    
    this.messageElement.appendChild(this.contentElement);
  }
  
  /**
   * Set the content of the message
   * @param content The new content
   */
  public setContent(content: string): void {
    this.content = content;
    this.contentElement.textContent = content;
  }
  
  /**
   * Get the content of the message
   */
  public getContent(): string {
    return this.content;
  }
  
  /**
   * Get the DOM element for the message
   */
  public getElement(): HTMLDivElement {
    return this.messageElement;
  }
}

/**
 * A simple chat widget for Jupyter.
 */
export class ChatWidget extends Widget {
  private chatContainer: HTMLDivElement;
  private buttonContainer: HTMLDivElement;
  private divider: HTMLDivElement;
  private inputContainer: HTMLDivElement;
  private chatInput: HTMLTextAreaElement;
  private sendButton: HTMLButtonElement;
  private messages: ResponseMessage[] = [];
  private messageMap: Map<string, ResponseMessage> = new Map();
  private settings: IChatSettings = DEFAULT_SETTINGS;

  private voittaToolRouter:VoittaToolRouter | undefined;
  private apiKey: string;

  // WebSocket connection
  private ws: WebSocket | null = null;
  
  // Counter for generating unique IDs
  private static idCounter = 0;
  private static messageCounter = 0;
  private app: JupyterFrontEnd;
  private settingsRegistry: ISettingRegistry | null;

  constructor(app: JupyterFrontEnd, settingsRegistry: ISettingRegistry | null) {
    // Generate a unique ID for this widget instance
    const id = `escobar-chat-${ChatWidget.idCounter++}`;
    super();

    this.app = app;
    this.settingsRegistry = settingsRegistry;
    this.id = id;
    this.addClass('escobar-chat');
    this.title.label = 'Chat';
    this.title.caption = 'Escobar Chat';
    this.title.iconClass = 'jp-MessageIcon'; // Add an icon for the sidebar
    this.title.closable = true;

    // Initialize apiKey from settings or default
    this.apiKey = this.settings.apiKey;

    // Create the main layout
    this.node.style.display = 'flex';
    this.node.style.flexDirection = 'column';
    this.node.style.height = '100%';
    this.node.style.padding = '5px';
    
    // Load settings if provided
    if (settingsRegistry) {
      this.loadSettings(settingsRegistry);
    }

    // Create button container for top buttons
    this.buttonContainer = document.createElement('div');
    this.buttonContainer.className = 'escobar-button-container';
    
    // Style the container to be in the top right and fit its content
    this.buttonContainer.style.display = 'flex';
    this.buttonContainer.style.alignItems = 'center';
    this.buttonContainer.style.justifyContent = 'flex-end'; // Align buttons to the right
    this.buttonContainer.style.padding = '5px';
    this.buttonContainer.style.backgroundColor = 'rgba(128, 128, 128, 0.5)'; // Semi-transparent grey background
    this.buttonContainer.style.borderRadius = '4px'; // Rounded corners
    
    this.node.appendChild(this.buttonContainer);

    // Create buttons
    this.createTopButtons();

    // Create chat container
    this.chatContainer = document.createElement('div');
    this.chatContainer.className = 'escobar-chat-container';
    // Set initial height to 80% of the container
    this.chatContainer.style.height = '80%';
    this.chatContainer.style.flex = 'none';
    this.node.appendChild(this.chatContainer);

    // Create divider
    this.divider = document.createElement('div');
    this.divider.className = 'escobar-divider';
    this.node.appendChild(this.divider);

    // Add drag functionality to divider
    this.setupDividerDrag();

    // Create input container
    this.inputContainer = document.createElement('div');
    this.inputContainer.className = 'escobar-input-container';
    this.node.appendChild(this.inputContainer);

    // Create chat input
    this.chatInput = document.createElement('textarea');
    this.chatInput.className = 'escobar-chat-input';
    this.chatInput.placeholder = 'Type your message here...';
    this.chatInput.rows = 2;
    this.chatInput.addEventListener('keydown', (event: KeyboardEvent) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        this.sendMessage(this.sendButton.textContent);
      }
    });
    this.inputContainer.appendChild(this.chatInput);

    const splitButton:HTMLDivElement = createEscobarSplitButton(["Talk","Plan","Act"]);
    this.sendButton = splitButton["mainButton"];
    this.inputContainer.appendChild(splitButton);

    this.sendButton.addEventListener('click', () => {
      this.sendMessage(this.sendButton.textContent);
    });

    setTimeout(async () => {
      await this.init();
    }, 1000);
    
    
    // Connect to WebSocket server
    //this.connectWebSocket();
  }

  /**
   * Create the top buttons for the chat interface
   */
  private createTopButtons(): void {
    // Style for all buttons to make them more bold without backgrounds
    const buttonStyle = `
      font-weight: bold;
      margin: 0 5px;
      padding: 5px;
      background: transparent;
      border: none;
    `;
    
    // Add a style for the SVG icons to make them brighter but keep them sharp
    const iconStyle = document.createElement('style');
    iconStyle.textContent = `
      .escobar-icon-svg {
        stroke-width: 3;
        stroke: #ffffff;
      }
    `;
    document.head.appendChild(iconStyle);
    
    // Create new chat button with inline SVG
    const newChatButton = this.createIconButton(
      'escobar-new-chat-button',
      buttonStyle,
      `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="16"></line>
        <line x1="8" y1="12" x2="16" y2="12"></line>
      </svg>`,
      'New Chat'
    );
    newChatButton.addEventListener('click',async () => {
      await this.createNewChat();
      console.log('New chat button clicked');
    });
    this.buttonContainer.appendChild(newChatButton);

    // Create reconnect button with inline SVG
    const reconnectButton = this.createIconButton(
      'escobar-reconnect-button',
      buttonStyle,
      `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
        <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"></path>
      </svg>`,
      'Reconnect'
    );
    reconnectButton.addEventListener('click', async () => {
      console.log('Reconnect button clicked');
      
      // Close existing connection if any
      const ws = get_ws();
      if (ws) {
        ws.close();
      }
      
      try {
        // Call the init function to fully reinitialize the connection
        await this.init();
        console.log("Reconnected and initialized successfully");
        
        // Blink the reconnect icon 3 times to indicate success
        const iconContainer = reconnectButton.querySelector('.escobar-icon-container') as HTMLElement;
        if (iconContainer) {
          // Store original opacity
          const originalOpacity = iconContainer.style.opacity || '1';
          
          // Blink 3 times (fade out and in)
          for (let i = 0; i < 3; i++) {
            // Fade out
            iconContainer.style.opacity = '0.2';
            await new Promise(resolve => setTimeout(resolve, 150));
            
            // Fade in
            iconContainer.style.opacity = '1';
            await new Promise(resolve => setTimeout(resolve, 150));
          }
        }
      } catch (e) {
        console.error('Error reconnecting to server:', e);
        this.addMessage('assistant', 'Error reconnecting to server. Please check your settings and try again.');
      }
    });
    this.buttonContainer.appendChild(reconnectButton);

    // Create stop button with inline SVG
    const stopButton = this.createIconButton(
      'escobar-stop-button',
      buttonStyle,
      `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
        <rect x="6" y="6" width="12" height="12" rx="2" ry="2"></rect>
      </svg>`,
      'Stop'
    );
    stopButton.addEventListener('click', () => {
      console.log('Stop button clicked');
      
      // Find the last assistant message that's still generating
      const lastMessage = this.messages[this.messages.length - 1];
      if (lastMessage && lastMessage.role === 'assistant' && lastMessage.getContent().includes('Waiting for response')) {
        // Update the message to indicate it was stopped
        lastMessage.setContent('Message generation stopped by user.');
      }
      
      // TODO: In a future implementation, we could send a stop signal to the server
      // For now, we just update the UI to indicate the message was stopped
    });
    this.buttonContainer.appendChild(stopButton);
    
    // Create settings button with inline SVG
    const settingsButton = this.createIconButton(
      'escobar-settings-button',
      buttonStyle,
      `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="escobar-icon-svg">
        <circle cx="12" cy="12" r="3"></circle>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
      </svg>`,
      'Settings'
    );
    settingsButton.addEventListener('click', () => {
      // Create and show settings page
      if (this.settingsRegistry) {
        const settingsPage = new SettingsPage(
          this.settingsRegistry, 
          this.settings,
          (newSettings) => {
            // Update settings when saved
            this.updateSettings(newSettings);
            console.log('Settings updated:', newSettings);
          }
        );
        settingsPage.show();
      } else {
        console.error('Settings registry not available');
      }
    });
    this.buttonContainer.appendChild(settingsButton);
  }

  /**
   * Create an icon button with tooltip
   * @param className CSS class for the button
   * @param svgContent Inline SVG content
   * @param tooltip Tooltip text for mouseover
   * @returns The created button element
   */
  private createIconButton(className: string, style: string, svgContent: string, tooltip: string): HTMLButtonElement {
    const button = document.createElement('button');
    button.className = `escobar-icon-button ${className}`;
    button.title = tooltip; // This adds the native tooltip on hover
    button.style.cssText = style; // Apply the custom style
    
    // Create a span to hold the SVG content
    const iconSpan = document.createElement('span');
    iconSpan.className = 'escobar-icon-container';
    iconSpan.innerHTML = svgContent;
    
    button.appendChild(iconSpan);
    return button;
  }

  private handlePythonResponse(response: any, responseMsg?: ResponseMessage): void {
    try {
      let responseText: string;
      
      console.log("handlePythonResponse:", response)

      var value = response.value;


      if (typeof value === 'string') {
        responseText = value;
      } else if (value && typeof value === 'object') {
        responseText = JSON.stringify(value);
      } else {
        responseText = 'Received empty response from server';
      }
      
      // Create a new response message and set its content
      responseMsg.setContent(responseText)
    } catch (error) {
      console.error('Error handling Python response:', error);
      const responseMsg = this.addMessage("assistant", 'Error: Failed to process server response');
    }
  }

  async say(args:any) {

  }

  async init() {
    await this.clearChatArea();
    this.voittaToolRouter = new VoittaToolRouter();
    const tools = await get_tools(this.app);
    
    registerFunction('handleResponse', false, this.handlePythonResponse.bind(this));
    registerFunction('say', false, this.say.bind(this));
    this.voittaToolRouter.tools = tools;

    try {
      // Use serverUrl from settings
      await initPythonBridge(this.settings.serverUrl);
      console.log("WEBSOCKET CONNECTED!!!");
    } catch (e) {
      console.error(e);
    }

    const old_messages = await this.loadMessages();

    // this is a very stupid approach....
    let start_call_id = this.generateMessageId();
    const payload = JSON.stringify({
      method: "start",
      api_key: this.apiKey,
      call_id: start_call_id,
      intraspection: this.voittaToolRouter.intraspect(),
      rootPath: "rootPath"
    });

    let response = await callPython(payload);
    console.log(`------ python start: ${response}`)
  }

  /**
   * Generate a unique message ID
   */
  private generateMessageId(): string {
    const timestamp = Date.now();
    const counter = ChatWidget.messageCounter++;
    return `msg-${timestamp}-${counter}`;
  }

  /**
   * Find a message by ID
   * @param id The message ID to find
   */
  private findMessageById(id: string): ResponseMessage | undefined {
    return this.messageMap.get(id);
  }

  /**
   * Load settings from the settings registry
   */
  private loadSettings(settingsRegistry: ISettingRegistry): void {
    settingsRegistry
      .load('escobar:plugin')
      .then(settings => {
        this.updateSettings(settings.composite as any as IChatSettings);
        
        // Add a greeting message
        if (this.settings.defaultGreeting) {
          this.addMessage('assistant', this.settings.defaultGreeting);
        }
        
        // Listen for setting changes
        settings.changed.connect(() => {
          this.updateSettings(settings.composite as any as IChatSettings);
        });
      })
      .catch(reason => {
        console.error('Failed to load settings for escobar.', reason);
      });
  }
  
  /**
   * Update settings
   */
  private updateSettings(settings: IChatSettings): void {
    this.settings = { ...DEFAULT_SETTINGS, ...settings };
    
    // Update apiKey when settings change
    this.apiKey = this.settings.apiKey;
  }

  private async createNewChat(): Promise<void> {
   //await this.clearChatArea();

    const call_id = this.generateMessageId();
    const payload = JSON.stringify({
      method: "createNewChat",
      message: {machineId: "jupyter lab","sessionId":"jupyter lab"},
      api_key: this.apiKey,
      call_id: call_id
    });
    const response = await callPython(payload);

    this.init();

    //await this.loadMessages();
  }

  private async loadMessages(): Promise<void> {
    const call_id = this.generateMessageId()
    const payload = JSON.stringify({
      method: "loadMessages",
      message: {machineId: "jupyter lab","sessionId":"jupyter lab"},
      api_key: this.apiKey,
      call_id: call_id
    });
    const response = await callPython(payload);
    console.log("------ loadMessages -----");
    console.log(response.value);
    for (var i = 0; i < response.value.length; i++) {
      const message = response.value[i];
      switch (message.role) {
        case "user": 
          this.addMessage('user', message.content);
          break;
        case "assistant":
          if ((message.content != undefined) && (message.content != "")) {
            this.addMessage('assistant', message.content);
          }
          break;
        default:
          console.log(`unknwon message type: ${message.role}`);
      }
    }
  }



  /**
   * Send a message from the input field.
   */
  private async sendMessage(mode:string): Promise<void> {
    const content = this.chatInput.value.trim();

    console.log("sendMessage:", content, "as:", mode);

    if (!content) {
      return;
    }

    // Generate a unique ID for this message
    const messageId = this.generateMessageId();
    const call_id = this.generateMessageId()
    
    // Add user message
    const userMessage = this.addMessage('user', content, messageId);
    
    // Clear input
    this.chatInput.value = '';
    
    // Create a placeholder response message with the same ID
    const responseMessage = this.addMessage('assistant', 'Waiting for response...', messageId);
    
    const ws = get_ws();

    // Send message to WebSocket server if connected
    if (ws && ws.readyState === WebSocket.OPEN) {
      console.log("sending user data....");
      try {
        const payload = JSON.stringify({
          method: "userMessage",
          message: content,
          mode: mode,
          api_key: this.apiKey,
          call_id: call_id
        });
        const response = await callPython(payload);
        console.log(`Sent message with ID: ${messageId}`);
        this.handlePythonResponse(response, responseMessage);

      } catch (error) {
        console.error('Error sending message to WebSocket server:', error);
        responseMessage.setContent('Error sending message to server');
      }
    } else {
      // Fallback to echo response if not connected
      setTimeout(() => {
        responseMessage.setContent(`Echo: ${content} (WebSocket not connected)`);
      }, 500);
    }
    
    // Limit the number of messages if needed
    this.limitMessages();
  }

  /**
   * Add a message to the chat.
   * @param role The role of the message sender ('user' or 'assistant')
   * @param content The message content
   * @param id Optional message ID (generated if not provided)
   * @returns The created ResponseMessage
   */
  private addMessage(role: 'user' | 'assistant', content: string, id?: string): ResponseMessage {
    // Generate ID if not provided
    const messageId = id || this.generateMessageId();
    
    // Create a new ResponseMessage
    const message = new ResponseMessage(messageId, role, content);
    
    // Add to messages array
    this.messages.push(message);
    
    // Add to message map
    this.messageMap.set(messageId, message);
    
    // Add to DOM
    this.chatContainer.appendChild(message.getElement());
    
    // Scroll to bottom
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    
    return message;
  }
  
  /**
   * Limit the number of messages based on settings
   */
  
  private limitMessages(): void {
    if (this.messages.length > this.settings.maxMessages) {
      // Remove excess messages
      const excessCount = this.messages.length - this.settings.maxMessages;
      const removedMessages = this.messages.splice(0, excessCount);
      
      // Remove from DOM and message map
      for (const message of removedMessages) {
        this.chatContainer.removeChild(message.getElement());
        this.messageMap.delete(message.id);
      }
    }
  }

  private async clearChatArea(): Promise<void> {
    // Create a copy of the messages array to safely iterate through
    const messagesToRemove = [...this.messages];
    
    // Clear the original arrays first
    this.messages = [];
    
    // Now safely remove each message from the DOM and the map
    for (const message of messagesToRemove) {
      try {
        if (this.chatContainer.contains(message.getElement())) {
          this.chatContainer.removeChild(message.getElement());
        }
        this.messageMap.delete(message.id);
      } catch (error) {
        console.error('Error removing message:', error);
      }
    }
    
    // Clear the message map as a final safety measure
    this.messageMap.clear();
  }
  
  /**
   * Handle activation requests for the widget
   */
  protected onActivateRequest(msg: Message): void {
    super.onActivateRequest(msg);
    this.chatInput.focus();
  }

  /**
   * Setup drag functionality for the divider
   */
  private setupDividerDrag(): void {
    let isDragging = false;
    let startY = 0;
    let startHeight = 0;

    const isScrolledToBottom = () => {
      // Get the scroll position
      const scrollTop = this.chatContainer.scrollTop;
      // Get the visible height
      const clientHeight = this.chatContainer.clientHeight;
      // Get the total scrollable height
      const scrollHeight = this.chatContainer.scrollHeight;
      
      // If scrollTop + clientHeight is approximately equal to scrollHeight,
      // then the container is scrolled to the bottom
      // (using a small threshold to account for rounding errors)

      return Math.abs(scrollTop + clientHeight -scrollHeight) < 100;
    };



    // Mouse move event handler
    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      
      // Calculate exact delta from start position

      const delta = e.pageY - startY - 18;

      //console.log("event:", delta, e.offsetY, e.pageY, e.screenY, e.clientY);

      // Get container height to calculate minimum and maximum allowed height
      const containerHeight = this.node.offsetHeight;
      const minChatHeight = Math.max(100, containerHeight * 0.3); // At least 30% of container or 100px
      const maxChatHeight = containerHeight * 0.85; // At most 85% of container
      
      // Apply delta directly to the starting height with min/max constraints
      const newHeight = Math.min(maxChatHeight, Math.max(minChatHeight, startHeight + delta));
      
      // Update chat container height
      this.chatContainer.style.height = `${newHeight}px`;
      this.chatContainer.style.flex = 'none';

      if (isScrolledToBottom()) {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
      }

    };
    
    // Mouse up event handler
    const onMouseUp = () => {
      if (!isDragging) return;
      
      isDragging = false;
      
      // Remove temporary event listeners
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      
      // Restore text selection
      document.body.style.userSelect = '';
    };
    
    // Attach mousedown event to divider
    this.divider.addEventListener('mousedown', (e: MouseEvent) => {
      // Prevent default to avoid text selection
      e.preventDefault();
      e.stopPropagation();
      
      // Store initial values
      isDragging = true;
      startY = e.pageY;
      startHeight = this.chatContainer.offsetHeight;
      
      // Add temporary event listeners
      window.addEventListener('mousemove', onMouseMove);
      window.addEventListener('mouseup', onMouseUp);
      
      // Prevent text selection during drag
      document.body.style.userSelect = 'none';
    });
  }

  /**
   * Dispose of the widget and clean up resources
   */
  dispose(): void {
    // Close WebSocket connection when widget is disposed
    const ws = get_ws();
    if (ws) {
      ws.close();
    }
    super.dispose();
  }
}
