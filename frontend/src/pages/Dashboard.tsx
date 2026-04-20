import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import { getCurrentNetWorth } from '../api/networth'
import { getDashboardSummary } from '../api/analytics'
import { getAccounts } from '../api/accounts'
import { getTransactions } from '../api/transactions'

export default function Dashboard() {
  const { user, logout } = useAuth()

  const { data: networth } = useQuery({
    queryKey: ['networth'],
    queryFn: getCurrentNetWorth,
    refetchInterval: 30 * 60 * 1000,
  })

  const { data: summary } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: getDashboardSummary,
  })

  const { data: accounts } = useQuery({
    queryKey: ['accounts'],
    queryFn: getAccounts,
  })

  const { data: transactions } = useQuery({
    queryKey: ['transactions'],
    queryFn: () => getTransactions(),
  })

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-white">Finance OS</h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-400 text-sm">{user?.full_name || user?.email}</span>
          <button
            onClick={logout}
            className="text-sm text-gray-400 hover:text-white transition-colors"
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="p-6 max-w-7xl mx-auto">
        {/* Net Worth */}
        <div className="mb-8">
          <p className="text-gray-400 text-sm mb-1">Total Net Worth</p>
          <h2 className="text-5xl font-bold text-white">
            €{networth?.total_net_worth?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
          </h2>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <p className="text-gray-400 text-sm mb-1">Income This Month</p>
            <p className="text-2xl font-semibold text-green-400">
              €{summary?.total_income_this_month?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
            </p>
          </div>
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <p className="text-gray-400 text-sm mb-1">Expenses This Month</p>
            <p className="text-2xl font-semibold text-red-400">
              €{summary?.total_expenses_this_month?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
            </p>
          </div>
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <p className="text-gray-400 text-sm mb-1">Savings Rate</p>
            <p className="text-2xl font-semibold text-indigo-400">
              {summary?.savings_rate_this_month ?? 0}%
            </p>
          </div>
        </div>

        {/* Accounts and Transactions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Accounts */}
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4">Accounts</h3>
            <div className="space-y-3">
              {accounts?.map((account) => (
                <div key={account.id} className="flex items-center justify-between">
                  <div>
                    <p className="text-white font-medium">{account.name}</p>
                    <p className="text-gray-400 text-sm capitalize">{account.type}</p>
                  </div>
                  <p className="text-white font-semibold">
                    €{account.current_balance.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              ))}
              {!accounts?.length && (
                <p className="text-gray-500 text-sm">No accounts yet</p>
              )}
            </div>
          </div>

          {/* Recent Transactions */}
          <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
            <h3 className="text-lg font-semibold mb-4">Recent Transactions</h3>
            <div className="space-y-3">
              {transactions?.slice(0, 5).map((transaction) => (
                <div key={transaction.id} className="flex items-center justify-between">
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
                <p className="text-gray-500 text-sm">No transactions yet</p>
              )}
            </div>
          </div>
        </div>

        {/* Net Worth Breakdown */}
        <div className="mt-6 bg-gray-900 rounded-xl p-5 border border-gray-800">
          <h3 className="text-lg font-semibold mb-4">Portfolio Breakdown</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-400 text-sm">Bank Balance</p>
              <p className="text-xl font-semibold text-white">
                €{networth?.bank_balance?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
              </p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Investment Value</p>
              <p className="text-xl font-semibold text-white">
                €{networth?.investment_value?.toLocaleString('pt-PT', { minimumFractionDigits: 2 }) ?? '0.00'}
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}