FROM arm32v7/ubuntu:latest

RUN apt-get update && \
#   apt-get install -y --no-install-recommends git gcc libcurl4-openssl-dev libssl-dev python-pip python3-pip libboost-python1.58-dev libpython3-dev && \
    apt-get install -y --no-install-recommends git gcc vim libcurl4-openssl-dev libboost-python1.58-dev libpython3-dev libssl-dev python3-pip && \
    rm -rf /var/lib/apt/lists/* 

# install known good versions.  tensorflow is picky and there is a known issue with numpy: https://stackoverflow.com/questions/55890813/how-to-fix-object-arrays-cannot-be-loaded-when-allow-pickle-false-for-imdb-loa
RUN pip3 install setuptools wheel
RUN pip3 install numpy==1.16.1 librosa==0.6.2 keras==2.2.4 tensorflow==1.12.0 azure-storage==0.36.0 requests==2.20.0 flask==1.0.2 pillow==6.0.0

# need to download the keras audio and set to a known good version
RUN git clone https://github.com/chen0040/keras-audio.git &&\
    cd keras-audio && \
    git reset --hard c34c30695169e0f274c0f3d175dba2b4c9dc301a

# need to modify the modify the LRU in cifar.  To do this we just copy over a modified file
COPY . .

# if there is an updated model, copy that file over
COPY ../model/. models/.

RUN mv ./keras-audio/keras_audio ./ && rm -f -r ./keras-audio

EXPOSE 8080/tcp

CMD python3 -u ./audioinference.py