"""
Week 1 - 前置練習：Python 基礎熱身 (w100_python_basics.py)

這個練習確認三個財務開發最核心的 Python 工具：
  1. list     -- 現金流序列、報酬率陣列
  2. dict     -- 投資組合記錄、財務指標物件
  3. def 函式 -- 把公式包裝成可重覆使用的計算單元

執行方式：
  python w100_python_basics.py
"""

# ──────────────────────────────────────────────
# Part 1：list 操作 (現金流序列)
# ──────────────────────────────────────────────
cash_flows = [-100_000, 20_000, 30_000, 40_000, 50_000]  # 期初投入 + 未來四年現金流

print("=== Part 1: List 操作 ===")
print(f"現金流序列：{cash_flows}")
print(f"共 {len(cash_flows)} 期（含第 0 期）")
print(f"期初投入：{cash_flows[0]:,} 元")
print(f"未來各期現金流統計：最大={max(cash_flows[1:]):,}, 總和={sum(cash_flows[1:]):,}")

# ──────────────────────────────────────────────
# Part 2：dict 操作 (投資組合記錄)
# ──────────────────────────────────────────────
print("\n=== Part 2: Dict 操作 ===")

portfolio = {
    "name": "我的退休計劃",
    "initial_amount": 100_000,
    "annual_rate": 0.07,
    "years": 10,
}

print(f"投資組合名稱：{portfolio['name']}")
print(f"本金：{portfolio['initial_amount']:,} 元")
print(f"年報酬率：{portfolio['annual_rate'] * 100:.1f}%")

# ──────────────────────────────────────────────
# Part 3：def 函式 (把終值公式包裝起來)
# ──────────────────────────────────────────────
print("\n=== Part 3: def 函式 ===")


def calculate_future_value(initial_amount: float, annual_rate: float, years: int) -> float:
    """
    計算單筆投入的複利終值。
    
    Args:
        initial_amount: 初始本金 (元)
        annual_rate   : 年化報酬率 (小數，例如 0.07 代表 7%)
        years         : 投資年數
    
    Returns:
        years 年後的終值 (元)
    """
    return initial_amount * (1 + annual_rate) ** years


def create_portfolio(name: str, amount: float, rate: float) -> dict:
    """
    建立一個包含 10 年終值的投資組合記錄（字典）。
    
    Args:
        name  : 投資組合名稱
        amount: 初始本金 (元)
        rate  : 年化報酬率 (小數)
    
    Returns:
        dict 格式的投資組合，含 10 年終值
    """
    fv_10yr = calculate_future_value(amount, rate, 10)
    return {
        "name": name,
        "initial_amount": amount,
        "annual_rate": rate,
        "fv_10yr": round(fv_10yr, 2),
    }


# ── 實際執行看看 ──
my_plan = create_portfolio("我的退休計劃", 100_000, 0.07)
print(f"投資組合：{my_plan['name']}")
print(f"  本金：{my_plan['initial_amount']:,} 元")
print(f"  年報酬率：{my_plan['annual_rate'] * 100:.1f}%")
print(f"  預估 10 年終值：{my_plan['fv_10yr']:,.2f} 元")

# ── 進階挑戰：建立多個組合，放在 list 裡比較 ──
print("\n=== 進階挑戰：多組合比較 ===")
plans = [
    create_portfolio("保守型 (定存 2%)", 100_000, 0.02),
    create_portfolio("穩健型 (ETF 7%)", 100_000, 0.07),
    create_portfolio("積極型 (股票 12%)", 100_000, 0.12),
]

for plan in plans:
    gain = plan["fv_10yr"] - plan["initial_amount"]
    print(f"  {plan['name']}: 10 年後 {plan['fv_10yr']:>12,.2f} 元  |  獲利 {gain:>10,.2f} 元")
