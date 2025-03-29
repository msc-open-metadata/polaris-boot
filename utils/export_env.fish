if test -f .env
    for line in (cat .env | grep -v '^#' | grep -v '^\s*$')
        set item (string split -m 1 '=' $line)
        set -gx (string trim $item[1]) (string trim $item[2])
        echo "Exported $item[1]"
    end
else
    echo ".env file not found"
end
