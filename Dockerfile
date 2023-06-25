FROM archlinux:latest

RUN pacman -Syy

RUN pacman -Sy --noconfirm archlinux-keyring && \
    pacman -Syu --noconfirm

RUN pacman -Sy --noconfirm base-devel wget sudo

RUN wget https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tgz && \
    tar -xvf Python-3.11.2.tgz && \
    cd Python-3.11.2 && \
    ./configure --enable-optimizations && \
    make && \
    make install && \
    cd .. && \
    rm -rf Python-3.11.2 && \
    rm Python-3.11.2.tgz && \
    echo "export PATH=\"/usr/local/bin:\$PATH\"" >> /etc/profile.d/python_custom.sh

RUN ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip

RUN pacman -Scc --noconfirm

RUN mkdir /code

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./ /code/

RUN poetry install

#RUN chmod +x ./start_local.sh
#
#ENTRYPOINT [ "./start_local.sh" ]
