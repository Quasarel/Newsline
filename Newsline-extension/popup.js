document.addEventListener('DOMContentLoaded', function() {
    var xhr = new XMLHttpRequest();
    // xhr.onreadystatechange = function() {
    //   if (xhr.readyState === XMLHttpRequest.DONE) {
    //     if (xhr.status === 200) {
    //       document.getElementById('content').innerHTML = xhr.responseText;
    //     } else {
    //       console.error('Failed to fetch website content');
    //     }
    //   }
    // };
    // xhr.open('GET', 'https://feeder.co/1/feeds/', true);
    xhr.open('GET', 'http://127.0.0.1:8000/feeds', true);
    // xhr.open('GET', 'http://127.0.0.1:8000/', true);
    xhr.onload = function () {
        // Проверяем, что статус ответа успешный (200)
        if (xhr.status === 200) {
          // Парсим полученный JSON ответ
          var jsonData = JSON.parse(xhr.responseText);
      
          // Создаем HTML для отображения данных
          var htmlContent = '';
          index = 0;
          jsonData.feeds.forEach(function(feed) {
            // htmlContent += '<li>';
            htmlContent += '<div class="item';
            htmlContent += (index % 2 == 0) ?' odd">':' even">'
            htmlContent += '<a href="' + feed.id + '" target="_blank">'
            htmlContent += '<div class="item-meta">'
            htmlContent += '<div class="item-favicon"><img width="14" src="' + feed.icon + '"></div>';
            htmlContent += '<div class="item-sub-title">' + feed.domain + '</div>';
            htmlContent += '<div class="item-date">' + feed.published +'</div>';
            htmlContent += '</div>';
            
            htmlContent += '<div class="item-content" style="font-size: 13px;">'
            htmlContent += '<strong>' + feed.title + '</strong></a>';
            htmlContent += '</div>';
            index++;
            
            // htmlContent += '</li>';
            htmlContent += '</div>';
          });
        //   htmlContent += '</ul>';
      
      
          // Отображаем HTML в интерфейсе popup-окна
          document.getElementById('content').innerHTML = htmlContent;
        } else {
          console.error('Failed to load data. Status:', xhr.status);
        }
      };
      
      // Устанавливаем обработчик для события onerror, который вызывается при ошибке запроса
      xhr.onerror = function () {
        console.error('Failed to load data');
      };
    xhr.send();
  });