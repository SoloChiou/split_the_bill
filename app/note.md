# 架構設計

<!-- prettier-ignore -->
+------------+                +---------------+                 +--------------------+
|   client   |--------------->| Flask /Python |---------------> |      database      |
| (frontend) |<-------------- |   (backend)   |<--------------- | groups/member/money|
+------------+                +---------------+                 +--------------------+
  templates                                                      Docker --> MySql/GCP
    vue

# Database 規劃
