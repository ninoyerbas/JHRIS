"""Constants used throughout JHRIS application."""

# Employee status constants
STATUS_ACTIVE = 'active'
STATUS_INACTIVE = 'inactive'

# Allowed employee status values
ALLOWED_STATUSES = [STATUS_ACTIVE, STATUS_INACTIVE]

# Validation patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
DATE_PATTERN = r'^\d{4}-\d{2}-\d{2}$'
