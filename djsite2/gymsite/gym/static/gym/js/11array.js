const passengers = [];
    function addPassenger() {
        const name = document.getElementById('passengerName').value;
        const itemsCount = parseInt(document.getElementById('itemsCount').value);
        const totalWeight = parseFloat(document.getElementById('totalWeight').value);

        if (!isNaN(itemsCount) && !isNaN(totalWeight) && itemsCount>0 && totalWeight>0) {
            passengers.push({ name, itemsCount, totalWeight });
            updateResults();
            alert(`Пассажир ${name} добавлен.`);
        } else {
            alert('Пожалуйста, введите корректные значения.');
        }
    }
    function removePassenger() {
        const nameToRemove = document.getElementById('removePassengerName').value;
        const indexToRemove = passengers.findIndex(passenger => passenger.name === nameToRemove);

        if (indexToRemove !== -1) {
            passengers.splice(indexToRemove, 1);
            updateResults();
            alert(`Пассажир ${nameToRemove} удален.`);
        } else {
            alert(`Пассажир ${nameToRemove} не найден.`);
        }
    }
    function findAverageWeightDifference() {
        const averageWeight = calculateAverageWeight();

        if (passengers.length === 0) {
            alert('Добавьте хотя бы одного пассажира.');
            return;
        }

        let closestPassenger = null;
        let minDifference = Number.MAX_VALUE;

        passengers.forEach(passenger => {
            const passengerAverageWeight = passenger.totalWeight / passenger.itemsCount;
            const difference = Math.abs(passengerAverageWeight - averageWeight);

            if (difference <= 0.3 && difference < minDifference) {
                minDifference = difference;
                closestPassenger = passenger;
            }
        });

        if (closestPassenger) {
            document.getElementById('result').innerText = `Найден пассажир: ${closestPassenger.name}`;
        } else {
            document.getElementById('result').innerText = 'Подходящий пассажир не найден.';
        }
    }
    function calculateAverageWeight() {
        if (passengers.length === 0) {
            return 0;
        }

        let totalItemsCount = 0;
        let totalWeight = 0;

        passengers.forEach(passenger => {
            totalItemsCount += passenger.itemsCount;
            totalWeight += passenger.totalWeight;
        });

        return totalWeight / totalItemsCount;
    }

    function updateResults() {
        const resultElement = document.getElementById('result');
        resultElement.innerText = '';

        passengers.forEach(passenger => {
            resultElement.innerText += `Фамилия: ${passenger.name}, Количество вещей: ${passenger.itemsCount}, Общий вес: ${passenger.totalWeight}\n`;
        });
    }