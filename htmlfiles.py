INDEX_HTML = """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Проверка через reCAPTCHA</title>
  <script src="https://www.google.com/recaptcha/api.js" async defer></script>
  <script src="https://telegram.org/js/telegram-web-app.js?56"></script>
  <style>
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      text-align: center;
      font-family: Arial, sans-serif;
    }
    .container {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="g-recaptcha" data-sitekey="{{ site_key }}" data-callback="onSubmit"></div>
  </div>
  <script>
    function onSubmit(token) {
      fetch("/verify", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `g-recaptcha-response=${token}`
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          Telegram.WebApp.sendData("verified");
        } else {
          Telegram.WebApp.sendData("error");
        }
      });
    }
  </script>
</body>
</html>
"""
