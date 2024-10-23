SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
sudo cp "$SCRIPT_DIR/nginx.conf" "/usr/local/nginx/conf/nginx.conf"