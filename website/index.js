document.getElementById('registrationForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const fullName = document.getElementById('fullName').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert('Passwords dont match!');
        return;
    }

    try {
        const response = await fetch('http://localhost:3000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fullName, username, email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            alert('Registration successful! Your ID is ' + data.userId);
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (err) {
        console.error(err);
        alert('An error occurred.');
    }
});
