#!/bin/bash
echo "Running db init script"

mysql -u root --password="$MYSQL_ROOT_PASSWORD"  << EOF
USE ${MYSQL_DATABASE};
GRANT ALL PRIVILEGES ON  test_${MYSQL_DATABASE}.* TO '${MYSQL_USER}';
EOF

echo "Done running db init script"

