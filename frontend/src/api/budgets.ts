import client from './client'
import type { Budget } from '../types/types'

export const getBudgets = async (): Promise<Budget[]> => {
  const response = await client.get('/budgets')
  return response.data
}

export const getBudgetsStatus = async () => {
  const response = await client.get('/budgets/status')
  return response.data
}

export const createBudget = async (data: {
  category_id: number
  amount_limit: number
  period: string
  start_date: string
  end_date?: string
  alert_at_percent?: number
}): Promise<Budget> => {
  const response = await client.post('/budgets', data)
  return response.data
}