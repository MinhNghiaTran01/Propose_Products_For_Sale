import requests
import re
import json
import os
# URL của API Shopee
def extract_ids(url):
    # Sử dụng regex để tìm kiếm mẫu i.{shopid}.{itemid} trong URL
    match = re.search(r'i\.(\d+)\.(\d+)', url)
    if match:
        shopid = match.group(1)
        itemid = match.group(2)
        return shopid, itemid
    else:
        return None, None
      
def open_file(file):
  try:
    with open(file,'r', encoding='utf-8') as file_read:
      return json.load(file_read)
  except:
    print("Error file is not readable")

def saveDataInFile(data):
    fileSave = './feedback.json'
    existing_data = []  # Khởi tạo sẵn một list rỗng

    # Kiểm tra nếu file tồn tại và cố gắng đọc dữ liệu từ file
    if os.path.exists(fileSave):
        try:
            with open(fileSave, 'r', encoding='utf-8') as file_read:
                existing_data = json.load(file_read)
                # Đảm bảo dữ liệu đọc được là một list
                if not isinstance(existing_data, list):
                    existing_data = []
        except json.JSONDecodeError:
            # Nếu không thể đọc được JSON, giữ existing_data là list rỗng
            print("Không thể đọc dữ liệu JSON từ file, dữ liệu hiện tại sẽ được reset.")

    # Thêm data mới vào list hiện có
    existing_data.append(data)

    # Ghi dữ liệu đã cập nhật trở lại file
    try:
        with open(fileSave, 'w', encoding='utf-8') as file_write:
            json.dump(existing_data, file_write, ensure_ascii=False, indent=4)
        print(f"Dữ liệu đã được lưu vào file {fileSave} thành công.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lưu file: {e}")
  
def getFetchData(path):
  url = 'https://shopee.vn' + path
  headers = {
      'authority': 'shopee.vn',
      'method': 'GET',
      'path': '{path}',
      'scheme': 'https',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-encoding': 'gzip, deflate, br, zstd',
      'accept-language': 'vi,en-US;q=0.9,en;q=0.8,ja;q=0.7',
      'cache-control': 'max-age=0',
      'cookie': '_gcl_au=1.1.692727828.1719906461; _QPWSDCXHZQA=f5685dd9-b0cf-4ae1-a87c-2d6e6674d121; REC7iLP4Q=2b509ed5-ad5f-43d0-826b-8be47c6572e7; _fbp=fb.1.1719906461063.657082909524653350; SPC_F=N0zNLiVFjRcceKJrmtPX46bF0NmBAw2c; REC_T_ID=5c5a1658-3847-11ef-91ed-cef47d801dba; SPC_CLIENTID=TjB6TkxpVkZqUmNjvrdefpiyqixeagmi; SPC_U=301443359; SPC_T_IV=TGpFQ3h4T1lvZTdPMXVGMw==; SPC_R_T_ID=KOorsWlKK/JUpWL3fh9G2j8rTwpcKiHy7b4YANgGL6j+itU6EVZn66uw/MtP8Zr0nY+HoUZ2oErCt0RbczUVrjlsUe6Wmifd2LddpvxzXEAWQ97eRk+cX9atu5+/9+swhSfIPoUlg5Ch6DeV5yZog35Ls4SykiotTk6TqEzeoDs=; SPC_R_T_IV=TGpFQ3h4T1lvZTdPMXVGMw==; SPC_T_ID=KOorsWlKK/JUpWL3fh9G2j8rTwpcKiHy7b4YANgGL6j+itU6EVZn66uw/MtP8Zr0nY+HoUZ2oErCt0RbczUVrjlsUe6Wmifd2LddpvxzXEAWQ97eRk+cX9atu5+/9+swhSfIPoUlg5Ch6DeV5yZog35Ls4SykiotTk6TqEzeoDs=; _hjSessionUser_868286=eyJpZCI6IjA3MWQ5N2YxLTQwNmQtNWU1Yi04N2EwLTUwOTU3M2ViNjNmZiIsImNyZWF0ZWQiOjE3MTk5MDY0NjgzNTQsImV4aXN0aW5nIjp0cnVlfQ==; _gac_UA-61914164-6=1.1719980430.CjwKCAjwyo60BhBiEiwAHmVLJRDUuPAzGLrUGgCfWlYelDYfJ_EPO3Sg9SG8pCrGy2_ZHQXt-GSwdRoCrsEQAvD_BwE; _gcl_aw=GCL.1719980430.CjwKCAjwyo60BhBiEiwAHmVLJRDUuPAzGLrUGgCfWlYelDYfJ_EPO3Sg9SG8pCrGy2_ZHQXt-GSwdRoCrsEQAvD_BwE; __LOCALE__null=VN; csrftoken=zEG6UKtZ3GHYqiep62X3Qn2o0QcswUxZ; _gcl_gs=2.1.k1$i1720231117; _med=affiliates; SPC_SEC_SI=v1-SUpVNkFCU2RJZzNOU2NPTGQVSj5lNS3D1z51GFQC6CRnhUF7WPJesl+mwND3Tn2MHHg6eSAMXP7QTqJRRIw1GsXB9R5oJwC+ZEAd62DXQvg=; SPC_SI=ahVoZgAAAABHSllOd04wTR43JAIAAAAAelJLUHZVQks=; _sapid=e00fa4fcbb2b7799783d8943e45b55a1edf6e8cc4196ad9b32a08407; _hjSession_868286=eyJpZCI6Ijg2ZTQ2NzBlLTA3OGItNGRiMS1hNDVlLTI3Y2YzYmJhNzFiMyIsImMiOjE3MjAyMzExMjc3NDgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; SPC_CDS_CHAT=2dbf9331-d462-4c1f-b34d-2a595ff541d8; shopee_webUnique_ccd=LkN20c%2B3pF2dBnCkQR5Oiw%3D%3D%7C6X2cURdPS3e2j6CKZt0l84658xIU2umpopQL4Vl9F1rl%2BDOjSQEpTcXWnLDoAjkArSQXbsGWL8Y%3D%7Ck3tNdevoFvoClQXU%7C08%7C3; ds=b152d3a3c8b10971bd07cc66933ee926; SPC_IA=1; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.374917494.1719906463; _gid=GA1.2.89507040.1720231134; _ga_4GPP1ZXG63=GS1.1.1720231127.7.1.1720231153.34.0.0',
      'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  }
  # Gửi yêu cầu GET với headers
  response = requests.get(url, headers=headers)
  # Kiểm tra mã trạng thái
  if response.status_code == 200:
      data = response.json()
      ratings = {
        'cmtid': data['data']['ratings']['cmtid'],
        'comment': data['data']['ratings']['comment'],
        'cmtime': data['data']['ratings']['cmtime'],
        'detailed_rating': data['data']['ratings']['detailed_rating'],
        'editable': data['data']['ratings']['editable'],
        'editable_date': data['data']['ratings']['editable_date'],
        'template_tags': data['data']['ratings']['template_tags'],
      }
      return ratings
  else:
      return None
      
def main():
  fileInput = './Infor_product_and_shop_detail.json'
  data = open_file(fileInput)
  if data is not None:
    if isinstance(data, list):
     for item in data:
       if item['link'] is not None:
         shopid,itemid = extract_ids( item['link'] )
         path = f'/api/v2/item/get_ratings?itemid={itemid}&shopid={shopid}'
         while True:
          dataFetch =  getFetchData(path)
          if dataFetch == None:
            break
          item.update(dataFetch)
          saveDataInFile(item)
if __name__ == "__main__":
    main()
