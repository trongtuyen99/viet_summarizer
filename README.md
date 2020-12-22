# viet_summarizer
- Xây dựng mô hình tóm tắt văn bản dựa trên phương pháp trích xuất (extraction-based) với 3 mô hình chính:
  - Clustering (Kmean)
  - TextRank (ý tưởng cơ bản giống với pagerank)
  - Lsa
- Chạy ứng dụng trên nền web (chi tiết trong file report)
  - Cách chạy:
    - cd vào thư mục chứa file main.py (`viet_summarizer/tree/main/src/main.py`)
    - Chạy lệnh:
      ```sh
      streamlit run main.py
      ```
- Các thư viện liên quan:
  - numpy, pandas, matplotlib
  - sklearn
  - nltk
  - gensim
  - pyvi
  - networkx 
  - streamlit
