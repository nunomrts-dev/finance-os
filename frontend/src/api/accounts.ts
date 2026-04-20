import client from './client'
import type { Account } from '../types/types'

export const getAccounts = async (): Promise<Account[]> => {
  const response = await client.get('/accounts')
  return response.data
}

export const getAccountsSummary = async () => {
  const response = await client.get('/accounts/summary')
  return response.data
}

export const createAccount = async (data: {
  name: string
  type: string
  currency: string
  current_balance: number
}): Promise<Account> => {
  const response = await client.post('/accounts', data)
  return response.data
}

export const updateAccount = async (id: number, data: Partial<Account>): Promise<Account> => {
  const response = await client.put(`/accounts/${id}`, data)
  return response.data
}