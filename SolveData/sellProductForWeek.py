import json
import os
from datetime import datetime, timezone, timedelta
import pytz
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def draw_chart(data):
  weeks = list(data.keys())
  sales = list(data.values())

  # Tạo biểu đồ
  plt.figure(figsize=(15, 5))  # Kích thước hợp lý hơn cho biểu đồ
  plt.plot(weeks, sales, marker='o', color='b')
  plt.title('Biểu đồ thể hiện lượt bán hàng theo 2 tuần')
  plt.xlabel('Tuần')
  plt.ylabel('Lượt bán')
  plt.xticks(rotation=45, ha='right', fontsize=8)
  plt.grid(True)
  plt.tight_layout()  # Đảm bảo không có phần nội dung nào bị cắt khi hiển thị
  # Hiển thị biểu đồ
  plt.show()

# Khi gọi hàm, bạn chỉ cần truyền dữ liệu của bạn vào hàm này.
# draw_chart(your_data_dictionary)


def find_earliest_time(datetime_list):
    if datetime_list:
        return min(datetime_list)
    else:
        return None

def find_latest_time(datetime_list):
    if datetime_list:
        return max(datetime_list)
    else:
        return None
      
def convert_timestamp_to_vietnam_time(timestamp):
  # Chuyển đổi timestamp thành đối tượng datetime với nhận thức về múi giờ UTC
  utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
  
  # Thiết lập múi giờ Việt Nam
  vietnam_zone = pytz.timezone('Asia/Ho_Chi_Minh')
  
  # Chuyển đổi datetime sang múi giờ Việt Nam
  vietnam_time = utc_time.astimezone(vietnam_zone)
  
  return vietnam_time.strftime('%d-%m-%Y %H:%M:%S')

def openFile(file):
  if os.path.exists(file):
    print("File already exists")
  with open(file,"r",encoding="utf-8") as f:
    data = json.load(f)
  return data

def saveFile(data,file):
  with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def addTimestampInObject(data):
  for item in data:
    if 'code' in item:
      for cmt in item['ratings']:
        timestamp = convert_timestamp_to_vietnam_time(cmt['ctime'])
        cmt['timestamp'] = timestamp
        
  return data

def count_days_per_two_weeks(datetime_list):
    if not datetime_list:
        return {}
    
    # Đảm bảo rằng tất cả các phần tử trong danh sách là kiểu datetime
    datetime_list = [datetime.strptime(dt, '%d-%m-%Y %H:%M:%S') 
                     if isinstance(dt, str) else dt for dt in datetime_list]
    
    min_date = find_earliest_time(datetime_list)
    max_date = find_latest_time(datetime_list)

    if min_date is None or max_date is None:
        return {}
    
    # Tính toán ngày đầu tiên và cuối cùng của hai tuần đầu tiên chứa ngày sớm nhất
    start_of_week = min_date - timedelta(days=min_date.weekday())  # Chuyển về thứ Hai đầu tuần
    end_of_week = start_of_week + timedelta(days=13)  # Ngày cuối của khoảng 2 tuần (14 ngày)

    # Tạo từ điển để theo dõi số ngày trong mỗi khoảng 2 tuần
    weeks_count = {}

    # Lặp qua từng khoảng 2 tuần từ ngày bắt đầu đến ngày kết thúc
    while start_of_week <= max_date:
        # Đếm số ngày trong khoảng 2 tuần hiện tại
        count = sum(1 for date in datetime_list if start_of_week <= date <= end_of_week)
        week_label = f"{start_of_week.strftime('%d-%m-%Y')} to {end_of_week.strftime('%d-%m-%Y')}"
        weeks_count[week_label] = count

        # Chuẩn bị cho khoảng 2 tuần tiếp theo
        start_of_week += timedelta(days=14)
        end_of_week += timedelta(days=14)

    return weeks_count


def sellProductByWeek(file):
  with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)
  for item in data:
    if 'code' in item:
      time_list = [cmt['timestamp'] for cmt in item['ratings']]
      weeks_count = count_days_per_two_weeks(time_list)
      draw_chart(weeks_count)
      
      
def main():
  file = os.path.abspath('C:\\Thuc tap\\Clone\\DataAlterFiler\\Infor_feed_back_detail.json')
  data = openFile(file)
  # newData = addTimestampInObject(data)
  saveFile(data,file)
  sellProductByWeek(file)
main()