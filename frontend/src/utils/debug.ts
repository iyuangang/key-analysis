import { config } from '../config'

export const debug = {
  log: (...args: any[]) => {
    if (config.debug) {
      console.log(...args)
    }
  },
  
  error: (...args: any[]) => {
    console.error(...args)
  },
  
  warn: (...args: any[]) => {
    if (config.debug) {
      console.warn(...args)
    }
  },
  
  trace: (message: string) => {
    if (config.debug) {
      console.trace(message)
    }
  }
} 
