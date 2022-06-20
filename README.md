# network_centrality


![Betweenness](https://media.springernature.com/lw785/springer-static/image/prt%3A978-1-4419-9863-7%2F5/MediaObjects/978-1-4419-9863-7_5_Part_Fig1-874_HTML.gif)

Betweenness centrality bir ağdaki en kısa yollara dayanan bir göstergedir. Bir vertex ya da kenar üzerinden geçen en kısa yol sayısının ağdaki vertexler arasındaki toplam en kısa yol sayısına oranıyla bulunur.

Toplu taşıma ağlarını graph olarak modellenip, ağ elemanlarının merkezliliklerine göre kritik ağ elemanlarını tespit ederek toplu taşıma ağı hakkında ve ağın performansı ile ilgili yorum yapmak mümkündür. 

network_centrality benim toplu taşıma ağlarının merkezliliklerinin senaryolara bağlı olarak nasıl değiştiğini hesaplamak için yazdığım bazı scriptleri içeriyor. 




İterasyonla yol içindeki yüksek merkezliliğe sahip olan ağ elemanları her iterasyonda çıkarılarak yeni bir ağ oluşturulur ve değişim incelenebilir. Her iterasyonda belirlenen kritik ağ elemanları ağdan çıkartılarak ağ hakkında çok boyutlu bir bakış açısı kazanmak mümkündür.


![İstanbul İlk Hali--Son İterasyon ](https://user-images.githubusercontent.com/48276457/174641738-ab66269c-25e0-4425-b2b3-91f5550eda0c.png)



Aşağıda Brooklyn ve Paris için bu iterasyonla belirlenen kritik ağları görebilirsiniz

![Brooklyn Hepsi](https://user-images.githubusercontent.com/48276457/174641905-679c4848-bbc4-4bb8-a083-68a382f38ad0.png)

![Paris Hepsi](https://user-images.githubusercontent.com/48276457/174642472-7b33ea92-6744-462b-869a-587d45aa616a.png)






Closeness centrality : Ağ elemanlarının birbirine olan en kısa uzaklık ortalamalarına göre belirlenir.


![İstanbul Yakınlılık Merkezliliği](https://user-images.githubusercontent.com/48276457/174642132-d42bec46-2aea-4722-9749-d0bbfbaafb4e.png)






