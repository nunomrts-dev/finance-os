import client from './client'
import type { NetWorth } from '../types/types'

export const getCurrentNetWorth = async (): Promise<NetWorth> => {
  const response = await client.get('/networth/current')
  return response.data
}

export const getNetWorthHistory = async (limit?: number) => {
  const response = await client.get('/networth/history', { params: { limit } })
  return response.data
}

export const getNetWorthBreakdown = async () => {
  const response = await client.get('/networth/breakdown')
  return response.data
}