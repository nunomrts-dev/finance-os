import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { createBudget, getBudgetsStatus } from '../api/budgets'
import { getCategories } from '../api/categories'

interface BudgetStatus {
  budget_id: number
  category_id: number
  amount_limit: number
  amount_spent: number
  amount_remaining: number
  percent_used: number
  alert_at_percent: number
  is_over_budget: boolean
  is_near_limit: boolean
}

export default function Budgets() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    category_id: '',
    amount_limit: '',
    period: 'monthly',
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    alert_at_percent: '80',
  })

  const { data: budgetStatus } = useQuery({
    queryKey: ['budget-status'],
    queryFn: getBudgetsStatus,
  })

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  })

  const mutation = useMutation({
    mutationFn: createBudget,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['budget-status'] })
      setShowForm(false)
      setForm({
        category_id: '',
        amount_limit: '',
        period: 'monthly',
        start_date: new Date().toISOString().split('T')[0],
        end_date: '',
        alert_at_percent: '80',
      })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({
      category_id: parseInt(form.category_id),
      amount_limit: parseFloat(form.amount_limit),
      period: form.period,
      start_date: new Date(form.start_date).toISOString(),
      end_date: form.end_date ? new Date(form.end_date).toISOString() : undefined,
      alert_at_percent: parseFloat(form.alert_at_percent),
    })
  }

  const expenseCategories = categories?.filter(c => c.type === 'EXPENSE')

  const getCategoryName = (category_id: number) => {
    return categories?.find(c => c.id === category_id)?.name ?? 'Unknown'
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Budgets</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          {showForm ? 'Cancel' : '+ Add Budget'}
        </button>
      </div>

      {showForm && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">New Budget</h3>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Category</label>
              <select
                value={form.category_id}
                onChange={(e) => setForm({ ...form, category_id: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              >
                <option value="">Select category</option>
                {expenseCategories?.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Amount Limit (€)</label>
              <input
                type="number"
                step="0.01"
                value={form.amount_limit}
                onChange={(e) => setForm({ ...form, amount_limit: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Period</label>
              <select
                value={form.period}
                onChange={(e) => setForm({ ...form, period: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              >
                <option value="monthly">Monthly</option>
                <option value="weekly">Weekly</option>
                <option value="yearly">Yearly</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Alert At (%)</label>
              <input
                type="number"
                value={form.alert_at_percent}
                onChange={(e) => setForm({ ...form, alert_at_percent: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Start Date</label>
              <input
                type="date"
                value={form.start_date}
                onChange={(e) => setForm({ ...form, start_date: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">End Date (optional)</label>
              <input
                type="date"
                value={form.end_date}
                onChange={(e) => setForm({ ...form, end_date: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              />
            </div>
            <div className="md:col-span-2">
              <button
                type="submit"
                disabled={mutation.isPending}
                className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                {mutation.isPending ? 'Saving...' : 'Save Budget'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="space-y-4">
        {budgetStatus?.map((budget: BudgetStatus) => {
          const percent = budget.percent_used
          const isOver = budget.is_over_budget
          const isNear = budget.is_near_limit

          return (
            <div key={budget.budget_id} className="bg-gray-900 rounded-xl p-5 border border-gray-800">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-white font-semibold">{getCategoryName(budget.category_id)}</h3>
                <span className={`text-sm font-medium ${isOver ? 'text-red-400' : isNear ? 'text-amber-400' : 'text-green-400'}`}>
                  {isOver ? 'Over budget' : isNear ? 'Near limit' : 'On track'}
                </span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2 mb-3">
                <div
                  className={`h-2 rounded-full transition-all ${isOver ? 'bg-red-500' : isNear ? 'bg-amber-500' : 'bg-green-500'}`}
                  style={{ width: `${Math.min(percent, 100)}%` }}
                />
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-400">
                  €{budget.amount_spent.toLocaleString('pt-PT', { minimumFractionDigits: 2 })} spent
                </span>
                <span className="text-gray-400">
                  €{budget.amount_limit.toLocaleString('pt-PT', { minimumFractionDigits: 2 })} limit
                </span>
              </div>
            </div>
          )
        })}
        {!budgetStatus?.length && (
          <div className="text-gray-400 text-sm">No budgets yet</div>
        )}
      </div>
    </div>
  )
}