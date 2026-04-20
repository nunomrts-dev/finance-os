import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getInvestments, createInvestment, getPortfolioPerformance, getPerformanceBySource, getCurrentPrice } from '../api/investments'

interface SourcePerformance {
  funding_source: string
  amount_invested: number
  current_value: number
  gain_loss_eur: number
  gain_loss_percent: number
}

export default function Investments() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    amount_invested_eur: '',
    cspx_price_at_purchase: '',
    units_purchased: '',
    fees: '0',
    funding_source: 'SALARY',
    notes: '',
    date: new Date().toISOString().split('T')[0],
  })

  const { data: investments } = useQuery({
    queryKey: ['investments'],
    queryFn: getInvestments,
  })

  const { data: performance } = useQuery({
    queryKey: ['performance'],
    queryFn: getPortfolioPerformance,
  })

  const { data: bySource } = useQuery({
    queryKey: ['performance-by-source'],
    queryFn: getPerformanceBySource,
  })

  const { data: currentPrice } = useQuery({
    queryKey: ['current-price'],
    queryFn: getCurrentPrice,
    refetchInterval: 30 * 60 * 1000,
  })

  const mutation = useMutation({
    mutationFn: createInvestment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investments'] })
      queryClient.invalidateQueries({ queryKey: ['performance'] })
      queryClient.invalidateQueries({ queryKey: ['performance-by-source'] })
      queryClient.invalidateQueries({ queryKey: ['networth'] })
      setShowForm(false)
      setForm({
        amount_invested_eur: '',
        cspx_price_at_purchase: '',
        units_purchased: '',
        fees: '0',
        funding_source: 'SALARY',
        notes: '',
        date: new Date().toISOString().split('T')[0],
      })
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    mutation.mutate({
      amount_invested_eur: parseFloat(form.amount_invested_eur),
      cspx_price_at_purchase: parseFloat(form.cspx_price_at_purchase),
      units_purchased: parseFloat(form.units_purchased),
      fees: parseFloat(form.fees),
      funding_source: form.funding_source,
      notes: form.notes || undefined,
      date: new Date(form.date).toISOString(),
    })
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Investments</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          {showForm ? 'Cancel' : '+ Add Investment'}
        </button>
      </div>

      {/* Current Price */}
      <div className="bg-gray-900 rounded-xl p-5 border border-gray-800 mb-6">
        <p className="text-gray-400 text-sm mb-1">CSPX Current Price</p>
        <p className="text-3xl font-bold text-white">
          {currentPrice?.price_eur ? `€${currentPrice.price_eur.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}` : 'Market Closed'}
        </p>
        {currentPrice?.fetched_at && (
          <p className="text-gray-400 text-xs mt-1">
            Last updated: {new Date(currentPrice.fetched_at).toLocaleString('pt-PT')}
          </p>
        )}
      </div>

      {/* Performance Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm mb-1">Total Invested</p>
          <p className="text-2xl font-bold text-white">
            €{performance?.total_invested?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
          </p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm mb-1">Current Value</p>
          <p className="text-2xl font-bold text-white">
            €{performance?.current_value?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
          </p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm mb-1">Gain / Loss</p>
          <p className={`text-2xl font-bold ${(performance?.gain_loss_eur ?? 0) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {(performance?.gain_loss_eur ?? 0) >= 0 ? '+' : ''}€{performance?.gain_loss_eur?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
            <span className="text-sm ml-2">({performance?.gain_loss_percent ?? 0}%)</span>
          </p>
        </div>
      </div>

      {/* Source Breakdown */}
      {bySource && bySource.length > 0 && (
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">By Funding Source</h3>
          <div className="space-y-3">
            {bySource.map((source: SourcePerformance) => (
              <div key={source.funding_source} className="flex items-center justify-between">
                <div>
                  <p className="text-white font-medium capitalize">{source.funding_source.toLowerCase()}</p>
                  <p className="text-gray-400 text-sm">Invested: €{source.amount_invested.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}</p>
                </div>
                <p className={`font-semibold ${source.gain_loss_eur >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {source.gain_loss_eur >= 0 ? '+' : ''}€{source.gain_loss_eur.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Add Investment Form */}
      {showForm && (
        <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">New Investment</h3>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Amount Invested (€)</label>
              <input
                type="number"
                step="0.01"
                value={form.amount_invested_eur}
                onChange={(e) => setForm({ ...form, amount_invested_eur: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">CSPX Price at Purchase (€)</label>
              <input
                type="number"
                step="0.01"
                value={form.cspx_price_at_purchase}
                onChange={(e) => setForm({ ...form, cspx_price_at_purchase: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Units Purchased</label>
              <input
                type="number"
                step="0.0001"
                value={form.units_purchased}
                onChange={(e) => setForm({ ...form, units_purchased: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Fees (€)</label>
              <input
                type="number"
                step="0.01"
                value={form.fees}
                onChange={(e) => setForm({ ...form, fees: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Funding Source</label>
              <select
                value={form.funding_source}
                onChange={(e) => setForm({ ...form, funding_source: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
              >
                <option value="SALARY">Salary</option>
                <option value="VINTED">Vinted</option>
                <option value="GIRLFRIEND">Girlfriend</option>
                <option value="SAVINGS">Savings</option>
                <option value="OTHER">Other</option>
              </select>
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
              <label className="block text-sm text-gray-400 mb-1">Notes</label>
              <input
                type="text"
                value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-white"
                placeholder="Optional notes"
              />
            </div>
            <div className="md:col-span-2">
              <button
                type="submit"
                disabled={mutation.isPending}
                className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                {mutation.isPending ? 'Saving...' : 'Save Investment'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Investment List */}
      <div className="bg-gray-900 rounded-xl border border-gray-800">
        <div className="p-4 border-b border-gray-800">
          <h3 className="text-lg font-semibold text-white">Investment History</h3>
        </div>
        <div className="divide-y divide-gray-800">
          {investments?.map((inv) => (
            <div key={inv.id} className="flex items-center justify-between p-4">
              <div>
                <p className="text-white font-medium capitalize">{inv.funding_source.toLowerCase()}</p>
                <p className="text-gray-400 text-sm">
                  {inv.units_purchased} units @ €{inv.cspx_price_at_purchase}
                </p>
                <p className="text-gray-400 text-xs">
                  {new Date(inv.date).toLocaleDateString('pt-PT')}
                </p>
              </div>
              <p className="text-white font-semibold">
                €{inv.amount_invested_eur.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
              </p>
            </div>
          ))}
          {!investments?.length && (
            <div className="p-6 text-gray-400 text-sm">No investments yet</div>
          )}
        </div>
      </div>
    </div>
  )
}