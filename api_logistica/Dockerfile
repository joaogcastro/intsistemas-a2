FROM php:8.2-cli

# Set working directory
WORKDIR /var/www/html

# Instalar extensões do sistema e PHP (sockets)
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    libzip-dev \
    curl \
    && docker-php-ext-install sockets

# Copiar arquivos da aplicação
COPY . /var/www/html

# Instalar Composer
RUN curl -sS https://getcomposer.org/installer | php \
    && php composer.phar install

# Expor porta da API
EXPOSE 8000

# Rodar servidor embutido do PHP
CMD ["php", "-S", "0.0.0.0:8000", "app.php"]
