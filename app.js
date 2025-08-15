document.addEventListener('DOMContentLoaded', () => {
    const apiKey = "d2d1e3cde3b87e265b99f988ada138aa"; // あなたのAPIキーに置き換えてください
    const locationElement = document.getElementById('location');
    const tempElement = document.getElementById('temperature');
    const descElement = document.getElementById('description');
    const iconElement = document.getElementById('weather-icon'); // アイコン要素を追加

    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                getWeather(lat, lon);
            },
            () => {
                locationElement.textContent = "位置情報の取得に失敗しました。";
                tempElement.textContent = "";
                descElement.textContent = "位置情報の利用を許可してください。";
            }
        );
    } else {
        locationElement.textContent = "このブラウザは位置情報に対応していません。";
    }

    async function getWeather(lat, lon) {
        try {
            const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric&lang=ja`;
            const response = await fetch(url);
            const data = await response.json();

            if (response.ok) {
                locationElement.textContent = data.name;
                tempElement.textContent = `${Math.round(data.main.temp)}°C`;
                descElement.textContent = data.weather[0].description;

                // 新しく追加したアイコン表示処理
                const iconCode = data.weather[0].icon;
                iconElement.src = `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
                iconElement.alt = data.weather[0].description;
            } else {
                locationElement.textContent = "天気予報の取得に失敗しました。";
                tempElement.textContent = "";
                descElement.textContent = `エラー: ${data.message}`;
            }
        } catch (error) {
            locationElement.textContent = "通信中にエラーが発生しました。";
            tempElement.textContent = "";
            descElement.textContent = "";
        }
    }
});