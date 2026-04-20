import client from './client'
import type { Category } from '../types/types'

export const getCategories = async (): Promise<Category[]> => {
  const response = await client.get('/categories')
  return response.data
}