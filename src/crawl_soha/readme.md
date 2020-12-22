# Crawl dữ liệu trên trang soha.vn
## Các dữ liệu trích xuất từ 1 trang:
1. Tiêu đề
2. Sapo
3. Nội dung
4. Url

## Cách chạy Crawl dữ liệu:
1. Chạy file Crawler.ipynb trong thư mục `crawler`
2. Chạy lệnh trực tiếp trên terminal:
```sh
scrapy crawl crawler_24h -o news_24h.csv
```

* Lưu ý: để chạy crawl dữ liệu dạng duyệt theo chiều sâu với 1 trang web, cần chạy lệnh crawl nhiều lần, có thể viết file bash hoặc chạy `os.system(command)` trong python

## Kết quả
- Dữ liệu crawl được từ trang soha.vn: [600 mb data soha.vn](https://drive.google.com/file/d/1SuYzCb8kpNQRkM24nLdStGp1c9iwPBnQ/view?usp=sharing)
