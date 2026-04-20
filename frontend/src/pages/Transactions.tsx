import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTransactions, createTransaction } from '../api/transactions'
import { getAccounts } from '../api/accounts'
import { getCategories } from '../api/categories'

export default function Transactions() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    account_id: '',
    category_id: '',
    type: 'OUT',
    amount: '',
    description: '',
    date: new Date().toISOString().split('T')[0],
    is_recurring: false,
  })

  const { data: transactions, isLoading } = useQuery({
    queryKey: ['transactions'],
    queryFn: () => getTransactions(),
  })

  const { data: accounts } = useQuery({
    queryKey: ['accounts'],
    queryFn: getAccounts,
  })

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  })

  const mutation = useMutation({
    mutationFn: createTransaction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
      queryClient.invalidateQueries({ queryKey: ['accounts'] })
      queryClient.invalidateQueries({ queryKey: ['networth'] })
      queryClient.invalidateQueries({ queryKey: ['dashboard-summary'] })
      setShowForm(false)
      setForm({
        account_id: '',
        category_id: '',
        type: 'OUT',
        amount: '',
        description: '',
        date: new Date().toISOString().split('T')[0],
        is_recurring: false,
      })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({
      account_id: parseInt(form.account_id),
      category_id: form.category_id ? parseInt(form.category_id) : undefined,
      type: form.type,
      amount: parseFloat(form.amount),
      description: form.description,
      date: new Date(form.date).toISOString(),
      is_recurring: form.is_recurring,
    })
  }

  const filteredCategories = categories?.filter(c => 
    form.type === 'IN' ? c.type === 'INCOME' : c.type === 'EXPENSE'
  )

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Transactions</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          {showForm ? 'Cancel' : '+ Add Transaction'}
        </button>
      </div>

      {showForm && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">New Transaction</h3>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Type</label>
              <select
                value={form.type}
                onChange={(e) => setForm({ ...form, type: e.target.value, category_id: '' })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              >
                <option value="OUT">Expense</option>
                <option value="IN">Income</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Amount (€)</label>
              <input
                type="number"
                step="0.01"
                value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Account</label>
              <select
                value={form.account_id}
                onChange={(e) => setForm({ ...form, account_id: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              >
                <option value="">Select account</option>
                {accounts?.map(a => (
                  <option key={a.id} value={a.id}>{a.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Category</label>
              <select
                value={form.category_id}
                onChange={(e) => setForm({ ...form, category_id: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              >
                <option value="">Select category</option>
                {filteredCategories?.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Description</label>
              <input
                type="text"
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                placeholder="What was this for?"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Date</label>
              <input
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div className="md:col-span-2">
              <button
                type="submit"
                disabled={mutation.isPending}
                className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                {mutation.isPending ? 'Saving...' : 'Save Transaction'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="bg-gray-900 rounded-xl border border-gray-800">
        {isLoading ? (
          <div className="p-6 text-gray-400">Loading...</div>
        ) : (
          <div className="divide-y divide-gray-800">
            {transactions?.map((transaction) => (
              <div key={transaction.id} className="flex items-center justify-between p-4">
                <div>
                  <p className="text-white font-medium">
                    {transaction.description || 'No description'}
                  </p>
                  <p className="text-gray-400 text-sm">
                    {new Date(transaction.date).toLocaleDateString('pt-PT')}
                  </p>
                </div>
                <p className={`font-semibold ${transaction.type === 'IN' ? 'text-green-400' : 'text-red-400'}`}>
                  {transaction.type === 'IN' ? '+' : '-'}€{transaction.amount.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
                </p>
              </div>
            ))}
            {!transactions?.length && (
              <div className="p-6 text-gray-400 text-sm">No transactions yet</div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}