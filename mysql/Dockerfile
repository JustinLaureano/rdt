FROM mysql:8.0.29

ENV TZ=America/Detroit

# Set proper permissions for mysql data
RUN chown -R mysql:root /var/lib/mysql/

# Add custom config settings
COPY conf/config.cnf /etc/my.cnf.d/docker.cnf

# Expose the mysql port
EXPOSE 3306

# Start mysql service
# CMD ["mysqld", "--default-time-zone=-06:00"]
CMD ["mysqld"]