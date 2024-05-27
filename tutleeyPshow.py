import base64
import os


def tutle():
    import finlab
    from finlab import data
    from finlab import backtest
    from finlab import login

    # 登入 FinLab API
    finlab.login("vAaBvcNeAmbi2OLDvq+9SIu96gfJZy8iuFA58yxhWL8QLKNB1jyjWScd+oJ4Y4Bg#vip_m")

    close = data.get('price:收盤價')
    vol = data.get('price:成交股數')
    sma20 = close.average(20)
    sma60 = close.average(60)
    rev = data.get('monthly_revenue:當月營收')
    ope_earn = data.get('fundamental_features:營業利益率')
    yield_ratio = data.get('price_earning_ratio:殖利率(%)')
    boss_hold = data.get("internal_equity_changes:董監持有股數占比")
    rev_growth_rate = data.get('monthly_revenue:去年同月增減(%)')

    cond1 = yield_ratio >= 6
    cond2 = (close > sma20) & (close > sma60)
    cond3 = rev.average(3) > rev.average(12)
    cond4 = ope_earn >= 3
    cond5 = boss_hold >= 10
    cond6 = (vol.average(5) >= 50 * 1000) & (vol.average(5) <= 10000 * 1000)
    cond_all = cond1 & cond2 & cond3 & cond4 & cond5 & cond6
    cond_all = cond_all * rev_growth_rate
    cond_all = cond_all[cond_all > 0].is_largest(10)

    results = backtest.sim(cond_all, resample='W', fee_ratio=1.425 / 1000 / 3, stop_loss=0.06, take_profit=0.5,
                           position_limit=0.125, name='高殖利率烏龜', live_performance_start='2022-05-01')

    return results


if __name__ == "__main__":
    results = tutle()

    # 獲取當前代碼文件的絕對路徑
    current_file_path = os.path.abspath(__file__)

    # 讀取代碼文件,指定編碼為 UTF-8
    with open(current_file_path, 'r', encoding='utf-8') as file:
        code_content = file.read()

    # 將代碼內容進行 base64 編碼
    encoded_code = base64.b64encode(code_content.encode()).decode()

    # 構建輸出文件的路徑
    output_file_path = os.path.join(os.path.dirname(current_file_path), 'tutleeyPshow.txt')

    # 將加密後的代碼寫入新文件
    with open(output_file_path, 'w') as file:
        file.write(encoded_code)