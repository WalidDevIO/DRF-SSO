docker build -t boilerplate_cas:back .
docker run --rm -ti -p 8000:8000 boilerplate_cas:back

#Test callback URL: https://cas.ifremer.fr/login?service=http://134.246.147.156:8000/cas/callback