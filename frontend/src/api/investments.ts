import client from './client'
import type { Investment } from '../types/types'

export const getInvestments = async (): Promise<Investment[]> => {
  const response = await client.get('/investments')
  return response.data
}

export const createInvestment = async (data: {
  amount_invested_eur: number
  cspx_price_at_purchase: number
  units_purchased: number
  fees: number
  funding_source: string
  notes?: string
  date: string
}): Promise<Investment> => {
  const response = await client.post('/investments', data)
  return response.data
}

export const getPortfolioPerformance = async () => {
  const response = await client.get('/investments/performance')
  return response.data
}

export const getPerformanceBySource = async () => {
  const response = await client.get('/investments/performance/by-source')
  return response.data
}

export const getCurrentPrice = async () => {
  const response = await client.get('/investments/price/current')
  return response.data
}