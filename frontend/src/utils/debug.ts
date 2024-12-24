import { currentConfig } from '../config'

export const debug = {
  log: (...args: any[]) => {
    if (currentConfig.debug) {
      console.log(...args)
    }
  },
  
  warn: (...args: any[]) => {
    if (currentConfig.debug) {
      console.warn(...args)
    }
  },
  
  error: (...args: any[]) => {
    if (currentConfig.debug) {
      console.error(...args)
    }
  }
} 
