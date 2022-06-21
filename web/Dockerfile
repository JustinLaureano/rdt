FROM rockylinux:8

# Init Setup
RUN dnf update -y && dnf upgrade -y

# Add non-root user for deployments
RUN adduser webuser && gpasswd -a webuser wheel

# Install general utilities
RUN dnf install -y curl firewalld git nano wget net-tools cifs-utils dnf-utils unzip

# Install Repo's
RUN dnf install -y epel-release \
        http://rpms.remirepo.net/enterprise/remi-release-8.rpm && \
    dnf upgrade -y --refresh

# Install PHP
RUN dnf module reset -y php && \
    dnf module enable -y php:remi-8.1 && \
    dnf install -y php php-bcmath php-common php-cli php-curl php-dom php-fpm \
        php-gd php-iconv php-imagick php-json php-ldap php-mbstring php-mcrypt \
        php-memcached php-mysql php-opcache php-pear php-pgsql php-pdo php-readline \
        php-redis php-simplexml php-xml php-xmlreader php-zip php-zlib openssl

# Install Composer
COPY --from=composer:2.2.6 /usr/bin/composer /usr/local/bin/composer

# Install Node.js
RUN dnf module install -y nodejs:16

# Install apache
RUN dnf install -y httpd httpd-tools

# Set custom apache config
COPY conf.d/00-default.conf /etc/httpd/conf.d/00-default.conf

# Add user to apache group
RUN usermod -a -G apache webuser

# Create custom script directory
RUN mkdir /usr/local/scripts

# Copy custom scripts
COPY scripts/ /usr/local/scripts/

# Make the custom scripts executable
RUN chmod u+x /usr/local/scripts/*

# Make default work directory the web server root
WORKDIR /var/www/html

# Expose apache port
EXPOSE 80

# Run startup script on container start
CMD ["/usr/local/scripts/startup.sh"]
