const fs = require('fs');


// Đường dẫn tới file a.json và b.json
const aFilePath = './data_qa_nam.json';
const bFilePath = './data_shop_detail_after_filter.json';

// Hàm để lấy phần chính của link (i.xxxxx)
const getMainPart = (link) => {
  const match = link.match(/i\.(\d+)\./);
  return match ? match[1] : null;
};


try {

  if (!fs.existsSync(aFilePath)) {
    throw new Error(`File không tồn tại: ${aFilePath}`);
  }
  if (!fs.existsSync(bFilePath)) {
    throw new Error(`File không tồn tại: ${bFilePath}`);
  }

  // Đọc dữ liệu từ file a.json và b.json
  const aData = JSON.parse(fs.readFileSync(aFilePath, 'utf8'));
  const bData = JSON.parse(fs.readFileSync(bFilePath, 'utf-8'));

  // Lấy các phần định danh từ currentPageLink trong a.json
  const identifiersA = aData.map(item => getMainPart(item.link));

  // Thực hiện lọc qua từng phần tử của aData
  combinedData = []
  aData.forEach((item, index) => {
    const identifier = getMainPart(item.link);
    const matchingBItem  = bData.find(shop => getMainPart(shop.currentPageLink) === identifier);
    
    // Thực hiện các thao tác với từng phần tử của aData
    if (matchingBItem) {
      const combinedItem = {
        ...item,
        shopName: matchingBItem.shopName,
        onlineStatus: matchingBItem.onlineStatus,
        ratings: matchingBItem.ratings,
        responseRate: matchingBItem.responseRate,
        joinTime: matchingBItem.joinTime,
        productsCount: matchingBItem.productsCount,
        responseTime: matchingBItem.responseTime,
        followers: matchingBItem.followers,
      };
      combinedData.push(combinedItem);
    } 
  });
  // console.log(combinedData);
  // console.log(combinedData);
  fs.writeFile("./Infor_product_and_shop_detail.json", JSON.stringify(combinedData, null, 2), (err) => {
    if (err) {
      console.error("Đã xảy ra lỗi khi ghi file JSON:", err);
    } else {
      console.log("Ghi file JSON thành công!");
    }
  });

} catch (err) {
  console.error("Đã xảy ra lỗi khi đọc hoặc xử lý file JSON:", err);
}
