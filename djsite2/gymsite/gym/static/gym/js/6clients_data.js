    document.addEventListener('DOMContentLoaded', function () {
    const maleStat = document.getElementById('male_statistics');
    const femaleStat = document.getElementById('female_statistics');
    const resultContainer = document.getElementById('resultContainer');
    // Отправка AJAX-запроса
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_clients_data/', true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        // Обработка полученных данных
        if(xhr.status === 200){
          var responseData = JSON.parse(xhr.responseText);
          console.log(responseData);
          var femaleCount = 0;
          var maleCount = 0;
          var totalFemaleAge = 0;
          var totalMaleAge = 0;
          responseData.forEach(function (item) {
            if(item.gender === 'F'){
              ++femaleCount;
              totalFemaleAge += item.age
            }
            else{
              ++maleCount;
              totalMaleAge += item.age;
            }
          });
          let total_clients = (femaleCount+maleCount);
          var femalePercentage = (femaleCount/total_clients*100).toFixed(2);
          var malePercentage = (maleCount/total_clients*100).toFixed(2);
          var averFemaleAge = (totalFemaleAge/femaleCount).toFixed(2);
          var averMaleAge = (totalMaleAge/maleCount).toFixed(2);
          resultContainer.innerHTML = `
                        <p>Процент Женщин: ${femalePercentage}% Средний ворсраст: ${averFemaleAge} лет</p>
                        <p>Процент Мужчин: ${malePercentage}% Средний ворсраст: ${averMaleAge} лет</p>
                    `;
        }
        else{
          alert(xhr.status);
        }
      }
    };
    xhr.send();
  });