# Function to set DJANGO_SETTINGS_MODULE
set_django_settings() {
    export DJANGO_SETTINGS_MODULE=website.settings_dev
}

# Run Django command with DJANGO_SETTINGS_MODULE set
run_django_command() {
    set_django_settings
    python3 manage.py "$@"
}

# Check if any arguments are provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command>"
    exit 1
fi

# Run the provided Django command
run_django_command "$@"