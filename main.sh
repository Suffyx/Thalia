pip install -r requirements.txt > /dev/null &
echo "Installing Dependencies..."
echo -ne '#              \r'
sleep 1
echo -ne '##             \r'
echo -ne '####           \r'
sleep 1
echo -ne '####           \r'
echo -ne '#####          \r'
sleep 1
echo -ne '######         \r'
echo -ne '#######        \r'
sleep 1
echo -ne '########       \r'
echo -ne '#########      \r'
sleep 1
echo -ne '##########     \r'
echo -ne '###########    \r'
sleep 1
echo -ne '############   \r'
echo -ne '\n'

python3 bot.py
