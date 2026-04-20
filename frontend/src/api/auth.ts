import client from './client'
import type { User, Token } from '../types/types'

export const login = async (email: string, password: string): Promise<Token> => {
  const formData = new URLSearchParams()
  formData.append('username', email)
  formData.append('password', password)

  const response = await client.post('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export const register = async (
  email: string,
  password: string,
  full_name: string
): Promise<User> => {
  const response = await client.post('/auth/register', {
    email,
    password,
    full_name,
  })
  return response.data
}

export const getMe = async (): Promise<User> => {
  const response = await client.get('/auth/me')
  return response.data
}

export { useAuth } from '../context/AuthContext'