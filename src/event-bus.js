// src/event-bus.js
import mitt from 'mitt';

const emitter = mitt();

let currentOptions = [];
let selectedButton = null;

export const EventBusOne = {
  on: emitter.on,
  off: emitter.off,
  emit: emitter.emit,
  getOptions: () => currentOptions,
  setOptions: (options) => {
    currentOptions = options;
    emitter.emit('options-sent', options);
  }
};


