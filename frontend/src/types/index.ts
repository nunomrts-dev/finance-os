export interface User {
  id: number
  email: string
  full_name: string | null
  role: string
  is_active: boolean
  created_at: string
}

export interface Account {
  id: number
  user_id: number
  name: string
  type: string
  currency: string
  current_balance: number
  is_active: boolean
  created_at: string
}

export interface Category {
  id: number
  user_id: number | null
  name: string
  type: string
  color: string
  icon: string | null
  is_default: boolean
  created_at: string
}

export interface Transaction {
  id: number
  user_id: number
  account_id: number
  category_id: number | null
  type: string
  amount: number
  currency: string
  description: string | null
  notes: string | null
  date: string
  is_recurring: boolean
  recurring_frequency: string | null
  created_at: string
  updated_at: string | null
}

export interface Budget {
  id: number
  user_id: number
  category_id: number
  amount_limit: number
  period: string
  start_date: string
  end_date: string | null
  alert_at_percent: number
  created_at: string
}

export interface Investment {
  id: number
  user_id: number
  amount_invested_eur: number
  cspx_price_at_purchase: number
  units_purchased: number
  fees: number
  funding_source: string
  notes: string | null
  date: string
  created_at: string
}

export interface NetWorth {
  bank_balance: number
  investment_value: number
  total_net_worth: number
  current_cspx_price: number
}

export interface Token {
  access_token: string
  token_type: string
}