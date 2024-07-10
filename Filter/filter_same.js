const fs = require('fs');

// Đường dẫn tới file a.json
const aFilePath = './data_shop_detail.json';
const outputFilePath = './data_shop_detail_after_filter.json';

// Hàm để lấy phần chính của link (i.xxxxx)
const getMainPart = (link) => {
  const match = link.match(/i\.(\d+)\./);
  return match ? match[0] : null; // Sử dụng match[0] để giữ lại "i.xxxxx"
};

try {
  // Đọc dữ liệu từ file a.json
  const aData = JSON.parse(fs.readFileSync(aFilePath, 'utf8'));

  // Tạo đối tượng để lưu trữ các phần định danh duy nhất
  const identifierMap = {};

  aData.forEach(item => {
    const mainPart = getMainPart(item.currentPageLink);
    if (mainPart && !identifierMap[mainPart]) {
      identifierMap[mainPart] = item; // Lưu trữ object đầu tiên gặp phải
    }
  });

  // Tạo danh sách các object duy nhất
  const filteredData = Object.values(identifierMap);

  // Lưu kết quả vào file output.json
  fs.writeFileSync(outputFilePath, JSON.stringify(filteredData, null, 2), 'utf8');

  console.log(`Đã lọc và lưu kết quả vào file ${outputFilePath}`);
} catch (err) {
  console.error("Đã xảy ra lỗi khi đọc hoặc xử lý file JSON:", err);
}
