import calendar
from datetime import datetime
import base64
import requests
import os
from dotenv import load_dotenv
import pandas as pd

# .envファイルの内容を読み込見込む
load_dotenv()

# --- 設定項目 ---
service_user_token = base64.b64decode(os.environ['API_KEY_BASE64']).decode("utf-8").strip()
all_session_url = f"{os.environ['BASE_URL']}/{os.environ['ORG_ID']}/sessions"

def get_total_acu_consumed(after_timestamp, before_timestamp):
    headers = {
        "Authorization": f"Bearer {service_user_token}",
        "Content-Type": "application/json"
    }
    
    total_acu = 0.0
    item_count = 0
    next_page_token = None
    output_records = []
    
    while True:
        # ページネーション用のパラメータ設定
        params = {
            "after": next_page_token,
            "created_after": after_timestamp,
            "created_before": before_timestamp
        }
        if next_page_token:
            params["page_token"] = next_page_token
        
        response = requests.get(all_session_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        items = data.get("items", [])
        
        # 各 session の acus_consumed を加算
        for item in items:
            acu = item.get("acus_consumed", 0)
            total_acu += float(acu)
            item_count += 1
            output_records.append({
                "session_id": item.get("session_id"),
                "url": item.get("url"),
                # "title": item.get("title")
                "user_id": item.get("user_id"),
                "acus_consumed": item.get("acus_consumed", 0),
                "created_at": datetime.fromtimestamp(item.get("created_at")).strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": datetime.fromtimestamp(item.get("updated_at")).strftime('%Y-%m-%d %H:%M:%S'),
                "is_archived": item.get("is_archived")
            })
            
        # 次のページがあるか確認
        next_page_token = data.get("end_cursor")
        if not next_page_token:
            break

    print("-" * 35)
    print(f"対象セッション数: {item_count}")
    print(f"個人合計消費 ACU: {total_acu:.4f}")
    print("-" * 35)

    df = pd.DataFrame(output_records)
    # CSVとして保存
    df.to_csv("./output_all_sessions.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    now = datetime.now()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_ts = int(first_day.timestamp())

    last_day_num = calendar.monthrange(now.year, now.month)[1]
    last_day = now.replace(day=last_day_num, hour=23, minute=59, second=59, microsecond=0)
    last_day_ts = int(last_day.timestamp())

    print(f"集計期間: {first_day} - {last_day}")
    print(f"Organization: {os.environ['ORG_ID']} からデータを取得中...")

    get_total_acu_consumed(first_day_ts, last_day_ts)