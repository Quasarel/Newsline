document.addEventListener('DOMContentLoaded', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://127.0.0.1:8000/feeds', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
          var jsonData = JSON.parse(xhr.responseText);
      
          var htmlContent = '';
          index = 0;
          jsonData.feeds.forEach(function(feed) {
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
            
            htmlContent += '</div>';
          });
      
      
          document.getElementById('content').innerHTML = htmlContent;
        } else {
          console.error('Failed to load data. Status:', xhr.status);
        }
      };
      
      xhr.onerror = function () {
        console.error('Failed to load data');
      };
    xhr.send();
  });