FROM python:2.7.15-slim

# set the working directory to /app
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

# install git flex libcpanplus-perl make
RUN apt-get update && \
    apt-get install -y git flex libcpanplus-perl make

# install perl libs
RUN export PERL_MM_USE_DEFAULT=1 && perl -MCPAN -e 'install List::MoreUtils; install Text::LevenshteinXS; install Parallel::Loops'

# install requirements
RUN pip install -r requirements.txt

# download UGCNormal
RUN git clone https://github.com/carolcoimbra/UGCNormal.git ugc_norm

# configure UGCNormal
RUN cd ugc_norm && sh configure.sh

EXPOSE 5000

# run app.py when the container launches
CMD ["gunicorn", "__init__:create_app()", "-b", ":5000"]
