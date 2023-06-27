#!/bin/bash

# set -e
# set -u

# function create_user_and_database() {
# 	local database=$1
# 	echo "**Creating user and database '$database'**"
# 	mysql -u root --password="$MYSQL_ROOT_PASSWORD" << EOF
# 	    CREATE DATABASE IF NOT EXISTS ${database};
#         USE ${database};
#         GRANT ALL PRIVILEGES ON  ${database}.* TO '${MYSQL_USER}';
# EOF

# }

# if [ -n "$DATABASES" ]; then
# 	echo "**Multiple database creation requested: $DATABASES**"
# 	for db in $(echo $DATABASES | tr ',' ' '); do
# 		create_user_and_database $db
# 	done
# 	echo "**Multiple databases created**"
# fi

echo "Running db init script"

mysql -u root --password="$MYSQL_ROOT_PASSWORD"  << EOF
USE ${MYSQL_DATABASE};
GRANT ALL PRIVILEGES ON  test_${MYSQL_DATABASE}.* TO '${MYSQL_USER}';
EOF

echo "Done running db init script"
