# Diyagram Örneği

Mermaid diyagramını aşağıdaki gibi oluşturabilirsiniz:

```mermaid
graph TD
    A[Başlangıç] --> B{Karar}
    B -->|Evet| C[İşlem 1]
    B -->|Hayır| D[İşlem 2]
    C --> E[Bitiş]
    D --> E
```

## Diğer Diyagram Tipleri

Akış şeması:
```mermaid
flowchart LR
    A[Giriş] --> B(İşlem)
    B --> C{Kontrol}
    C -->|Evet| D[Çıkış]
    C -->|Hayır| B
```

Sıralı diyagram:
```mermaid
sequenceDiagram
    participant Kullanıcı
    participant Sistem
    Kullanıcı->>Sistem: İstek gönder
    Sistem-->>Kullanıcı: Yanıt ver
```

## İpuçları

1. Diyagramı üç backtick ve "mermaid" kelimesi ile başlatın
2. Diyagram tipini belirtin (graph, flowchart, sequenceDiagram vb.)
3. Mermaid sözdizimini kullanarak diyagramınızı oluşturun
4. GitHub otomatik olarak diyagramı görselleştirecektir
