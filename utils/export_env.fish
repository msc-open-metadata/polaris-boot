if test -f secrets/.env
    for line in (cat secrets/.env | grep -v '^#' | grep -v '^\s*$')
        set item (string split -m 1 '=' $line)
        set -gx (string trim $item[1]) (string trim $item[2])
        echo "Exported $item[1]"
    end
else
    echo "secrets/.env file not found"
end
