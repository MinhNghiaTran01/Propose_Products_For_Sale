const fs = require('fs');

// Đường dẫn tới file a.json
const aFilePath = './output.json';

// Đọc dữ liệu từ file a.json
const aData = JSON.parse(fs.readFileSync(aFilePath, 'utf8'));

// Hàm để lấy phần chính của link (i.xxxxx.yyyyy)
const getMainPart = (link) => {
  const match = link.match(/i\.\d+\.\d+/);
  return match ? match[0] : null;
};

// Tạo một tập hợp để lưu trữ các phần chính của link đã gặp
const seenLinks = new Set();
const filteredData = [];

aData.forEach(item => {
  const mainPart = getMainPart(item.link);
  if (mainPart && !seenLinks.has(mainPart)) {
    seenLinks.add(mainPart);
    filteredData.push(item);
  }
});

// Ghi kết quả vào file a.json
fs.writeFileSync(aFilePath, JSON.stringify(filteredData, null, 2));

console.log(`Đã lọc và lưu kết quả vào file ${aFilePath}`);
