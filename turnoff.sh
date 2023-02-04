
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

while IFS= read -r line; do
    kill -9 $line
done < pid.txt