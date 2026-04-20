import client from './client'

export const getDashboardSummary = async () => {
  const response = await client.get('/analytics/dashboard')
  return response.data
}

export const getSpendingByCategory = async (start_date?: string, end_date?: string) => {
  const response = await client.get('/analytics/spending', {
    params: { start_date, end_date }
  })
  return response.data
}

export const getIncomeBySource = async (start_date?: string, end_date?: string) => {
  const response = await client.get('/analytics/income', {
    params: { start_date, end_date }
  })
  return response.data
}

export const getMonthlySummary = async (year?: number, month?: number) => {
  const response = await client.get('/analytics/monthly', {
    params: { year, month }
  })
  return response.data
}

export const getCashflow = async () => {
  const response = await client.get('/analytics/cashflow')
  return response.data
}