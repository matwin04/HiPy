var avrStatus = document.getElementById('pwrbtn');
if (avrStatus.textContent === 'ON') {
    avrStatus.style.color = 'green';
}
else if (avrStatus.textContent === 'STANDBY') {
    avrStatus.style.color = 'red';
}