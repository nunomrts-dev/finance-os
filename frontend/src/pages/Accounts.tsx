import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getAccounts, createAccount } from '../api/accounts'

export default function Accounts() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    name: '',
    type: 'checking',
    currency: 'EUR',
    current_balance: '',
  })

  const { data: accounts, isLoading } = useQuery({
    queryKey: ['accounts'],
    queryFn: getAccounts,
  })

  const mutation = useMutation({
    mutationFn: createAccount,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] })
      queryClient.invalidateQueries({ queryKey: ['networth'] })
      setShowForm(false)
      setForm({ name: '', type: 'checking', currency: 'EUR', current_balance: '' })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({
      name: form.name,
      type: form.type,
      currency: form.currency,
      current_balance: parseFloat(form.current_balance),
    })
  }

  const totalBalance = accounts?.reduce((sum, a) => sum + a.current_balance, 0) ?? 0

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white">Accounts</h2>
          <p className="text-gray-400 text-sm mt-1">
            Total: €{totalBalance.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          {showForm ? 'Cancel' : '+ Add Account'}
        </button>
      </div>

      {showForm && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">New Account</h3>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Account Name</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                placeholder="e.g. CGD Main"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Type</label>
              <select
                value={form.type}
                onChange={(e) => setForm({ ...form, type: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              >
                <option value="checking">Checking</option>
                <option value="savings">Savings</option>
                <option value="cash">Cash</option>
                <option value="investment">Investment</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Starting Balance (€)</label>
              <input
                type="number"
                step="0.01"
                value={form.current_balance}
                onChange={(e) => setForm({ ...form, current_balance: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                disabled={mutation.isPending}
                className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                {mutation.isPending ? 'Saving...' : 'Save Account'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {isLoading ? (
          <div className="text-gray-400">Loading...</div>
        ) : (
          accounts?.map((account) => (
            <div key={account.id} className="bg-gray-900 rounded-xl p-5 border border-gray-800">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-white font-semibold">{account.name}</h3>
                <span className="text-xs text-gray-400 capitalize bg-gray-800 px-2 py-1 rounded">
                  {account.type}
                </span>
              </div>
              <p className="text-2xl font-bold text-white">
                €{account.current_balance.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-gray-400 text-sm mt-1">{account.currency}</p>
            </div>
          ))
        )}
        {!accounts?.length && !isLoading && (
          <div className="text-gray-400 text-sm">No accounts yet</div>
        )}
      </div>
    </div>
  )
}