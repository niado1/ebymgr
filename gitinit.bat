git checkout -b main

for /f %i in (file_list.txt) do git add %i
git commit -m "Initial commit"
git push -u origin main