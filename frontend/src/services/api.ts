import axios from 'axios'
import { currentConfig } from '../config'
import { debug } from '../utils/debug'
import router from '../router'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)

// 设置默认时区
const TIMEZONE = 'Asia/Shanghai'

export const api = axios.create({
  baseURL: currentConfig.api.baseURL
})

// 时区转换工具函数
const convertToUTC = (timestamp: number) => {
  // 将本地时间戳转换为UTC时间戳
  const localDate = dayjs(timestamp)

  debug.log('Converting to UTC:', {
    input: {
      timestamp,
      local: {
        date: localDate.format('YYYY-MM-DD HH:mm:ss'),
        timezone: TIMEZONE
      }
    },
    output: {
      timestamp: localDate.valueOf(),
      utc: localDate.utc().format('YYYY-MM-DD HH:mm:ss')
    }
  })

  return localDate.valueOf()
}

// 响应数据时区转换
const convertDatesToLocal = (data: any) => {
  if (!data) return data

  if (Array.isArray(data)) {
    return data.map(item => {
      if (item.created_at) {
        // 将UTC时间戳转换为本地时区时间
        const utcTime = dayjs.utc(item.created_at)
        const localTime = utcTime.tz(TIMEZONE)

        debug.log('Converting array date to local:', {
          input: {
            raw: item.created_at,
            parsed: utcTime.format('YYYY-MM-DD HH:mm:ss'),
            timezone: 'UTC'
          },
          output: {
            formatted: localTime.format('YYYY-MM-DD HH:mm:ss'),
            timezone: TIMEZONE
          }
        })

        return {
          ...item,
          created_at: localTime.format('YYYY-MM-DD HH:mm:ss')
        }
      }
      return item
    })
  }

  if (typeof data === 'object' && data.created_at) {
    // 将UTC时间戳转换为本地时区时间
    const utcTime = dayjs.utc(data.created_at)
    const localTime = utcTime.tz(TIMEZONE)

    debug.log('Converting object date to local:', {
      input: {
        raw: data.created_at,
        parsed: utcTime.format('YYYY-MM-DD HH:mm:ss'),
        timezone: 'UTC'
      },
      output: {
        formatted: localTime.format('YYYY-MM-DD HH:mm:ss'),
        timezone: TIMEZONE
      }
    })

    return {
      ...data,
      created_at: localTime.format('YYYY-MM-DD HH:mm:ss')
    }
  }

  return data
}

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    debug.log('Request:', config)
    return config
  },
  error => {
    debug.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    debug.log('Response:', response)
    debug.log('Response data structure:', {
      hasData: !!response.data,
      dataType: typeof response.data,
      data: response.data
    })

    // 转换响应数据中的时间为本地时区
    const convertedData = convertDatesToLocal(response.data)
    return convertedData
  },
  error => {
    debug.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      config: error.config,
      stack: error.stack
    })

    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('isAuthenticated')
      window.location.href = '/login'
    } else if (error.response?.status === 500) {
      localStorage.removeItem('token')
      localStorage.removeItem('isAuthenticated')
      window.location.href = '/login'
    }

    if (error.response?.data?.detail) {
      return Promise.reject(new Error(error.response.data.detail))
    }

    return Promise.reject(error)
  }
)

interface DateRangeParams {
  start?: number;
  end?: number;
}

export const getRecentKeys = (dateRange: { start: number; end: number } | null = null) => {
  let params: DateRangeParams = {}

  if (dateRange) {
    const now = dayjs().tz(TIMEZONE)
    const start = dayjs(dateRange.start).tz(TIMEZONE)
    const end = dayjs(dateRange.end).tz(TIMEZONE)

    // 如果是"今天"的查询，使用过去24小时
    if (start.isSame(now, 'day') && end.isSame(now, 'day')) {
      const endTime = now
      const startTime = endTime.subtract(24, 'hour')

      params = {
        start: startTime.utc().valueOf(),
        end: endTime.utc().valueOf()
      }

      debug.log('Using 24-hour range:', {
        local: {
          start: startTime.format('YYYY-MM-DD HH:mm:ss'),
          end: endTime.format('YYYY-MM-DD HH:mm:ss'),
          timezone: TIMEZONE
        },
        utc: {
          start: startTime.utc().format('YYYY-MM-DD HH:mm:ss'),
          end: endTime.utc().format('YYYY-MM-DD HH:mm:ss')
        },
        timestamps: {
          start: params.start,
          end: params.end
        }
      })
    } else {
      // 自定义日期范围，使用UTC时间戳
      params = {
        start: start.utc().valueOf(),
        end: end.utc().valueOf()
      }

      debug.log('Using custom date range:', {
        local: {
          start: start.format('YYYY-MM-DD HH:mm:ss'),
          end: end.format('YYYY-MM-DD HH:mm:ss'),
          timezone: TIMEZONE
        },
        utc: {
          start: start.utc().format('YYYY-MM-DD HH:mm:ss'),
          end: end.utc().format('YYYY-MM-DD HH:mm:ss')
        },
        timestamps: {
          start: params.start,
          end: params.end
        }
      })
    }
  }

  return api.get('/keys/recent', { params })
}

export const getHighScoreKeys = (dateRange: { start: number; end: number } | null = null) => {
  let params: DateRangeParams = {}

  if (dateRange) {
    const start = dayjs(dateRange.start).tz(TIMEZONE)
    const end = dayjs(dateRange.end).tz(TIMEZONE)

    params = {
      start: start.utc().valueOf(),
      end: end.utc().valueOf()
    }

    debug.log('High score keys date range:', {
      local: {
        start: start.format('YYYY-MM-DD HH:mm:ss'),
        end: end.format('YYYY-MM-DD HH:mm:ss'),
        timezone: TIMEZONE
      },
      utc: {
        start: start.utc().format('YYYY-MM-DD HH:mm:ss'),
        end: end.utc().format('YYYY-MM-DD HH:mm:ss')
      },
      timestamps: params
    })
  }

  return api.get('/keys/high-score', { params })
}

export const getStatistics = (dateRange: { start: number; end: number } | null = null) => {
  let params: DateRangeParams = {}

  if (dateRange) {
    const start = dayjs(dateRange.start).tz(TIMEZONE)
    const end = dayjs(dateRange.end).tz(TIMEZONE)

    params = {
      start: start.utc().valueOf(),
      end: end.utc().valueOf()
    }

    debug.log('Statistics date range:', {
      local: {
        start: start.format('YYYY-MM-DD HH:mm:ss'),
        end: end.format('YYYY-MM-DD HH:mm:ss'),
        timezone: TIMEZONE
      },
      utc: {
        start: start.utc().format('YYYY-MM-DD HH:mm:ss'),
        end: end.utc().format('YYYY-MM-DD HH:mm:ss')
      },
      timestamps: params
    })
  }

  return api.get('/statistics', { params })
}

interface MaskOrdersRequest {
  type: 'orderId' | 'productId'
  ids: string[]
}

interface ModifyOrderRequest {
  type: 'orderId' | 'productId'
  id: string
  changes: {
    amount?: number
    customerName?: string
    customerId?: string
    idType?: string
  }
}

interface OperationResult {
  success: boolean
  message: string
  affectedRows: number
  details?: Record<string, any>
}

export async function maskOrders(params: MaskOrdersRequest): Promise<OperationResult> {
  const response = await fetch('/api/orders/mask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}

export async function modifyOrder(params: ModifyOrderRequest): Promise<OperationResult> {
  const response = await fetch('/api/orders/modify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
} 
