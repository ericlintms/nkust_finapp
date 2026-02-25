def calculate_npv(rate, cash_flows):
    """
    計算淨現值 (NPV)
    :param rate: 折現率 (例如 0.05 代表 5%)
    :param cash_flows: 現金流 List (第一項通常為負數，代表初始投資)
    :return: NPV 數值
    """
    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + rate) ** t)
    return npv

if __name__ == "__main__":
    # 範例數據：初始投資 10000，未來三年分別拿回 3000, 4200, 6800
    cash_flows = [-10000, 3000, 4200, 6800]
    discount_rate = 0.05  # 5% 的折現率

    result = calculate_npv(discount_rate, cash_flows)
    print(f"現金流: {cash_flows}")
    print(f"折現率: {discount_rate*100}%")
    print(f"計算出的 NPV 為: {result:.2f}")

    if result > 0:
        print("結論: NPV大於0，這是一項好投資！")
    else:
        print("結論: NPV小於0，應該放棄這項投資。")
