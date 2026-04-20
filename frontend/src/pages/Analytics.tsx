import { useQuery } from '@tanstack/react-query'
import { getDashboardSummary, getSpendingByCategory, getIncomeBySource, getCashflow } from '../api/analytics'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const COLORS = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#818cf8', '#4f46e5', '#4338ca']

interface CashflowItem {
  date: string
  income: number
  expenses: number
  net: number
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const renderLabel = (entry: any) => `${entry.category_name} ${entry.percentage}%`

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const formatEur = (value: any) =>
  `€${Number(value).toLocaleString('pt-PT', { minimumFractionDigits: 2 })}`

export default function Analytics() {
  const { data: summary } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: getDashboardSummary,
  })

  const { data: spending } = useQuery({
    queryKey: ['spending'],
    queryFn: () => getSpendingByCategory(),
  })

  const { data: income } = useQuery({
    queryKey: ['income'],
    queryFn: () => getIncomeBySource(),
  })

  const { data: cashflow } = useQuery({
    queryKey: ['cashflow'],
    queryFn: getCashflow,
  })

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-white mb-6">Analytics</h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm mb-1">Income</p>
          <p className="text-xl font-bold text-green-400">
            {formatEur(summary?.total_income_this_month ?? 0)}
          </p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm mb-1">Expenses</p>
          <p className="text-xl font-bold text-red-400">
            {formatEur(summary?.total_expenses_this_month ?? 0)}
          </p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm mb-1">Net Savings</p>
          <p className="text-xl font-bold text-white">
            {formatEur(summary?.net_savings_this_month ?? 0)}
          </p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm mb-1">Savings Rate</p>
          <p className="text-xl font-bold text-indigo-400">
            {summary?.savings_rate_this_month ?? 0}%
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <h3 className="text-lg font-semibold text-white mb-4">Spending by Category</h3>
          {spending && spending.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={spending}
                  dataKey="total_amount"
                  nameKey="category_name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={renderLabel}
                >
                  {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
                  {spending.map((_: any, index: number) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={formatEur} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-400 text-sm">No spending data yet</p>
          )}
        </div>

        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <h3 className="text-lg font-semibold text-white mb-4">Income by Source</h3>
          {income && income.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={income}
                  dataKey="total_amount"
                  nameKey="category_name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={renderLabel}
                >
                  {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
                  {income.map((_: any, index: number) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={formatEur} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-400 text-sm">No income data yet</p>
          )}
        </div>
      </div>

      <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
        <h3 className="text-lg font-semibold text-white mb-4">Cashflow — Last 6 Months</h3>
        {cashflow && cashflow.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cashflow as CashflowItem[]}>
              <XAxis dataKey="date" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                formatter={formatEur}
                contentStyle={{ backgroundColor: '#111827', border: '1px solid #1f2937' }}
              />
              <Legend />
              <Bar dataKey="income" name="Income" fill="#34d399" />
              <Bar dataKey="expenses" name="Expenses" fill="#f87171" />
              <Bar dataKey="net" name="Net" fill="#818cf8" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-400 text-sm">No cashflow data yet</p>
        )}
      </div>
    </div>
  )
}
