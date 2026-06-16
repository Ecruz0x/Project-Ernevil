curl.exe -L "https://get.enterprisedb.com/postgresql/postgresql-17.6-1-windows-x64.exe" -o postgresql-installer.exe

Start-Process ".\postgresql-installer.exe" `
  -ArgumentList "--mode unattended --superpassword yourpassword" `
  -Wait


net start postgresql-x64-17