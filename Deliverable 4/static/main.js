const MAIN_SCREEN = document.getElementById('main-screen');
const LOGIN_SCREEN = document.getElementById('login-screen');
const SIGNUP_SCREEN = document.getElementById('signup-screen');

document.getElementById('main-login-button').addEventListener('click', () => {
  MAIN_SCREEN.style.display = 'none';
  LOGIN_SCREEN.style.display = 'block';
})

document.getElementById('main-signup-button').addEventListener('click', () => {
  MAIN_SCREEN.style.display = 'none';
  SIGNUP_SCREEN.style.display = 'block';
})

document.getElementById('login-button').addEventListener('click', () => {
  location.href = "Home"
})

document.getElementById('signup-button').addEventListener('click', () => {
  location.href = "Home"
})