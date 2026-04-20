import client from './client'
import type { Transaction } from '../types/types'

export const getTransactions = async (params?: {
  type?: string
  category_id?: number
  account_id?: number
  start_date?: string
  end_date?: string
}): Promise<Transaction[]> => {
  const response = await client.get('/transactions', { params })
  return response.data
}

export const createTransaction = async (data: {
  account_id: number
  category_id?: number
  type: string
  amount: number
  currency?: string
  description?: string
  notes?: string
  date: string
  is_recurring?: boolean
  recurring_frequency?: string
}): Promise<Transaction> => {
  const response = await client.post('/transactions', data)
  return response.data
}

export const deleteTransaction = async (id: number): Promise<void> => {
  await client.delete(`/transactions/${id}`)
}