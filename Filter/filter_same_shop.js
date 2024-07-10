const fs = require('fs');

// Đường dẫn tới file a.json
const aFilePath = './data_shop_detail_after_filter.json';

// Hàm để lấy phần chính của link (i.xxxxx)
const getMainPart = (link) => {
  const match = link.match(/i\.(\d+)\./);
  return match ? match[1] : null;
};

try {
  // Đọc dữ liệu từ file a.json
  const aData = JSON.parse(fs.readFileSync(aFilePath, 'utf8'));

  // Lấy các phần định danh từ currentPageLink trong a.json
  const identifiers = aData.map(item => getMainPart(item.currentPageLink));

  // Tạo một tập hợp để kiểm tra các phần định danh trùng lặp
  const seen = new Set();
  const duplicates = new Set();

  identifiers.forEach(id => {
    if (seen.has(id)) {
      duplicates.add(id);
    } else {
      seen.add(id);
    }
  });

  if (duplicates.size > 0) {
    console.log(`Các phần định danh trùng lặp: ${Array.from(duplicates).join(', ')}`);
  } else {
    console.log('Không có phần định danh nào trùng lặp.');
  }
} catch (err) {
  console.error("Đã xảy ra lỗi khi đọc hoặc xử lý file JSON:", err);
}
