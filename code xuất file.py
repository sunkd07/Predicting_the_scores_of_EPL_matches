import sqlite3
import pandas as pd

# 1. Lấy dữ liệu từ kho SQLite và sắp xếp theo ngày
conn = sqlite3.connect('epl.db')
df = pd.read_sql_query("SELECT * FROM matches ORDER BY date, match_week", conn)
conn.close()

data = []

# 2. Duyệt từng trận đấu để tính thông số quá khứ
for i, row in df.iterrows():
    date, home, away = row['date'], row['home_team'], row['away_team']
    past = df[df['date'] < date] # Chỉ lấy các trận trong quá khứ (chống gian lận)

    # Lọc 5 trận gần nhất của Đội nhà & Đội khách (bất kể đá sân nào)
    h_5 = past[(past['home_team'] == home) | (past['away_team'] == home)].tail(5)
    a_5 = past[(past['home_team'] == away) | (past['away_team'] == away)].tail(5)

    # Lọc 5 trận đối đầu gần nhất giữa 2 đội này
    h2h = past[((past['home_team'] == home) & (past['away_team'] == away)) |
               ((past['home_team'] == away) & (past['away_team'] == home))].tail(5)

    # Tính trung bình bàn thắng & thủng lưới (Nếu chưa có lịch sử thì lấy mặc định 0.0 và 1.0)
    h_scored   = h_5.apply(lambda r: r['home_goals'] if r['home_team'] == home else r['away_goals'], axis=1).mean() if len(h_5) > 0 else 0.0
    h_conceded = h_5.apply(lambda r: r['away_goals'] if r['home_team'] == home else r['home_goals'], axis=1).mean() if len(h_5) > 0 else 0.0

    a_scored   = a_5.apply(lambda r: r['home_goals'] if r['home_team'] == away else r['away_goals'], axis=1).mean() if len(a_5) > 0 else 0.0
    a_conceded = a_5.apply(lambda r: r['away_goals'] if r['home_team'] == away else r['home_goals'], axis=1).mean() if len(a_5) > 0 else 0.0

    h2h_home   = h2h.apply(lambda r: r['home_goals'] if r['home_team'] == home else r['away_goals'], axis=1).mean() if len(h2h) > 0 else 1.0
    h2h_away   = h2h.apply(lambda r: r['away_goals'] if r['home_team'] == home else r['home_goals'], axis=1).mean() if len(h2h) > 0 else 1.0

    # Dán nhãn kết quả: H (Nhà thắng), A (Khách thắng), D (Hòa)
    label = 'H' if row['home_goals'] > row['away_goals'] else ('A' if row['home_goals'] < row['away_goals'] else 'D')

    # Gom đúng 7 cột (6 feature + 1 label)
    data.append([h_scored, h_conceded, a_scored, a_conceded, h2h_home, h2h_away, label])

# 3. Lưu ra file CSV bàn giao cho Machine Learning
cols = ['home_scored_last5', 'home_conceded_last5', 'away_scored_last5', 'away_conceded_last5', 'h2h_home_goals', 'h2h_away_goals', 'result']
pd.DataFrame(data, columns=cols).to_csv('ml_features_dataset.csv', index=False)

print("Đã xuất file ml_features_dataset.csv!")