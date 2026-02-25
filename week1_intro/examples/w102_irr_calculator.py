# 請先安裝 numpy_financial: pip install numpy_financial
import numpy_financial as npf

def calculate_irr(cash_flows):
    """
    計算內部報酬率 (IRR)
    :param cash_flows: 現金流 List
    :return: IRR 百分比
    """
    # 使用 numpy_financial 提供的 irr 函數
    irr = npf.irr(cash_flows)
    return irr

if __name__ == "__main__":
    # 範例數據：初始投資 10000，未來三年分別拿回 3000, 4200, 6800
    cash_flows = [-10000, 3000, 4200, 6800]
    
    result = calculate_irr(cash_flows)
    
    print(f"現金流: {cash_flows}")
    # 將結果轉換為百分比格式
    print(f"計算出的 IRR 為: {result * 100:.2f}%")
